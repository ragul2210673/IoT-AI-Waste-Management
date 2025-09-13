import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# GPIO pin assignments
DIR = 27
STEP = 17
MS1 = 22
MS2 = 23
MS3 = 24

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)
GPIO.setup(MS3, GPIO.OUT)

# Enable 1/16 microstepping for higher precision
GPIO.output(MS1, GPIO.HIGH)
GPIO.output(MS2, GPIO.HIGH)
GPIO.output(MS3, GPIO.HIGH)

# Steps per full revolution in 1/16 microstepping mode
STEPS_PER_REV = 200 * 16  # = 3200

def rotate_stepper(target_angle, step_delay=0.001):
    target_angle = max(-90, min(90, target_angle))  # Clamp angle to -90° to +90°

    direction = GPIO.HIGH if target_angle >= 0 else GPIO.LOW
    GPIO.output(DIR, direction)

    # Calculate number of steps
    steps = int((abs(target_angle) / 360.0) * STEPS_PER_REV)

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(step_delay)


"""
# Example usage
rotate_stepper(90)
time.sleep(1)
rotate_stepper(0)
time.sleep(1)
rotate_stepper(-90)
time.sleep(1)
rotate_stepper(0)
time.sleep(1)
GPIO.cleanup()
"""
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# GPIO pin assignments
DIR = 27
STEP = 17
MS1 = 22
MS2 = 23
MS3 = 24

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)
GPIO.setup(MS3, GPIO.OUT)

# Enable 1/16 microstepping for higher precision
GPIO.output(MS1, GPIO.HIGH)
GPIO.output(MS2, GPIO.HIGH)
GPIO.output(MS3, GPIO.HIGH)

# Steps per full revolution in 1/16 microstepping mode
STEPS_PER_REV = 200 * 16  # = 3200

def rotate_stepper(target_angle, step_delay=0.001):
    target_angle = max(-90, min(90, target_angle))  # Clamp angle to -90° to +90°

    direction = GPIO.HIGH if target_angle >= 0 else GPIO.LOW
    GPIO.output(DIR, direction)

    # Calculate number of steps
    steps = int((abs(target_angle) / 360.0) * STEPS_PER_REV)

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(step_delay)


"""
# Example usage
rotate_stepper(90)
time.sleep(1)
rotate_stepper(0)
time.sleep(1)
rotate_stepper(-90)
time.sleep(1)
rotate_stepper(0)
time.sleep(1)
GPIO.cleanup()