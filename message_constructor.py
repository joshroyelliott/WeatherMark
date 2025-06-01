import logging
import random

logger = logging.getLogger("weathermark.message")

# List of email subject lines
SUBJECT_LINES = [
    "Better weather in {our_city} today!",
    "Weather update: {our_city} vs {their_city}",
    "Weather comparison: We win in {our_city}!",
    "Lucky us! {our_city}'s weather beats {their_city}",
    "Weather alert: {our_city} has the advantage today",
    "Weather report: {our_city} comes out on top",
    "Sunshine in {our_city}, while {their_city}...",
    "Weather bragging rights for {our_city}!",
    "{our_city} weather FTW!",
    "Why {our_city} has the better forecast today",
    "Perfect conditions in {our_city} compared to {their_city}",
    "You'd rather be in {our_city} today!",
    "The forecast favors {our_city} today",
    "{our_city} vs {their_city}: Weather showdown",
    "Winning at weather in {our_city} today!",
]

# List of greeting messages
GREETINGS = [
    "Hey there!",
    "How's it going?",
    "G'day mate!",
    "Hello!",
    "Hi there!",
    "Good day to you!",
    "Howdy!",
    "Hey, what's up?",
    "Greetings!",
    "Hey, hope you're well!",
    "Kia Ora!",
    "Hey hey!",
    "Ahoy there!",
    "Top of the day to you!",
    "What a day!",
    "Oh hello!",
    "Well, well, well...",
    "Just checking in!",
    "Lovely day, isn't it?",
    "Weather alert!",
    "Weather update for you!",
    "Special weather bulletin:",
    "Breaking weather news:",
    "Attention weather enthusiasts!",
    "Guess what?",
    "You'll be pleased to know...",
    "Just wanted to share...",
    "Quick update for you:",
]

# List of statements about weather comparison
WEATHER_STATEMENTS = [
    "Looks like the weather in {their_city} isn't too flash today...",
    "Not a great day to be in {their_city} right now!",
    "I'd rather be here than in {their_city} today!",
    "The weather down in {their_city} is looking pretty grim!",
    "You might want to avoid {their_city} today!",
    "Feeling lucky to be in {our_city} and not {their_city} today!",
    "Guess who's got better weather than {their_city} today?",
    "Definitely a better day to be in {our_city} than {their_city}!",
    "If you're in {their_city}, you might want to grab an umbrella!",
    "Weather-wise, {our_city} is the place to be today, not {their_city}!",
    "While {their_city} deals with rain, we're basking in sunshine in {our_city}!",
    "Bad luck if you're in {their_city} today - the weather's not cooperating!",
    "Seems like Mother Nature is favoring {our_city} over {their_city} today!",
    "The forecast for {their_city} isn't looking great, unlike here in {our_city}!",
    "I'm glad I'm not in {their_city} with that weather!",
    "The sun is shining here, but {their_city} is getting soaked!",
    "While we enjoy the beautiful weather here, {their_city} is dealing with rain!",
    "Those clouds over {their_city} look pretty menacing from sunny {our_city}!",
    "Looks like {our_city} won the weather lottery compared to {their_city} today!",
    "If you had plans in {their_city} today, you might want to reschedule!",
    "Sending some sunshine from {our_city} to rainy {their_city}!",
    "The skies are much friendlier here in {our_city} than in {their_city}!",
    "Perfect day for outdoor activities in {our_city}, unlike in {their_city}!",
    "Why did the weather decide to be so nice here but not in {their_city}?",
    "Seems like all the good weather headed to {our_city} instead of {their_city}!",
]

# List of statements about temperature comparison
TEMPERATURE_STATEMENTS = [
    # Cold weather statements
    "Brrr, it sure must be chilly in {their_city} today!",
    "I hear they're all bundled up in {their_city} right now!",
    "Might want to pack a sweater if you're heading to {their_city}!",
    "Hope the folks in {their_city} remembered their jackets today!",
    "I bet they're cranking up the heaters in {their_city} right now!",
    "The cafes in {their_city} must be selling a lot of hot chocolate today!",
    "Looks like {their_city} is getting a taste of winter today!",
    "I'd be wearing my warmest coat if I were in {their_city} right now!",
    "Better bring some gloves if you're heading to {their_city}!",
    "I've heard it's so cold in {their_city} that people are seeing their breath!",
    "The temperature in {their_city} would make a penguin shiver!",
    "Those in {their_city} must be dreaming of a warm beach right now!",
    # Hot weather statements
    "Whew! How about that heat wave in {their_city}!",
    "I bet the air conditioners are working overtime in {their_city} today!",
    "Looks like {their_city} is having a scorcher today!",
    "I wouldn't want to be without air conditioning in {their_city} right now!",
    "Ice cream sales must be through the roof in {their_city} today!",
    "They're probably melting in {their_city} with those temperatures!",
    "I heard you could fry an egg on the sidewalk in {their_city} today!",
    "The swimming pools in {their_city} must be packed right now!",
    "Those in {their_city} are probably dreaming of a cool change!",
    "I bet everyone in {their_city} wishes they had a pool today!",
    "Sunscreen and cold drinks are essential in {their_city} today!",
    "The heat in {their_city} would make a lizard look for shade!",
    # General temperature statements
    "The temperature in {their_city} is way outside the comfort zone today!",
    "Perfect weather here in {our_city}, but not so much in {their_city}!",
    "I'll take our comfortable {our_city} weather over {their_city}'s any day!",
    "If you're in {their_city}, you might want to adjust your thermostat!",
    "Probably not the best day for outdoor activities in {their_city}!",
    "The folks in {their_city} are probably wishing they were here in {our_city} today!",
    "Temperature-wise, we definitely got the better deal here in {our_city}!",
    "I'm grateful for our perfect temperature here in {our_city} today!",
    "The thermometer readings in {their_city} are not looking ideal today!",
    "We've got the Goldilocks temperature here - not too hot, not too cold!",
    "Our temperature is just right, unlike the extreme in {their_city}!",
    "While we enjoy ideal temperatures, {their_city} is at the other end of the spectrum!",
]


def get_temperature_condition(temp, min_comfortable, max_comfortable):
    """Determine if temperature is too hot, too cold, or just right"""
    if temp < min_comfortable:
        return "cold"
    elif temp > max_comfortable:
        return "hot"
    else:
        return "comfortable"


def get_weather_emoji(weather_description):
    """Return an appropriate emoji based on the weather description"""
    weather_description = weather_description.lower()

    if "clear" in weather_description or "sunny" in weather_description:
        return "☀️"
    elif "cloud" in weather_description and "few" in weather_description:
        return "🌤️"
    elif "cloud" in weather_description and "scattered" in weather_description:
        return "⛅"
    elif "cloud" in weather_description:
        return "☁️"
    elif "rain" in weather_description and "light" in weather_description:
        return "🌦️"
    elif "rain" in weather_description and "heavy" in weather_description:
        return "🌧️"
    elif "rain" in weather_description:
        return "🌧️"
    elif "thunder" in weather_description or "storm" in weather_description:
        return "⛈️"
    elif "snow" in weather_description:
        return "❄️"
    elif "mist" in weather_description or "fog" in weather_description:
        return "🌫️"
    else:
        return "🌡️"  # Default to thermometer if no match


def get_temperature_emoji(
    temp, min_comfortable, max_comfortable, show_comfortable=True
):
    """
    Return an appropriate emoji based on the temperature

    Args:
        temp: The temperature to check
        min_comfortable: Minimum comfortable temperature
        max_comfortable: Maximum comfortable temperature
        show_comfortable: Whether to show the "just right" emoji for comfortable temperatures
    """
    if temp < min_comfortable - 5:
        return "🥶"  # Very cold
    elif temp < min_comfortable:
        return "❄️"  # Cold
    elif min_comfortable <= temp <= max_comfortable:
        return (
            "👌" if show_comfortable else ""
        )  # Just right (or nothing if we don't want to show it)
    elif temp > max_comfortable + 5:
        return "🔥"  # Very hot
    elif temp > max_comfortable:
        return "🥵"  # Hot
    else:
        return ""  # No emoji


def construct_message(
    our_city_data,
    their_city_data,
    our_city="Brisbane",
    their_city="Melbourne",
    min_comfortable=18,
    max_comfortable=26,
    reason="weather",
    signature="WeatherMark",
):
    """
    Construct a message based on weather data when our city has better weather

    Args:
        our_city_data: Weather data for our city
        their_city_data: Weather data for their city
        our_city: Name of our city
        their_city: Name of their city
        min_comfortable: Minimum comfortable temperature (Celsius)
        max_comfortable: Maximum comfortable temperature (Celsius)
        reason: The reason for the better conditions ("weather", "temperature", or "both")
        signature: Signature to include at the end of the message

    Returns:
        tuple: (message, subject) where message is the formatted message and 
               subject is a dynamic subject line for email
    """
    logger.debug(f"Constructing message with {reason} data")

    # Get weather descriptions
    our_weather = our_city_data["weather"][0]["description"]
    their_weather = their_city_data["weather"][0]["description"]

    # Get temperatures
    our_temp = round(our_city_data["main"]["temp"])
    their_temp = round(their_city_data["main"]["temp"])

    # Determine temperature conditions
    their_temp_condition = get_temperature_condition(
        their_temp, min_comfortable, max_comfortable
    )

    # Select random greeting
    greeting = random.choice(GREETINGS)

    # Determine which type of statement to use based on the reason
    if reason == "weather" or reason == "both":
        weather_statement = random.choice(WEATHER_STATEMENTS).format(
            our_city=our_city, their_city=their_city
        )
    else:
        weather_statement = ""

    if reason == "temperature" or reason == "both":
        # Select appropriate temperature statements based on condition
        temp_statements = []
        if their_temp_condition == "cold":
            # Use the cold-related statements (first 12)
            temp_statements = TEMPERATURE_STATEMENTS[:12]
        elif their_temp_condition == "hot":
            # Use the hot-related statements (next 12)
            temp_statements = TEMPERATURE_STATEMENTS[12:24]
        else:
            # This shouldn't happen in the "temperature" reason case,
            # but just in case, use the generic statements
            temp_statements = TEMPERATURE_STATEMENTS[24:]

        temp_statement = random.choice(temp_statements).format(
            our_city=our_city, their_city=their_city
        )
    else:
        temp_statement = ""

    # Construct the message
    message = f"{greeting} "

    if weather_statement and temp_statement:
        # If we have both, use them together with a transition
        # Remove "Melbourne" from the temperature statement if it's already in the weather statement
        # to avoid repetition
        if their_city in weather_statement and their_city in temp_statement:
            # Replace city name with "there" or "they" in temperature statement
            temp_statement = temp_statement.replace(f"in {their_city}", "there")
            temp_statement = temp_statement.replace(f"{their_city}'s", "their")

            # Add a transition word and make sure it flows well
            if temp_statement[0].isupper():
                temp_statement = (
                    "Also, " + temp_statement[0].lower() + temp_statement[1:]
                )
            else:
                temp_statement = "Also, " + temp_statement

        message += f"{weather_statement}\n{temp_statement}\n"
    elif weather_statement:
        # Just weather
        message += f"{weather_statement}\n"
    elif temp_statement:
        # Just temperature
        message += f"{temp_statement}\n"

    # Get appropriate weather emojis
    our_emoji = get_weather_emoji(our_weather)
    their_emoji = get_weather_emoji(their_weather)

    # Get temperature emojis - don't show "just right" emoji for their city
    our_temp_emoji = get_temperature_emoji(
        our_temp, min_comfortable, max_comfortable, show_comfortable=True
    )
    their_temp_emoji = get_temperature_emoji(
        their_temp, min_comfortable, max_comfortable, show_comfortable=False
    )

    # Add specific conditions with emojis
    if reason == "temperature":
        # For temperature-only messages, focus on temperature and don't mention weather conditions
        message += f"In {their_city}, it's currently {their_temp}°C {their_temp_emoji}.\n"
        
        if min_comfortable <= our_temp <= max_comfortable:
            message += f"Meanwhile, it's a comfortable {our_temp}°C {our_temp_emoji} here in {our_city}!"
        else:
            message += f"Meanwhile, it's {our_temp}°C {our_temp_emoji} here in {our_city}!"
    else:
        # For weather and both reasons, include both weather and temperature
        message += f"In {their_city}, it's currently {their_weather} {their_emoji} at {their_temp}°C {their_temp_emoji}.\n"
        
        if min_comfortable <= our_temp <= max_comfortable:
            message += f"Meanwhile, we're enjoying {our_weather} {our_emoji} at a comfortable {our_temp}°C {our_temp_emoji} here in {our_city}!"
        else:
            message += f"Meanwhile, we're enjoying {our_weather} {our_emoji} at {our_temp}°C {our_temp_emoji} here in {our_city}!"

    # Add signature if provided
    if signature:
        message += f"\n\n-- {signature}"
    
    # Generate a random subject line appropriate for the reason
    if reason == "temperature":
        # Filter for temperature-appropriate subject lines
        temp_subjects = [
            subj for subj in SUBJECT_LINES 
            if not any(w in subj.lower() for w in ["weather", "sunshine", "forecast"])
        ]
        subject = random.choice(temp_subjects or SUBJECT_LINES).format(
            our_city=our_city, their_city=their_city
        )
    else:
        # Use any subject line for weather or both reasons
        subject = random.choice(SUBJECT_LINES).format(
            our_city=our_city, their_city=their_city
        )

    return message, subject
