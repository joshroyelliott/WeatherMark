import requests
import json
import logging
import os
import copy
import random

logger = logging.getLogger("weathermark.api")

# Sample weather data for ideal conditions
MOCK_GOOD_WEATHER = {
    "coord": {"lon": 153.0281, "lat": -27.4679},
    "weather": [
        {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
    ],
    "base": "stations",
    "main": {
        "temp": 23.5,  # Perfect temperature
        "feels_like": 23.7,
        "temp_min": 22.0,
        "temp_max": 25.0,
        "pressure": 1015,
        "humidity": 61,
    },
    "visibility": 10000,
    "wind": {"speed": 3.6, "deg": 140},
    "clouds": {"all": 0},
    "dt": 1622181341,
    "sys": {
        "type": 1,
        "id": 9485,
        "country": "AU",
        "sunrise": 1622149551,
        "sunset": 1622187874,
    },
    "timezone": 36000,
    "id": 2174003,
    "name": "Brisbane",
    "cod": 200,
}

# Sample weather data for bad conditions
MOCK_BAD_WEATHER = {
    "coord": {"lon": 144.9633, "lat": -37.8136},
    "weather": [
        {"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}
    ],
    "base": "stations",
    "main": {
        "temp": 12.05,  # Uncomfortably cold
        "feels_like": 11.27,
        "temp_min": 10.78,
        "temp_max": 13.56,
        "pressure": 1010,
        "humidity": 88,
    },
    "visibility": 5000,
    "wind": {"speed": 5.7, "deg": 220},
    "clouds": {"all": 90},
    "dt": 1622181341,
    "sys": {
        "type": 1,
        "id": 9548,
        "country": "AU",
        "sunrise": 1622149822,
        "sunset": 1622185707,
    },
    "timezone": 36000,
    "id": 2158177,
    "name": "Melbourne",
    "cod": 200,
}

# Sample data with only temperature problems
MOCK_TEMP_BAD = {
    "coord": {"lon": 144.9633, "lat": -37.8136},
    "weather": [
        {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
    ],
    "base": "stations",
    "main": {
        "temp": 32.5,  # Uncomfortably hot
        "feels_like": 34.8,
        "temp_min": 30.2,
        "temp_max": 33.1,
        "pressure": 1010,
        "humidity": 70,
    },
    "visibility": 10000,
    "wind": {"speed": 2.3, "deg": 180},
    "clouds": {"all": 5},
    "dt": 1622181341,
    "sys": {
        "type": 1,
        "id": 9548,
        "country": "AU",
        "sunrise": 1622149822,
        "sunset": 1622185707,
    },
    "timezone": 36000,
    "id": 2158177,
    "name": "Melbourne",
    "cod": 200,
}


def get_weather(city, api_key=None, mock_type=None):
    """
    Fetch weather data for a given city using OpenWeatherMap API

    Args:
        city: The city to get weather for
        api_key: OpenWeatherMap API key
        mock_type: Type of condition to mock ('weather', 'temperature', 'both')

    Returns:
        dict: Weather data
    """
    # Use real API if no mock specified
    if not mock_type:
        if not api_key:
            logger.error("No API key provided")
            return None

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},au&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            weather_data = response.json()
            logger.debug(
                f"API response for {city}: {json.dumps(weather_data, indent=2)}"
            )
            return weather_data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for {city}: {e}")
            return None

    # Create mock data based on city and mock type
    if city.lower() == "brisbane":
        # Brisbane always gets good data
        mock_data = copy.deepcopy(MOCK_GOOD_WEATHER)
        mock_data["name"] = city
        logger.info(f"Using MOCK good conditions for {city} (mock type: {mock_type})")
        return mock_data
    else:
        # Other cities get bad data depending on mock_type
        if mock_type == "weather":
            # Bad weather (rainy) but comfortable temperature
            mock_data = copy.deepcopy(MOCK_BAD_WEATHER)
            mock_data["main"]["temp"] = 22.0  # Set comfortable temperature
            mock_data["name"] = city
            logger.info(f"Using MOCK bad weather conditions for {city}")
            return mock_data
        elif mock_type == "temperature":
            # Good weather (sunny) but uncomfortable temperature
            mock_data = copy.deepcopy(MOCK_TEMP_BAD)
            mock_data["name"] = city

            # Randomly choose between too hot or too cold
            if random.choice([True, False]):
                # Too hot temperature (around 32-35°C)
                mock_data["main"]["temp"] = random.uniform(32.0, 35.0)
                logger.info(
                    f"Using MOCK hot temperature conditions for {city}: {mock_data['main']['temp']:.1f}°C"
                )
            else:
                # Too cold temperature (around 5-15°C)
                mock_data["main"]["temp"] = random.uniform(5.0, 15.0)
                logger.info(
                    f"Using MOCK cold temperature conditions for {city}: {mock_data['main']['temp']:.1f}°C"
                )

            return mock_data
        elif mock_type == "both":
            # Bad weather and bad temperature
            mock_data = copy.deepcopy(MOCK_BAD_WEATHER)
            mock_data["name"] = city

            # Randomly choose between too hot or too cold
            if random.choice([True, False]):
                # Too hot temperature (around 32-35°C)
                mock_data["main"]["temp"] = random.uniform(32.0, 35.0)
                logger.info(
                    f"Using MOCK bad weather and hot temperature for {city}: {mock_data['main']['temp']:.1f}°C"
                )
            else:
                # Too cold temperature (around 5-15°C)
                mock_data["main"]["temp"] = random.uniform(5.0, 15.0)
                logger.info(
                    f"Using MOCK bad weather and cold temperature for {city}: {mock_data['main']['temp']:.1f}°C"
                )

            return mock_data
        else:
            # Fallback to real API if invalid mock type
            logger.warning(f"Invalid mock type: {mock_type}, using real API")
            if not api_key:
                logger.error("No API key provided")
                return None

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},au&appid={api_key}&units=metric"

            try:
                response = requests.get(url)
                response.raise_for_status()
                weather_data = response.json()
                logger.debug(
                    f"API response for {city}: {json.dumps(weather_data, indent=2)}"
                )
                return weather_data
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching weather data for {city}: {e}")
                return None


def is_sunny(weather_data):
    """Check if weather condition is sunny"""
    if not weather_data:
        return False

    # Check if weather data has valid structure
    if "weather" not in weather_data or not weather_data["weather"]:
        return False

    # OpenWeatherMap uses weather condition codes
    # Main condition is in weather[0]['main'] and detailed in weather[0]['description']
    condition = weather_data["weather"][0]["main"].lower()
    description = weather_data["weather"][0]["description"].lower()

    # Check for sunny conditions
    return "clear" in condition or "sun" in description


def is_rainy(weather_data):
    """Check if weather condition is rainy"""
    if not weather_data:
        return False

    # Check if weather data has valid structure
    if "weather" not in weather_data or not weather_data["weather"]:
        return False

    condition = weather_data["weather"][0]["main"].lower()
    description = weather_data["weather"][0]["description"].lower()

    # Check for rainy conditions
    return "rain" in condition or "rain" in description or "shower" in description


def is_temperature_comfortable(weather_data, min_temp, max_temp):
    """
    Check if temperature is within comfortable range

    Args:
        weather_data: Weather data from API
        min_temp: Minimum comfortable temperature (Celsius)
        max_temp: Maximum comfortable temperature (Celsius)

    Returns:
        bool: True if temperature is comfortable
    """
    if (
        not weather_data
        or "main" not in weather_data
        or "temp" not in weather_data["main"]
    ):
        return False

    temp = weather_data["main"]["temp"]

    # Check if temperature is in comfortable range
    is_comfortable = min_temp <= temp <= max_temp

    if is_comfortable:
        logger.debug(
            f"Temperature {temp}°C is comfortable (between {min_temp}°C and {max_temp}°C)"
        )
    else:
        logger.debug(
            f"Temperature {temp}°C is NOT comfortable (outside {min_temp}°C - {max_temp}°C range)"
        )

    return is_comfortable


def get_temperature(weather_data):
    """Extract temperature from weather data"""
    if (
        not weather_data
        or "main" not in weather_data
        or "temp" not in weather_data["main"]
    ):
        return None

    return weather_data["main"]["temp"]

