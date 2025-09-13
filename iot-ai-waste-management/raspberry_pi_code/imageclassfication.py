import cv2
import numpy as np
import urllib.request
import onnxruntime as ort
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

ESP32_CAM_URL = "http://192.168.4.1/capture"
model_path = "/home/KP/Batch_8/Garbage_V2.onnx"

session = ort.InferenceSession(model_path)
with open("/home/KP/Batch_8/categories1.txt", "r") as f:
    categories = [line.strip() for line in f.readlines()]

RECYCLABLE_WASTE = {"glass waste", "paper waste", "plastic waste"}
BIODEGRADABLE_WASTE = {"organic waste"}
HAZARDOUS_WASTE = {"battery waste", "metal waste", "automobile waste"}

def capture_image_from_esp32():
    try:
        resp = urllib.request.urlopen(ESP32_CAM_URL)
        image_array = np.array(bytearray(resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(image_array, -1)
        return frame
    except Exception as e:
        print("Error capturing image:", e)
        return None

def classify_image(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    pred = session.run(None, {session.get_inputs()[0].name: x})
    category_index = np.argmax(pred[0])
    waste_type = categories[category_index]
    if waste_type in RECYCLABLE_WASTE:
        cat = "Recyclable Waste"
        angle = 30
    elif waste_type in BIODEGRADABLE_WASTE:
        cat = "Biodegradable Waste"
        angle = -30
    elif waste_type in HAZARDOUS_WASTE:
        cat = "Hazardous Waste"
        angle = 0
    return waste_type, cat, angle

"""
if __name__ == "__main__":
    frame = capture_image_from_esp32()
    if frame is not None:
        waste_type, category, angle = classify_image(frame)
        print(f"Waste Type: {waste_type}\nCategory: {category}\nServo Angle: {angle}")
    else:
        print("Failed to capture image.")