import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from message_constructor import get_weather_emoji, get_temperature_emoji


class TestEmoji:
    """Tests for emoji functionality in the message_constructor module"""

    def test_weather_emoji(self):
        """Test weather emoji mapping"""
        # Test clear/sunny conditions
        assert get_weather_emoji("clear sky") == "☀️"
        assert get_weather_emoji("sunny") == "☀️"

        # Test cloudy conditions
        assert get_weather_emoji("few clouds") == "🌤️"
        assert get_weather_emoji("scattered clouds") == "⛅"
        assert get_weather_emoji("broken clouds") == "☁️"
        assert get_weather_emoji("overcast clouds") == "☁️"

        # Test rainy conditions
        assert get_weather_emoji("light rain") == "🌦️"
        assert get_weather_emoji("moderate rain") == "🌧️"
        assert get_weather_emoji("heavy rain") == "🌧️"

        # Test other conditions
        assert get_weather_emoji("thunderstorm") == "⛈️"
        assert get_weather_emoji("snow") == "❄️"
        assert get_weather_emoji("mist") == "🌫️"
        assert get_weather_emoji("fog") == "🌫️"

        # Test fallback
        assert get_weather_emoji("unknown weather") == "🌡️"

    def test_temperature_emoji(self):
        """Test temperature emoji mapping"""
        # Test with show_comfortable=True (our city)
        assert (
            get_temperature_emoji(14, 18, 26, True) == "❄️"
        )  # Cold (above very cold threshold)
        assert (
            get_temperature_emoji(10, 18, 26, True) == "🥶"
        )  # Very cold (more than 5 below min)
        assert get_temperature_emoji(22, 18, 26, True) == "👌"  # Just right
        assert (
            get_temperature_emoji(29, 18, 26, True) == "🥵"
        )  # Hot (below very hot threshold)
        assert (
            get_temperature_emoji(35, 18, 26, True) == "🔥"
        )  # Very hot (more than 5 above max)

        # Test with show_comfortable=False (their city)
        assert (
            get_temperature_emoji(14, 18, 26, False) == "❄️"
        )  # Cold (above very cold threshold)
        assert (
            get_temperature_emoji(10, 18, 26, False) == "🥶"
        )  # Very cold (more than 5 below min)
        assert get_temperature_emoji(22, 18, 26, False) == ""  # Just right (no emoji)
        assert (
            get_temperature_emoji(29, 18, 26, False) == "🥵"
        )  # Hot (below very hot threshold)
        assert (
            get_temperature_emoji(35, 18, 26, False) == "🔥"
        )  # Very hot (more than 5 above max)

    def test_emoji_edge_cases(self):
        """Test edge cases for emoji functions"""
        # Test at boundaries
        assert get_temperature_emoji(18, 18, 26, True) == "👌"  # Exactly at min
        assert get_temperature_emoji(26, 18, 26, True) == "👌"  # Exactly at max

        # Test empty input for weather emoji
        assert get_weather_emoji("") == "🌡️"

        # Test case insensitivity
        assert get_weather_emoji("CLEAR SKY") == "☀️"
        assert get_weather_emoji("Light Rain") == "🌦️"

