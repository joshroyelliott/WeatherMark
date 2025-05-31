import os
import tomli
import logging
import subprocess

logger = logging.getLogger("weathermark.config")

# Default configuration
DEFAULT_CONFIG = {
    "cities": {"our_city": "Brisbane", "their_city": "Melbourne"},
    "temperature": {"min_comfortable": 18, "max_comfortable": 26},
    "message": {"signature": "WeatherMark"},
    "email": {
        "enabled": False,
        "from": "your_email@example.com",
        "to": "recipient@example.com",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "timeout": 15,
    },
    "sms": {"enabled": False, "from_number": "+1234567890", "to_number": "+1234567890"},
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    },
}


def get_credential(name, env_var, pass_path):
    """Helper function to get a credential from environment variable or pass"""
    try:
        # Try to get from environment variable
        value = os.environ.get(env_var)
        if value:
            logger.debug(f"Retrieved {name} from environment variable")
            return value

        # Try to get from pass
        result = subprocess.run(
            ["pass", "show", pass_path], capture_output=True, text=True, check=True
        )
        value = result.stdout.strip()
        if value:
            logger.debug(f"Retrieved {name} from pass")
            return value

        logger.error(f"Could not find {name} in environment or pass")
        return None
    except Exception as e:
        logger.error(f"Failed to get {name}: {e}")
        return None


def load_config(config_file="config.toml"):
    """Load configuration from TOML file with fallback to defaults"""
    config = DEFAULT_CONFIG.copy()

    # Try to load configuration from file
    try:
        if os.path.exists(config_file):
            with open(config_file, "rb") as f:
                file_config = tomli.load(f)

            # Merge file config into default config
            if file_config:
                # Merge cities
                if "cities" in file_config:
                    config["cities"].update(file_config["cities"])

                # Merge temperature settings
                if "temperature" in file_config:
                    config["temperature"].update(file_config["temperature"])

                # Merge message settings
                if "message" in file_config:
                    config["message"].update(file_config["message"])

                # Merge email settings
                if "email" in file_config:
                    config["email"].update(file_config["email"])

                # Merge SMS settings
                if "sms" in file_config:
                    config["sms"].update(file_config["sms"])

                # Merge logging settings
                if "logging" in file_config:
                    config["logging"].update(file_config["logging"])

            logger.info(f"Loaded configuration from {config_file}")
        else:
            logger.warning(
                f"Configuration file {config_file} not found, using defaults"
            )
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        logger.warning("Using default configuration")

    return config


def get_credentials(config):
    """Get all credentials for API, email and SMS services"""
    # Weather API key
    api_key = get_credential(
        "OpenWeather API key", "OPENWEATHER_API_KEY", "openweather/api-key"
    )

    # Email credentials
    if config["email"]["enabled"]:
        # Get email password using format {smtp_server}/{from_email}
        email_from = config["email"]["from"]
        smtp_server = config["email"]["smtp_server"]
        pass_path = f"{smtp_server}/{email_from}"

        config["email"]["password"] = get_credential(
            "email password", "EMAIL_PASSWORD", pass_path
        )

    # SMS credentials
    if config["sms"]["enabled"]:
        # Account SID
        config["sms"]["account_sid"] = get_credential(
            "Twilio account SID", "TWILIO_ACCOUNT_SID", "twilio/account-sid"
        )

        # Auth token
        config["sms"]["auth_token"] = get_credential(
            "Twilio auth token", "TWILIO_AUTH_TOKEN", "twilio/auth-token"
        )

    return api_key, config

