import time
import cv2
import IR_sensor
import stepper_motor
import RPi.GPIO as GPIO
import servo_control
GPIO.setwarnings(False)  # Corrected

from Image_classification import classify_image, capture_image_from_esp32

def process_waste():
    frame = capture_image_from_esp32()
    if frame is not None:
        return classify_image(frame)
    else:
        print("Failed to capture image from ESP32-CAM.", flush=True)
        return None, None, 0



def main():
    while True:
        if IR_sensor.detect_object():
            waste_name, waste_category, angle = process_waste()
            if waste_name and waste_category:
                print(f"Detected Waste: {waste_name} | Category: {waste_category} | Angle: {angle}", flush= True)
            if angle != 0:
                print(f"Rotating stepper to {angle} degrees...", flush=True)
                stepper_motor.rotate_stepper(angle)
                time.sleep(1)
                print("Controlling lid...", flush=True)
                servo_control.control_lid()
                stepper_motor.rotate_stepper(-angle)  # Return to home
                time.sleep(1)
            else:
                print("Controlling lid...", flush=True)
                servo_control.control_lid()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()