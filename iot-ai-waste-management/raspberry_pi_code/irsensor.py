import RPi.GPIO as GPIO

# IR Sensor GPIO Pin
IR_SENSOR_PIN = 26  # Change as per your wiring

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

def detect_object():
    """Checks if waste is placed using IR sensor."""
    if GPIO.input(IR_SENSOR_PIN) == 0:
        print("Waste detected", flush=True)
        return True
    return False

"""
ch = 'y'
while ch == 'y':
    print(detect_object())  # ✅ Proper function call
    ch = input("ch= ")