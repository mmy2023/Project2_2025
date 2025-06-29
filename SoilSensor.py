import RPi.GPIO as GPIO
import time

# Configuration
SENSOR_PIN = 17  # GPIO pin connected to sensor's digital output

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
            print("No Water Detected")
        else:
            print("Water Detected")
        time.sleep(1)  # Update every second
except KeyboardInterrupt:
    GPIO.cleanup()