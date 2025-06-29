import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
MOISTURE_SENSOR_PIN = 17  # GPIO pin for moisture sensor
CHECK_INTERVAL = 60       # Check interval in seconds
DRY_THRESHOLD = GPIO.HIGH # High = Dry (adjust if needed)

# Email Configuration (Replace with your credentials)
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
QQ_EMAIL = "2573219557@qq.com"        # Your QQ email
QQ_APP_PASSWORD = "xdcencvaxdyxdiec"   # Your QQ app password
RECIPIENT = "2573219557@qq.com"        # Recipient email

# Global state variable
last_moisture_state = None  # None, 'wet', or 'dry'

def setup_gpio():
    """Initialize GPIO pins for sensor input"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)
    print("GPIO setup completed")

def read_soil_moisture():
    """Read soil moisture status from sensor"""
    return GPIO.input(MOISTURE_SENSOR_PIN)

def get_moisture_state():
    """Convert sensor reading to 'wet' or 'dry' state"""
    return 'dry' if read_soil_moisture() == DRY_THRESHOLD else 'wet'

def send_water_alert_email():
    """Send email notification when water is needed"""
    try:
        subject = "Water Alert: Soil is Dry!"
        body = f"The soil moisture sensor detected dry conditions at {datetime.now()}.\n\nPlease water your plants!"
        
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

def main():
    """Main monitoring loop"""
    global last_moisture_state
    
    try:
        setup_gpio()
        print("Soil Moisture Monitoring System Started")
        last_moisture_state = get_moisture_state()
        print(f"Initial state: {last_moisture_state}")
        
        while True:
            current_state = get_moisture_state()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check for state transition from wet to dry
            if last_moisture_state == 'wet' and current_state == 'dry':
                print(f"[{timestamp}] State changed: WET → DRY - Sending alert email")
                send_water_alert_email()
            
            # Update last state
            last_moisture_state = current_state
            
            # Log current status
            print(f"[{timestamp}] Current state: {current_state}")
            
            # Wait for next check
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        GPIO.cleanup()
        print("GPIO resources cleaned up")

if __name__ == "__main__":
    main()