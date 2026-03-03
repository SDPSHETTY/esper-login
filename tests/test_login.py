#!/usr/bin/env python3

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import requests

# Import the login module
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import login


class TestEsperLoginError:
    def test_custom_exception_creation(self):
        """Test that custom exception can be created and raised"""
        with pytest.raises(login.EsperLoginError) as excinfo:
            raise login.EsperLoginError("Test error message")
        assert str(excinfo.value) == "Test error message"


class TestKeyringSecurity:
    def test_get_keyring_service_name(self):
        """Test keyring service name generation"""
        endpoint = "test-endpoint"
        expected = "esper-login.test-endpoint"
        assert login.get_keyring_service_name(endpoint) == expected

    def test_sanitize_error_message_api_keys(self):
        """Test that API keys are redacted from error messages"""
        # Test API key pattern
        result = login.sanitize_error_message('api_key: abc123def456ghi789jkl012mno345pqr678')
        assert 'API_KEY_REDACTED' in result

        # Test JWT pattern (will be caught by general token or sensitive data pattern)
        result = login.sanitize_error_message('{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"}')
        assert any(redacted in result for redacted in ['JWT_REDACTED', 'TOKEN_REDACTED', 'SENSITIVE_DATA_REDACTED'])

        # Test authorization header
        result = login.sanitize_error_message('authorization: Bearer sk-1234567890123456789012345678901234567890')
        assert any(redacted in result for redacted in ['AUTH_REDACTED', 'SENSITIVE_DATA_REDACTED'])

    def test_sanitize_error_message_length_limit(self):
        """Test that long messages are handled properly"""
        # Test with a long message that doesn't match sensitive patterns
        long_message = "Error message: " + "Short text " * 50  # Simple repeating text
        result = login.sanitize_error_message(long_message)
        # Should be truncated or sanitized
        assert len(result) <= 520  # Give some buffer for truncation text

    def test_sanitize_error_message_none_input(self):
        """Test sanitization with None input"""
        result = login.sanitize_error_message(None)
        assert result is None


class TestConfigurationManagement:
    def setup_method(self):
        """Setup temporary config directory for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".login"
        self.config_file = self.config_dir / "config.json"

        # Mock the CONFIG_DIR and CONFIG_FILE
        self.original_config_dir = login.CONFIG_DIR
        self.original_config_file = login.CONFIG_FILE
        login.CONFIG_DIR = self.config_dir
        login.CONFIG_FILE = self.config_file

    def teardown_method(self):
        """Cleanup after each test"""
        login.CONFIG_DIR = self.original_config_dir
        login.CONFIG_FILE = self.original_config_file

    def test_load_config_creates_default_when_missing(self):
        """Test that load_config creates default config when file doesn't exist"""
        config = login.load_config()

        assert "active_sessions" in config
        assert "favorites" in config
        assert "recent_tenants" in config
        assert "preferences" in config
        assert self.config_file.exists()

    def test_load_config_reads_existing(self):
        """Test that load_config reads existing config file"""
        test_config = {"test_key": "test_value", "active_sessions": {}}
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)

        config = login.load_config()
        assert config["test_key"] == "test_value"

    def test_save_config(self):
        """Test that save_config writes config to file"""
        test_config = {"test_data": "test_value"}
        login.save_config(test_config)

        assert self.config_file.exists()
        with open(self.config_file, 'r') as f:
            saved_config = json.load(f)
        assert saved_config["test_data"] == "test_value"


class TestSessionManagement:
    def setup_method(self):
        """Setup for session management tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".login"
        self.config_file = self.config_dir / "config.json"

        # Mock the CONFIG_DIR and CONFIG_FILE
        self.original_config_dir = login.CONFIG_DIR
        self.original_config_file = login.CONFIG_FILE
        login.CONFIG_DIR = self.config_dir
        login.CONFIG_FILE = self.config_file

    def teardown_method(self):
        """Cleanup after each test"""
        login.CONFIG_DIR = self.original_config_dir
        login.CONFIG_FILE = self.original_config_file

    @patch('login.keyring.set_password')
    @patch('login.console.print')
    def test_save_session_success(self, mock_print, mock_keyring_set):
        """Test successful session saving"""
        tenant_info = {
            "name": "Test Company",
            "endpoint": "test-endpoint",
            "id": "123"
        }
        token = "test-token-12345"

        login.save_session(tenant_info, token)

        # Verify keyring was called
        mock_keyring_set.assert_called_once_with(
            "esper-login.test-endpoint",
            "api_token",
            token
        )

        # Verify session was saved to config
        config = login.load_config()
        assert "test-endpoint" in config["active_sessions"]
        session = config["active_sessions"]["test-endpoint"]
        assert session["tenant"] == tenant_info
        assert "token" not in session  # Token should not be in config
        assert "login_time" in session
        assert "last_used" in session

    @patch('login.keyring.set_password')
    @patch('login.console.print')
    def test_save_session_keyring_failure(self, mock_print, mock_keyring_set):
        """Test session saving when keyring fails"""
        mock_keyring_set.side_effect = Exception("Keyring error")

        tenant_info = {"name": "Test", "endpoint": "test", "id": "123"}
        login.save_session(tenant_info, "token")

        # Should still save session metadata
        config = login.load_config()
        assert "test" in config["active_sessions"]


class TestAPIFunctions:
    @patch('login.requests.get')
    def test_fetch_companies_success(self, mock_get):
        """Test successful company fetching"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"name": "Test Company"}]}
        mock_get.return_value = mock_response

        result = login.fetch_companies("test-api-key")

        assert result == {"data": [{"name": "Test Company"}]}
        mock_get.assert_called_once()

        # Verify headers
        call_args = mock_get.call_args
        headers = call_args[1]["headers"]
        assert headers["authorization"] == "test-api-key"

    @patch('login.requests.get')
    @patch('login.console.print')
    def test_fetch_companies_api_error(self, mock_print, mock_get):
        """Test company fetching with API error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        with pytest.raises(login.EsperLoginError) as excinfo:
            login.fetch_companies("invalid-key")

        assert "Failed to fetch companies: HTTP 401" in str(excinfo.value)

    @patch('login.requests.get')
    def test_fetch_companies_network_error(self, mock_get):
        """Test company fetching with network error"""
        mock_get.side_effect = requests.RequestException("Connection failed")

        with pytest.raises(login.EsperLoginError) as excinfo:
            login.fetch_companies("test-key")

        assert "Network error fetching companies" in str(excinfo.value)

    @patch('login.requests.post')
    def test_generate_api_token_success(self, mock_post):
        """Test successful API token generation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "generated-token-123"}
        mock_post.return_value = mock_response

        result = login.generate_api_token("company-123", "master-key")

        assert result == "generated-token-123"

        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "/companies/company-123/personal-access-token" in call_args[0][0]

    @patch('login.requests.post')
    def test_generate_api_token_missing_token(self, mock_post):
        """Test token generation when response lacks token"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}  # No token field
        mock_post.return_value = mock_response

        with pytest.raises(login.EsperLoginError) as excinfo:
            login.generate_api_token("company-123", "master-key")

        assert "No API token found in response" in str(excinfo.value)


class TestMigrationFunction:
    def setup_method(self):
        """Setup for migration tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".login"
        self.config_file = self.config_dir / "config.json"

        # Mock the CONFIG_DIR and CONFIG_FILE
        self.original_config_dir = login.CONFIG_DIR
        self.original_config_file = login.CONFIG_FILE
        login.CONFIG_DIR = self.config_dir
        login.CONFIG_FILE = self.config_file

    def teardown_method(self):
        """Cleanup after each test"""
        login.CONFIG_DIR = self.original_config_dir
        login.CONFIG_FILE = self.original_config_file

    @patch('login.keyring.set_password')
    @patch('login.console.print')
    def test_migrate_tokens_to_keyring(self, mock_print, mock_keyring_set):
        """Test migration of plaintext tokens to keyring"""
        # Setup config with plaintext tokens
        config = {
            "active_sessions": {
                "endpoint1": {
                    "token": "plaintext-token-1",
                    "tenant": {"name": "Test1", "endpoint": "endpoint1"}
                },
                "endpoint2": {
                    "tenant": {"name": "Test2", "endpoint": "endpoint2"}
                    # No token here
                }
            }
        }
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

        result = login.migrate_tokens_to_keyring()

        # Should migrate 1 token
        assert result == 1

        # Verify keyring was called
        mock_keyring_set.assert_called_once_with(
            "esper-login.endpoint1",
            "api_token",
            "plaintext-token-1"
        )

        # Verify token removed from config
        updated_config = login.load_config()
        assert "token" not in updated_config["active_sessions"]["endpoint1"]


class TestBrowserIntegration:
    @patch('login.sync_playwright')
    @patch('login.console.print')
    @patch('builtins.input', return_value='')  # Simulate user pressing enter
    def test_auto_login_success(self, mock_input, mock_print, mock_playwright):
        """Test successful browser automation"""
        # Mock playwright objects
        mock_pw_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        # Test the function
        login.auto_login("test-endpoint", "test-token")

        # Verify browser interactions
        mock_page.goto.assert_called_once()
        mock_page.wait_for_selector.assert_called_once()
        mock_page.fill.assert_called_once()
        mock_page.click.assert_called_once()

        # Verify cleanup
        mock_browser.close.assert_called_once()
        mock_pw_instance.stop.assert_called_once()

    @patch('login.sync_playwright')
    @patch('login.console.print')
    def test_auto_login_playwright_error(self, mock_print, mock_playwright):
        """Test browser automation with Playwright error"""
        mock_pw_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        # Make page.goto raise an exception
        mock_page.goto.side_effect = Exception("Timeout error")

        with pytest.raises(login.EsperLoginError) as excinfo:
            login.auto_login("test-endpoint", "test-token")

        assert "Browser automation failed" in str(excinfo.value)

        # Verify cleanup still happens
        mock_browser.close.assert_called_once()
        mock_pw_instance.stop.assert_called_once()


class TestDisplayFunctions:
    @patch('login.console.print')
    def test_display_tenant_info(self, mock_print):
        """Test tenant information display"""
        tenant_data = {
            "name": "Test Company",
            "endpoint": "test-endpoint",
            "id": "123"
        }

        login.display_tenant_info(tenant_data)

        # Verify that console.print was called
        mock_print.assert_called()

    @patch('login.load_config')
    @patch('login.console.print')
    def test_show_active_sessions_empty(self, mock_print, mock_load_config):
        """Test showing active sessions when none exist"""
        mock_load_config.return_value = {"active_sessions": {}}

        login.show_active_sessions()

        # Verify appropriate message was displayed
        mock_print.assert_called()

    @patch('login.load_config')
    @patch('login.console.print')
    def test_show_active_sessions_with_data(self, mock_print, mock_load_config):
        """Test showing active sessions with data"""
        from datetime import datetime
        mock_load_config.return_value = {
            "active_sessions": {
                "test-endpoint": {
                    "tenant": {"name": "Test Co", "endpoint": "test-endpoint"},
                    "last_used": datetime.now().isoformat()
                }
            }
        }

        login.show_active_sessions()

        # Verify console was used to display the table
        mock_print.assert_called()

    @patch('login.console.print')
    def test_show_enhanced_help(self, mock_print):
        """Test help display function"""
        login.show_enhanced_help()

        # Verify help was printed
        mock_print.assert_called()


class TestInteractiveFunctions:
    @patch('login.Prompt.ask')
    def test_interactive_tenant_selector_quit(self, mock_ask):
        """Test interactive selector when user quits"""
        mock_ask.return_value = 'q'
        companies_list = {"data": [{"name": "Test", "endpoint": "test"}]}

        with pytest.raises(KeyboardInterrupt):
            login.interactive_tenant_selector(companies_list)

    @patch('login.Prompt.ask')
    @patch('login.console.print')
    def test_interactive_tenant_selector_valid_choice(self, mock_print, mock_ask):
        """Test interactive selector with valid choice"""
        mock_ask.return_value = '1'
        companies_list = {
            "data": [
                {"name": "Test Company", "endpoint": "test-endpoint", "id": "123"}
            ]
        }

        result = login.interactive_tenant_selector(companies_list)

        assert result == companies_list["data"][0]

    @patch('login.Prompt.ask')
    @patch('login.console.print')
    def test_interactive_tenant_selector_invalid_then_valid(self, mock_print, mock_ask):
        """Test interactive selector with invalid then valid choice"""
        mock_ask.side_effect = ['invalid', '1']
        companies_list = {
            "data": [
                {"name": "Test Company", "endpoint": "test-endpoint"}
            ]
        }

        result = login.interactive_tenant_selector(companies_list)

        assert result == companies_list["data"][0]


class TestSwitchToSession:
    def setup_method(self):
        """Setup for switch session tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".login"
        self.config_file = self.config_dir / "config.json"

        # Mock the CONFIG_DIR and CONFIG_FILE
        self.original_config_dir = login.CONFIG_DIR
        self.original_config_file = login.CONFIG_FILE
        login.CONFIG_DIR = self.config_dir
        login.CONFIG_FILE = self.config_file

    def teardown_method(self):
        """Cleanup after each test"""
        login.CONFIG_DIR = self.original_config_dir
        login.CONFIG_FILE = self.original_config_file

    @patch('login.show_active_sessions')
    @patch('login.console.print')
    def test_switch_to_session_not_found(self, mock_print, mock_show_sessions):
        """Test switching to non-existent session"""
        # Create empty config
        login.save_config({"active_sessions": {}})

        login.switch_to_session("nonexistent-endpoint")

        # Should show error and list sessions
        mock_print.assert_called()
        mock_show_sessions.assert_called_once()

    @patch('login.keyring.get_password')
    @patch('login.auto_login')
    @patch('login.display_tenant_info')
    @patch('login.console.print')
    def test_switch_to_session_success(self, mock_print, mock_display, mock_auto_login, mock_keyring_get):
        """Test successful session switching"""
        # Setup session data
        tenant_info = {"name": "Test Co", "endpoint": "test-endpoint"}
        session_data = {"tenant": tenant_info, "last_used": "2023-01-01T00:00:00"}
        config = {"active_sessions": {"test-endpoint": session_data}}
        login.save_config(config)

        # Mock keyring response
        mock_keyring_get.return_value = "retrieved-token"

        login.switch_to_session("test-endpoint")

        # Verify keyring was called
        mock_keyring_get.assert_called_once_with("esper-login.test-endpoint", "api_token")

        # Verify auto_login was called
        mock_auto_login.assert_called_once_with("test-endpoint", "retrieved-token")

    @patch('login.keyring.get_password')
    @patch('login.console.print')
    def test_switch_to_session_missing_token(self, mock_print, mock_keyring_get):
        """Test switching to session with missing token"""
        # Setup session data
        tenant_info = {"name": "Test Co", "endpoint": "test-endpoint"}
        session_data = {"tenant": tenant_info}
        config = {"active_sessions": {"test-endpoint": session_data}}
        login.save_config(config)

        # Mock keyring returning None (no token)
        mock_keyring_get.return_value = None

        login.switch_to_session("test-endpoint")

        # Should print error message
        mock_print.assert_called()


class TestMainFunction:
    @patch('login.migrate_tokens_to_keyring')
    @patch('login.show_active_sessions')
    def test_main_list_mode(self, mock_show_sessions, mock_migrate):
        """Test main function in list mode"""
        # Mock sys.argv
        original_argv = sys.argv
        sys.argv = ['login.py', '--list']

        try:
            login.main()
            mock_show_sessions.assert_called_once()
        finally:
            sys.argv = original_argv

    @patch('login.migrate_tokens_to_keyring')
    @patch('login.switch_to_session')
    def test_main_switch_mode(self, mock_switch, mock_migrate):
        """Test main function in switch mode"""
        original_argv = sys.argv
        sys.argv = ['login.py', '--switch', 'test-endpoint']

        try:
            login.main()
            mock_switch.assert_called_once_with('test-endpoint')
        finally:
            sys.argv = original_argv

    @patch('login.migrate_tokens_to_keyring')
    @patch('login.show_enhanced_help')
    def test_main_help_mode(self, mock_help, mock_migrate):
        """Test main function in help mode"""
        original_argv = sys.argv
        sys.argv = ['login.py', '--help']

        try:
            login.main()
            mock_help.assert_called_once()
        finally:
            sys.argv = original_argv

    @patch('login.migrate_tokens_to_keyring')
    @patch('login.console.print')
    @patch('os.getenv')
    def test_main_missing_api_key(self, mock_getenv, mock_print, mock_migrate):
        """Test main function with missing API key"""
        original_argv = sys.argv
        sys.argv = ['login.py']
        mock_getenv.return_value = None

        try:
            login.main()
            # Should print error about missing API key
            mock_print.assert_called()
        finally:
            sys.argv = original_argv