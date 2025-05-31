import logging
import smtplib
import socket
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# For SMS, we'll use Twilio
try:
    from twilio.rest import Client as TwilioClient

    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

logger = logging.getLogger("weathermark.sender")


def send_email(message, subject, config):
    """
    Send an email with the weather message

    Args:
        message: The message content
        subject: Email subject
        config: Dictionary containing email configuration:
            - smtp_server: SMTP server address
            - smtp_port: SMTP server port
            - sender_email: Email address to send from
            - receiver_email: Email address to send to
            - password: SMTP password or app password
            - timeout: Connection timeout in seconds (optional, default: 10)

    Returns:
        bool: Success status
    """
    logger.debug("Preparing to send email")
    timeout = config.get("timeout", 10)  # Default timeout of 10 seconds

    try:
        # Create message
        email = MIMEMultipart()
        email["From"] = config["sender_email"]
        email["To"] = config["receiver_email"]
        email["Subject"] = subject

        # Attach message body
        email.attach(MIMEText(message, "plain"))

        # Debug info
        logger.debug(
            f"Connecting to SMTP server: {config['smtp_server']}:{config['smtp_port']}"
        )

        # Connect to server with timeout
        start_time = time.time()
        try:
            server = smtplib.SMTP(
                config["smtp_server"], config["smtp_port"], timeout=timeout
            )
        except (socket.timeout, socket.gaierror, ConnectionRefusedError) as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            return False

        logger.debug("SMTP connection established")

        try:
            # Set additional timeouts
            server.sock.settimeout(timeout)

            # Start TLS
            server.starttls()
            logger.debug("TLS started")

            # Login
            server.login(config["sender_email"], config["password"])
            logger.debug("Login successful")

            # Send message
            server.send_message(email)
            logger.debug("Message sent")

            # Close connection
            server.quit()

            elapsed = time.time() - start_time
            logger.info(
                f"Email sent successfully to {config['receiver_email']} in {elapsed:.2f} seconds"
            )
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check username and password.")
            server.quit()
            return False

        except socket.timeout:
            logger.error(f"SMTP operation timed out after {timeout} seconds")
            try:
                server.quit()
            except:
                pass
            return False

        except Exception as e:
            logger.error(f"SMTP error during sending: {e}")
            try:
                server.quit()
            except:
                pass
            return False

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def send_sms(message, config):
    """
    Send an SMS with the weather message using Twilio

    Args:
        message: The message content
        config: Dictionary containing SMS configuration:
            - account_sid: Twilio account SID
            - auth_token: Twilio auth token
            - from_number: Twilio phone number to send from
            - to_number: Phone number to send to

    Returns:
        bool: Success status
    """
    if not TWILIO_AVAILABLE:
        logger.error("Twilio package not installed. Install with: pip install twilio")
        return False

    logger.debug("Preparing to send SMS")

    try:
        # Initialize Twilio client
        client = TwilioClient(config["account_sid"], config["auth_token"])

        # Send message
        sms = client.messages.create(
            body=message, from_=config["from_number"], to=config["to_number"]
        )

        logger.info(f"SMS sent successfully to {config['to_number']} (SID: {sms.sid})")
        return True

    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False


def send_message(message, config):
    """
    Send message via the specified channels (email and/or SMS)

    Args:
        message: The message to send
        config: Dictionary containing configuration:
            - send_email: Boolean indicating whether to send email
            - send_sms: Boolean indicating whether to send SMS
            - email_config: Dictionary with email configuration (if send_email is True)
            - sms_config: Dictionary with SMS configuration (if send_sms is True)
            - subject: Email subject (optional, default: "Weather Update")

    Returns:
        dict: Status of each sending method
    """
    results = {}
    subject = config.get("subject", "Weather Update")

    # Send email if configured
    if config.get("send_email", False):
        if "email_config" in config:
            results["email"] = send_email(message, subject, config["email_config"])
        else:
            logger.error("Email sending enabled but no email_config provided")
            results["email"] = False

    # Send SMS if configured
    if config.get("send_sms", False):
        if "sms_config" in config:
            results["sms"] = send_sms(message, config["sms_config"])
        else:
            logger.error("SMS sending enabled but no sms_config provided")
            results["sms"] = False

    return results
