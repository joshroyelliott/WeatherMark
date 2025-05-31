import logging
import os
import argparse
from datetime import datetime

# Import modules
from config import load_config, get_credentials
from weather_api import (
    get_weather,
    is_sunny,
    is_rainy,
    is_temperature_comfortable,
    get_temperature,
)
from message_constructor import construct_message
from message_sender import send_message


# Parse command-line arguments
def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="WeatherMark - Compare weather between cities"
    )

    # Config file
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to configuration file (default: config.toml)",
    )

    # Mock data options
    parser.add_argument(
        "--mock",
        choices=["weather", "temperature", "both"],
        help="Type of condition to mock (weather, temperature, or both)",
    )

    # Debug mode
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_args()

    # Load configuration
    config = load_config(args.config)

    # Configure logging
    logging_level = getattr(logging, config["logging"]["level"])
    logging.basicConfig(level=logging_level, format=config["logging"]["format"])
    logger = logging.getLogger("weathermark")

    # Enable debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Get city names from config
    OUR_CITY = config["cities"]["our_city"]
    THEIR_CITY = config["cities"]["their_city"]

    # Get credentials
    api_key, config = get_credentials(config)

    # Check if we should use mock data
    use_mock = args.mock
    if use_mock:
        logger.info(f"Using mock weather data mode: {use_mock}")

    # Get weather data for both cities
    our_city_weather = get_weather(OUR_CITY, api_key, use_mock)
    their_city_weather = get_weather(THEIR_CITY, api_key, use_mock)

    # Log current weather information
    if our_city_weather:
        logger.info(
            f"{OUR_CITY}: {our_city_weather['weather'][0]['main']} - {our_city_weather['weather'][0]['description']}"
        )
    if their_city_weather:
        logger.info(
            f"{THEIR_CITY}: {their_city_weather['weather'][0]['main']} - {their_city_weather['weather'][0]['description']}"
        )

    # Compare weather conditions
    our_city_sunny = is_sunny(our_city_weather)
    their_city_rainy = is_rainy(their_city_weather)

    # Compare temperature conditions
    min_temp = config["temperature"]["min_comfortable"]
    max_temp = config["temperature"]["max_comfortable"]
    our_temp_comfortable = is_temperature_comfortable(
        our_city_weather, min_temp, max_temp
    )
    their_temp_comfortable = is_temperature_comfortable(
        their_city_weather, min_temp, max_temp
    )

    # Log temperature information
    our_temp = get_temperature(our_city_weather)
    their_temp = get_temperature(their_city_weather)
    if our_temp and their_temp:
        logger.info(
            f"Temperature - {OUR_CITY}: {our_temp}°C, {THEIR_CITY}: {their_temp}°C"
        )
        logger.info(f"Comfort range: {min_temp}°C - {max_temp}°C")
        logger.info(
            f"Temperature comfort - {OUR_CITY}: {our_temp_comfortable}, {THEIR_CITY}: {their_temp_comfortable}"
        )

    # Determine why we have better conditions
    # Only count weather as better if we have good weather (sunny) AND they have bad weather (rainy)
    weather_better = our_city_sunny and their_city_rainy

    # Only count temperature as better if our temperature is comfortable AND theirs is not
    temp_better = our_temp_comfortable and not their_temp_comfortable

    # Determine message reason
    reason = None
    if weather_better and temp_better:
        reason = "both"
        logger.info(f"Better in {OUR_CITY}! (weather and temperature)")
    elif weather_better:
        reason = "weather"
        logger.info(f"Better in {OUR_CITY}! (weather)")
    elif temp_better:
        reason = "temperature"
        logger.info(f"Better in {OUR_CITY}! (temperature)")

    # Check if our city has better conditions
    if reason:
        # Construct and display the message
        message = construct_message(
            our_city_weather,
            their_city_weather,
            OUR_CITY,
            THEIR_CITY,
            min_temp,
            max_temp,
            reason,
            config["message"]["signature"],
        )
        logger.info(message)

        # Send the message via configured channels
        if config["email"]["enabled"] or config["sms"]["enabled"]:
            # Prepare sender configuration
            sender_config = {
                "send_email": config["email"]["enabled"],
                "send_sms": config["sms"]["enabled"],
                "subject": f"Weather Update: Better in {OUR_CITY}!",
            }

            # Add channel-specific configs if enabled
            if config["email"]["enabled"]:
                # Skip email if no password available
                if not config["email"].get("password"):
                    logger.warning("No email password available - skipping email")
                    sender_config["send_email"] = False
                else:
                    sender_config["email_config"] = config["email"]

            if config["sms"]["enabled"]:
                # Skip SMS if credentials are missing
                if not config["sms"].get("account_sid") or not config["sms"].get(
                    "auth_token"
                ):
                    logger.warning("Missing Twilio credentials - skipping SMS")
                    sender_config["send_sms"] = False
                else:
                    sender_config["sms_config"] = config["sms"]

            # Only attempt to send if at least one channel is enabled
            if sender_config.get("send_email", False) or sender_config.get(
                "send_sms", False
            ):
                logger.info("Sending message...")
                send_results = send_message(message, sender_config)

                # Log the results
                for channel, success in send_results.items():
                    if success:
                        logger.info(f"Message sent successfully via {channel}")
                    else:
                        logger.error(f"Failed to send message via {channel}")
            else:
                logger.warning(
                    "No messaging channels enabled or all were skipped due to missing credentials"
                )
    else:
        conditions = []

        # Weather conditions
        if our_city_sunny:
            conditions.append(f"{OUR_CITY} is sunny")
        else:
            conditions.append(f"{OUR_CITY} is not sunny")
        if their_city_rainy:
            conditions.append(f"{THEIR_CITY} is rainy")
        else:
            conditions.append(f"{THEIR_CITY} is not rainy")

        # Temperature conditions
        if our_temp_comfortable:
            conditions.append(f"{OUR_CITY} temperature is comfortable")
        else:
            conditions.append(f"{OUR_CITY} temperature is not comfortable")
        if not their_temp_comfortable:
            conditions.append(f"{THEIR_CITY} temperature is not comfortable")
        else:
            conditions.append(f"{THEIR_CITY} temperature is comfortable")

        logger.info(f"No advantage for {OUR_CITY} detected")
        logger.info(f"Conditions: {', '.join(conditions)}")


if __name__ == "__main__":
    main()
