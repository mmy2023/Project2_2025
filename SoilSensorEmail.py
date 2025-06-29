import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, time

# Configuration
MOISTURE_SENSOR_PIN = 17  # GPIO pin for moisture sensor
CHECK_TIMES = [             # Times to check moisture (24-hour format)
    time(6, 0),   # 06:00
    time(12, 0),  # 12:00
    time(18, 0),  # 18:00
    time(0, 0)    # 00:00
]
DRY_THRESHOLD = GPIO.HIGH   # High = Dry (adjust if needed)

# Email Configuration
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
QQ_EMAIL = "2573219557@qq.com"        # Your QQ email
QQ_APP_PASSWORD = "xdcencvaxdyxdiec"   # Your QQ app password
RECIPIENT = "2573219557@qq.com"        # Recipient email

# Global state variable
alert_sent = False  # Track if alert has been sent for current dry condition

def setup_gpio():
    """Initialize GPIO pins for sensor input"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)
    print("GPIO setup completed")

def read_soil_moisture():
    """Read soil moisture status from sensor"""
    return GPIO.input(MOISTURE_SENSOR_PIN)

def is_soil_dry():
    """Check if soil moisture is below threshold"""
    return read_soil_moisture() == DRY_THRESHOLD

def should_check_now():
    """Determine if current time matches any check time"""
    current_time = datetime.now().time()
    return any(t == current_time for t in CHECK_TIMES)

def send_water_alert_email():
    """Send email notification when water is needed"""
    try:
        subject = "Water Alert: Soil is Dry!"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"The soil moisture sensor detected dry conditions at {timestamp}.\n\nPlease water your plants!"
        
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = QQ_EMAIL
        msg['To'] = RECIPIENT
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(QQ_EMAIL, QQ_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email alert sent to {RECIPIENT}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def check_and_alert():
    """Check soil moisture and send alert if dry"""
    global alert_sent
    
    is_dry = is_soil_dry()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{timestamp}] Check triggered - Soil is {'DRY' if is_dry else 'WET'}")
    
    if is_dry and not alert_sent:
        print("Sending water alert email")
        alert_sent = send_water_alert_email()
    elif not is_dry:
        # Reset alert flag when soil is wet again
        alert_sent = False

def main():
    """Main monitoring loop"""
    try:
        setup_gpio()
        print("Soil Moisture Monitoring System Started")
        print(f"Check times configured: {[t.strftime('%H:%M') for t in CHECK_TIMES]}")
        
        while True:
            if should_check_now():
                check_and_alert()
            
            # Sleep for 1 minute to reduce CPU usage
            time.sleep(60)
    
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        GPIO.cleanup()
        print("GPIO resources cleaned up")

if __name__ == "__main__":
    main()