import pytest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import load_config, get_credential


class TestConfig:
    """Tests for the config module"""

    def test_load_config_default(self):
        """Test loading config with default values when file doesn't exist"""
        # Use a non-existent file path
        config = load_config("nonexistent_config.toml")

        # Check that default values are used
        assert "cities" in config
        assert config["cities"]["our_city"] == "Brisbane"
        assert config["cities"]["their_city"] == "Melbourne"
        assert "temperature" in config
        assert config["temperature"]["min_comfortable"] == 18
        assert config["temperature"]["max_comfortable"] == 26
        assert "email" in config
        assert "sms" in config
        assert "logging" in config

    def test_load_config_custom(self):
        """Test loading custom config from file"""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".toml", delete=False
        ) as temp_file:
            temp_file.write("""
            [cities]
            our_city = "Sydney"
            their_city = "Perth"
            
            [temperature]
            min_comfortable = 20
            max_comfortable = 28
            
            [logging]
            level = "DEBUG"
            """)
            temp_path = temp_file.name

        try:
            # Load the config
            config = load_config(temp_path)

            # Check that values from file are used
            assert config["cities"]["our_city"] == "Sydney"
            assert config["cities"]["their_city"] == "Perth"
            assert config["temperature"]["min_comfortable"] == 20
            assert config["temperature"]["max_comfortable"] == 28
            assert config["logging"]["level"] == "DEBUG"

            # Check that default values are used for missing sections
            assert "email" in config
            assert "sms" in config
        finally:
            # Clean up
            os.unlink(temp_path)

    @patch("config.os.environ.get")
    @patch("config.subprocess.run")
    def test_get_credential_from_env(self, mock_run, mock_env_get):
        """Test getting credential from environment variable"""
        # Setup environment variable mock
        mock_env_get.return_value = "test_api_key"

        # Call function
        result = get_credential("test", "TEST_ENV_VAR", "test/path")

        # Assertions
        assert result == "test_api_key"
        mock_env_get.assert_called_once_with("TEST_ENV_VAR")
        mock_run.assert_not_called()

    @patch("config.os.environ.get")
    @patch("config.subprocess.run")
    def test_get_credential_from_pass(self, mock_run, mock_env_get):
        """Test getting credential from pass utility"""
        # Setup mocks
        mock_env_get.return_value = None  # No env var
        mock_process = MagicMock()
        mock_process.stdout = "test_password\n"
        mock_run.return_value = mock_process

        # Call function
        result = get_credential("test", "TEST_ENV_VAR", "test/path")

        # Assertions
        assert result == "test_password"
        mock_env_get.assert_called_once_with("TEST_ENV_VAR")
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0] == ["pass", "show", "test/path"]

    @patch("config.os.environ.get")
    @patch("config.subprocess.run")
    def test_get_credential_not_found(self, mock_run, mock_env_get):
        """Test handling when credential is not found"""
        # Setup mocks
        mock_env_get.return_value = None  # No env var
        mock_run.side_effect = Exception("Command failed")  # pass fails

        # Call function
        result = get_credential("test", "TEST_ENV_VAR", "test/path")

        # Assertions
        assert result is None
        mock_env_get.assert_called_once_with("TEST_ENV_VAR")
        mock_run.assert_called_once()

