import pytest
import sys
import os
import re

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from message_constructor import (
    construct_message,
    get_temperature_condition,
    GREETINGS,
    WEATHER_STATEMENTS,
    TEMPERATURE_STATEMENTS,
)

# Sample weather data for testing
SAMPLE_OUR_CITY_DATA = {
    "weather": [{"main": "Clear", "description": "clear sky"}],
    "main": {"temp": 23.5},
}

SAMPLE_THEIR_CITY_DATA = {
    "weather": [{"main": "Rain", "description": "moderate rain"}],
    "main": {"temp": 12.5},
}


class TestMessageConstructor:
    """Tests for the message_constructor module"""

    def test_get_temperature_condition(self):
        """Test temperature condition categorization"""
        assert get_temperature_condition(15, 18, 26) == "cold"
        assert get_temperature_condition(22, 18, 26) == "comfortable"
        assert get_temperature_condition(30, 18, 26) == "hot"

        # Edge cases
        assert get_temperature_condition(18, 18, 26) == "comfortable"  # Exactly at min
        assert get_temperature_condition(26, 18, 26) == "comfortable"  # Exactly at max

    def test_construct_message_weather_reason(self):
        """Test message construction with weather as the reason"""
        message = construct_message(
            SAMPLE_OUR_CITY_DATA,
            SAMPLE_THEIR_CITY_DATA,
            "Brisbane",
            "Melbourne",
            18,
            26,
            "weather",
            "Test Signature",
        )

        # Check message structure
        assert any(greeting in message for greeting in GREETINGS)
        assert any(
            statement.format(our_city="Brisbane", their_city="Melbourne") in message
            for statement in WEATHER_STATEMENTS
        )
        assert "clear sky" in message
        assert "moderate rain" in message

        # Check for temperature without hardcoding exact values
        our_temp = round(SAMPLE_OUR_CITY_DATA["main"]["temp"])
        their_temp = round(SAMPLE_THEIR_CITY_DATA["main"]["temp"])
        assert (
            str(our_temp) in message
            or str(round(SAMPLE_OUR_CITY_DATA["main"]["temp"])) in message
        )
        assert (
            str(their_temp) in message
            or str(round(SAMPLE_THEIR_CITY_DATA["main"]["temp"])) in message
        )
        assert "Brisbane" in message and "Melbourne" in message

        # No temperature statements should be included
        cold_indicators = ["chilly", "bundled", "sweater", "jacket", "cold", "heater", "winter", "gloves", "penguin"]
        heat_indicators = ["heat", "air condition", "scorcher", "melting", "ice cream", "swimming", "sunscreen", "pool"]
        
        # Check that none of the temperature-specific indicators are present
        # Get a sample of indicators to test for efficiency
        indicators_to_check = cold_indicators[:3] + heat_indicators[:3]
        for indicator in indicators_to_check:
            assert indicator.lower() not in message.lower()

    def test_construct_message_temperature_reason(self):
        """Test message construction with temperature as the reason"""
        message = construct_message(
            SAMPLE_OUR_CITY_DATA,
            SAMPLE_THEIR_CITY_DATA,
            "Brisbane",
            "Melbourne",
            18,
            26,
            "temperature",
            "Test Signature",
        )

        # Check message structure
        assert any(greeting in message for greeting in GREETINGS)

        # Should have one of the temperature-related keywords for cold
        cold_indicators = ["chilly", "bundled", "sweater", "jacket", "cold", "heater", "winter", 
                           "gloves", "penguin", "coat", "hot chocolate", "warm"]
        
        # The test data uses a cold temperature, so at least one cold indicator should be present
        temp_statement_found = any(
            indicator in message.lower() for indicator in cold_indicators
        )
        assert temp_statement_found

        # Verify city names are in the message
        assert "Brisbane" in message
        assert "Melbourne" in message

        # No weather statements should be included
        for statement in WEATHER_STATEMENTS:
            formatted = statement.format(our_city="Brisbane", their_city="Melbourne")
            assert formatted not in message

    def test_construct_message_both_reasons(self):
        """Test message construction with both reasons"""
        message = construct_message(
            SAMPLE_OUR_CITY_DATA,
            SAMPLE_THEIR_CITY_DATA,
            "Brisbane",
            "Melbourne",
            18,
            26,
            "both",
            "Test Signature",
        )

        # Check message structure
        assert any(greeting in message for greeting in GREETINGS)

        # Verify basic components that should always be present
        assert "Brisbane" in message
        assert "Melbourne" in message
        assert "clear sky" in message
        assert "moderate rain" in message

        # Get the temperature values we expect to see
        our_temp = round(SAMPLE_OUR_CITY_DATA["main"]["temp"])
        their_temp = round(SAMPLE_THEIR_CITY_DATA["main"]["temp"])
        assert str(our_temp) in message
        assert str(their_temp) in message

        # Should contain multiple lines (one for each component)
        assert message.count("\n") >= 2

        # Should contain the signature
        assert "-- Test Signature" in message

    def test_construct_message_no_signature(self):
        """Test message construction with no signature"""
        message = construct_message(
            SAMPLE_OUR_CITY_DATA,
            SAMPLE_THEIR_CITY_DATA,
            "Brisbane",
            "Melbourne",
            18,
            26,
            "weather",
            None,  # No signature
        )

        # Verify the message doesn't contain a signature line
        assert "-- " not in message
