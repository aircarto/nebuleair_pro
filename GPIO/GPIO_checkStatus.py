import RPi.GPIO as GPIO

# Set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number
gpio_pin = 24

# Set up GPIO pin as input
GPIO.setup(gpio_pin, GPIO.IN)

# Read the state of the GPIO pin
pin_state = GPIO.input(gpio_pin)

# Output the state of the GPIO pin
print(f"State of GPIO pin {gpio_pin}: {pin_state}")

# Clean up GPIO
GPIO.cleanup()
