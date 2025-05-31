import pytest
from unittest.mock import patch, MagicMock
import json
import sys
import os
import requests

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_api import (
    get_weather,
    is_sunny,
    is_rainy,
    is_temperature_comfortable,
    get_temperature,
)

# Sample weather data for testing
SAMPLE_SUNNY_DATA = {
    "weather": [{"main": "Clear", "description": "clear sky"}],
    "main": {"temp": 23.5},
}

SAMPLE_RAINY_DATA = {
    "weather": [{"main": "Rain", "description": "moderate rain"}],
    "main": {"temp": 12.5},
}

SAMPLE_CLOUDY_DATA = {
    "weather": [{"main": "Clouds", "description": "overcast clouds"}],
    "main": {"temp": 28.5},
}


class TestWeatherAPI:
    """Tests for the weather_api module"""

    @patch("weather_api.requests.get")
    def test_get_weather_success(self, mock_get):
        """Test successful API call to get weather data"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = SAMPLE_SUNNY_DATA
        mock_get.return_value = mock_response

        # Call function
        result = get_weather("Brisbane", "fake_api_key")

        # Assertions
        assert result == SAMPLE_SUNNY_DATA
        mock_get.assert_called_once()
        assert "Brisbane" in mock_get.call_args[0][0]
        assert "fake_api_key" in mock_get.call_args[0][0]

    @patch("weather_api.requests.get")
    def test_get_weather_api_error(self, mock_get):
        """Test API error handling"""
        # Setup mock to raise exception
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        # Call function with mock_type=None to ensure real API is used
        result = get_weather("Brisbane", "fake_api_key", mock_type=None)

        # Assertions
        assert result is None

    def test_get_weather_mock_data(self):
        """Test the mock data functionality"""
        # Test with weather mock
        weather_mock = get_weather("Brisbane", None, "weather")
        assert weather_mock is not None
        assert is_sunny(weather_mock)

        # Test with temperature mock
        temp_mock = get_weather("Melbourne", None, "temperature")
        assert temp_mock is not None
        assert is_sunny(temp_mock)  # Should be sunny but uncomfortable temperature

        # Test with both mock
        both_mock = get_weather("Melbourne", None, "both")
        assert both_mock is not None
        assert is_rainy(both_mock)  # Should be rainy and uncomfortable

    def test_is_sunny(self):
        """Test sunny condition detection"""
        assert is_sunny(SAMPLE_SUNNY_DATA) == True
        assert is_sunny(SAMPLE_RAINY_DATA) == False
        assert is_sunny(SAMPLE_CLOUDY_DATA) == False
        assert is_sunny(None) == False

        # Test with edge cases
        assert is_sunny({"weather": []}) == False
        assert (
            is_sunny({"weather": [{"main": "", "description": "sunny periods"}]})
            == True
        )

    def test_is_rainy(self):
        """Test rainy condition detection"""
        assert is_rainy(SAMPLE_SUNNY_DATA) == False
        assert is_rainy(SAMPLE_RAINY_DATA) == True
        assert is_rainy(SAMPLE_CLOUDY_DATA) == False
        assert is_rainy(None) == False

        # Test with edge cases
        assert is_rainy({"weather": []}) == False
        assert (
            is_rainy({"weather": [{"main": "Drizzle", "description": "light shower"}]})
            == True
        )

    def test_is_temperature_comfortable(self):
        """Test temperature comfort detection"""
        # Normal ranges
        assert is_temperature_comfortable(SAMPLE_SUNNY_DATA, 18, 26) == True
        assert (
            is_temperature_comfortable(SAMPLE_RAINY_DATA, 18, 26) == False
        )  # Too cold
        assert (
            is_temperature_comfortable(SAMPLE_CLOUDY_DATA, 18, 26) == False
        )  # Too hot

        # Edge cases
        assert (
            is_temperature_comfortable(SAMPLE_SUNNY_DATA, 23.5, 24) == True
        )  # Exactly at min
        assert (
            is_temperature_comfortable(SAMPLE_SUNNY_DATA, 23, 23.5) == True
        )  # Exactly at max
        assert is_temperature_comfortable(None, 18, 26) == False
        assert is_temperature_comfortable({}, 18, 26) == False
        assert is_temperature_comfortable({"main": {}}, 18, 26) == False

    def test_get_temperature(self):
        """Test temperature extraction"""
        assert get_temperature(SAMPLE_SUNNY_DATA) == 23.5
        assert get_temperature(SAMPLE_RAINY_DATA) == 12.5
        assert get_temperature(SAMPLE_CLOUDY_DATA) == 28.5
        assert get_temperature(None) is None
        assert get_temperature({}) is None
        assert get_temperature({"main": {}}) is None

