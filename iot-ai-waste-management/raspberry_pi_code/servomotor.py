import RPi.GPIO as GPIO
import time

SERVO_PIN = 13  
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setwarnings(False)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM frequency
servo.start(0)

def set_servo_angle_slow(start_angle, end_angle, step=1, delay=0.05):
    if start_angle < end_angle:
        angle_range = range(start_angle, end_angle + 1, step)
    else:
        angle_range = range(start_angle, end_angle - 1, -step)

    for angle in angle_range:
        duty_cycle = 2 + (angle / 18)
        servo.ChangeDutyCycle(duty_cycle)
        time.sleep(delay)

    servo.ChangeDutyCycle(0)  # Stop signal

def control_lid():
    print("Opening lid...")
    set_servo_angle_slow(0, 180, step=2, delay=0.1)  # Slowly open lid
    time.sleep(3)  # Keep it open

    print("Closing lid...")
    set_servo_angle_slow(180, 10, step=2, delay=0.1)  # Slowly close lid

"""
if __name__ == "__main__":
    control_lid()
    servo.stop()
    GPIO.cleanup()