# WeatherMark ☀️ 🌧️

<!--toc:start-->
- [WeatherMark ☀️ 🌧️](#weathermark-️-🌧️)
  - [🌞 Features](#🌞-features)
  - [📋 Requirements](#📋-requirements)
  - [🚀 Installation](#🚀-installation)
  - [🔑 Credentials](#🔑-credentials)
    - [Required:](#required)
    - [For Email Notifications:](#for-email-notifications)
    - [For SMS Notifications:](#for-sms-notifications)
  - [🖥️ Usage](#🖥️-usage)
  - [📱 Example Outputs](#📱-example-outputs)
    - [Weather Advantage](#weather-advantage)
    - [Temperature Advantage](#temperature-advantage)
    - [Both Weather and Temperature Advantage](#both-weather-and-temperature-advantage)
  - [🧪 Testing](#🧪-testing)
  - [🔧 Adding Custom Weather and Temperature Statements](#🔧-adding-custom-weather-and-temperature-statements)
  - [📝 License](#📝-license)
  - [🙏 Acknowledgements](#🙏-acknowledgements)
<!--toc:end-->

A lightweight Python application that compares weather conditions between cities and sends boastful notifications when your city has better weather.

<p align="center">
  <img src="https://raw.githubusercontent.com/yourusername/weathermark/main/examples/banner.png" alt="WeatherMark Banner" width="650">
</p>

## 🌞 Features

- Compares weather conditions between two cities (default: Brisbane and Melbourne)
- Detects both weather conditions (sunny vs. rainy) and temperature comfort
- Constructs engaging messages with random greetings and statements
- Includes weather and temperature emojis for visual comparison
- Sends notifications via email and/or SMS when your city has better conditions
- Configurable via TOML configuration file
- Includes mock data capability for testing

## 📋 Requirements

- Python 3.6+
- Required packages (all listed in `requirements.txt`):
  - requests
  - tomli
  - pytest (for running tests)
  - twilio (optional, for SMS functionality)

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/weathermark.git
   cd weathermark
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a virtual environment first:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Configure your settings in `config.toml`:

   ```toml
   [cities]
   our_city = "Brisbane"  # Your city
   their_city = "Melbourne"  # The comparison city

   [temperature]
   min_comfortable = 18  # Minimum comfortable temperature (Celsius)
   max_comfortable = 26  # Maximum comfortable temperature (Celsius)

   [message]
   signature = "WeatherMark"  # Signature for messages

   [email]
   enabled = true
   from = "your_email@example.com"
   to = "recipient@example.com"
   smtp_server = "smtp.gmail.com"
   smtp_port = 587

   [sms]
   enabled = false
   from_number = "+1234567890"  # Your Twilio number
   to_number = "+1234567890"    # Recipient's number
   ```

5. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api)

## 🔑 Credentials

### Required:

- OpenWeatherMap API key - Register at [OpenWeatherMap](https://openweathermap.org/api) to get your free API key

### For Email Notifications:

- Email account with SMTP access
- App password or account password

### For SMS Notifications:

- Twilio account - Sign up at [Twilio](https://www.twilio.com/)
- Twilio Account SID and Auth Token
- Twilio phone number to send from

The app securely handles these credentials through:

1. Environment variables:

   ```bash
   # Required for weather data
   export OPENWEATHER_API_KEY="your_api_key"

   # For email notifications
   export EMAIL_PASSWORD="your_email_password"

   # For SMS notifications (requires Twilio account)
   export TWILIO_ACCOUNT_SID="your_twilio_sid"
   export TWILIO_AUTH_TOKEN="your_twilio_token"
   ```

2. Or the [pass](https://www.passwordstore.org/) utility:
   - OpenWeatherMap API key: `pass show openweather/api-key`
   - Email password: `pass show smtp.example.com/your_email@example.com`
   - Twilio credentials: `pass show twilio/account-sid` and `pass show twilio/auth-token`

**Note:** For SMS functionality, you must have a Twilio account with a phone number capable of sending SMS messages. Free trial accounts will include "Sent from your Twilio trial account -" at the beginning of each message. To remove this prefix, you'll need to upgrade to a paid Twilio account.

## 🖥️ Usage

Basic usage:

```bash
python main.py
```

With mock data (for testing):

```bash
python main.py --mock weather   # Test weather conditions
python main.py --mock temperature   # Test temperature conditions
python main.py --mock both   # Test both conditions
```

Debug mode:

```bash
python main.py --debug
```

Custom configuration file:

```bash
python main.py --config custom_config.toml
```

## 📱 Example Outputs

### Weather Advantage

When your city has better weather (sunny) compared to the other city (rainy):

```
Hey there! Not a great day to be in Melbourne right now!
In Melbourne, it's currently moderate rain 🌧️ at 12°C 🥶.
Meanwhile, we're enjoying clear sky ☀️ at a comfortable 24°C 👌 here in Brisbane!

-- WeatherMark
```

### Temperature Advantage

When your city has comfortable temperature while the other city is too hot or too cold:

```
Hello! Brrr, it sure must be chilly there in Melbourne today!
In Melbourne, it's currently clear sky ☀️ at 14°C ❄️.
Meanwhile, we're enjoying clear sky ☀️ at a comfortable 23°C 👌 here in Brisbane!

-- WeatherMark
```

### Both Weather and Temperature Advantage

When your city has both better weather and more comfortable temperature:

```
G'day mate! Looks like the weather in Melbourne isn't too flash today...
Also, hope the folks in Melbourne remembered their jackets today!
In Melbourne, it's currently moderate rain 🌧️ at 10°C 🥶.
Meanwhile, we're enjoying clear sky ☀️ at a comfortable 23°C 👌 here in Brisbane!

-- WeatherMark
```

## 🧪 Testing

Run all tests:

```bash
pytest
```

Run tests for a specific module:

```bash
pytest tests/test_weather_api.py
```

Run a specific test:

```bash
pytest tests/test_message_constructor.py::TestMessageConstructor::test_construct_message_both_reasons
```

## 🔧 Adding Custom Weather and Temperature Statements

You can customize the application by adding your own weather and temperature statements in `message_constructor.py`. The app will randomly select from these statements when generating messages.

## 📝 License

[MIT License](LICENSE)

## 🙏 Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API
- [Twilio](https://www.twilio.com/) for SMS capabilities
