# Automated Waste Management and Hazard Monitoring Using IoT and AI

## Overview

This project presents an intelligent, automated system for waste segregation and hazard monitoring designed to tackle critical inefficiencies in urban waste management. By integrating the Internet of Things (IoT) and Artificial Intelligence (AI), our solution provides a robust framework for classifying waste, monitoring landfill levels, detecting hazardous conditions, and automating the entire sorting process.

The system aims to reduce landfill burden, minimize environmental pollution, and increase the efficiency of recycling processes, aligning with national initiatives like the Smart Cities Mission and Swachh Bharat Abhiyan.

## Problem Statement

India generates over 62 million tons of solid waste annually, with a significant portion remaining uncollected or improperly managed. This leads to several critical issues:
*   **Overflowing Landfills:** Major landfill sites are exceeding their capacity, posing severe environmental and health risks.
*   **Inefficient Segregation:** Manual waste sorting is labor-intensive, slow, and often inaccurate, with only 30% of recyclable waste being processed.
*   **Hazardous Conditions:** Unmonitored waste accumulation leads to the release of toxic gases (like methane and ammonia) and contributes to significant air and soil pollution.

Our project directly addresses these challenges by creating a smart, automated solution that handles waste classification and monitoring from end to end.

## Features

*   **AI-Powered Waste Classification:** Utilizes a Convolutional Neural Network (CNN) model, trained on the TrashNet dataset, to automatically classify waste into categories such as Biodegradable, Recyclable, Hazardous, and E-Waste.
*   **Automated Physical Sorting:** Employs servo motors to physically direct classified items into their respective bins, reducing human effort by an estimated 70%.
*   **Real-Time Fill-Level Monitoring:** An HC-SR04 ultrasonic sensor constantly measures the waste level in each bin to prevent overflow.
*   **Hazardous Gas Detection:** An MQ-135 gas sensor monitors the air for harmful gases like ammonia, CO₂, and methane, ensuring safety at disposal sites.
*   **Smart IoT Alerts:** The system is connected to the ThingSpeak cloud platform to log sensor data. When a bin is full or hazardous gases are detected, real-time alerts are automatically sent to authorities via the Twilio API.
*   **E-Waste Detection:** An RC522 RFID reader identifies and segregates electronic waste, which requires special handling.

## System Architecture

The system operates through a sequential, three-stage process:

1.  **Waste Input and Detection:**
    *   Waste is placed into the system.
    *   An RFID reader first checks for an e-waste tag. If detected, the item is immediately sorted into the e-waste bin.
    *   If no RFID tag is found, a Raspberry Pi Camera captures an image of the item.

2.  **AI Classification and Segregation:**
    *   The captured image is processed by the CNN model, which classifies the waste.
    *   Based on the classification label, commands are sent to SG90 servo motors, which guide the waste into the correct bin (Biodegradable, Recyclable, or Hazardous).

3.  **Monitoring and Cloud Alerts:**
    *   Ultrasonic and gas sensors continuously collect data on bin levels and air quality.
    *   This data is periodically uploaded to the ThingSpeak IoT platform for logging and analysis.
    *   If predefined thresholds are crossed (e.g., bin 90% full, gas level unsafe), the system triggers an alert to the relevant authorities via Twilio.

## Hardware and Software Components

| Component | Function |
| :--- | :--- |
| **Raspberry Pi** | Central processing unit for running the AI model and controlling peripherals. |
| **Raspberry Pi Camera**| Captures images of waste for AI classification. |
| **RC522 RFID Reader** | Detects and identifies tagged e-waste. |
| **SG90 Servo Motor** | Physically moves flaps to sort waste into different bins. |
| **HC-SR04 Ultrasonic Sensor**| Measures the fill level of each waste bin. |
| **MQ-135 Gas Sensor** | Detects harmful gases and monitors air quality. |
| **ThingSpeak** | IoT cloud platform for data logging, visualization, and analysis. |
| **Twilio API** | Sends SMS alerts to authorities for immediate action. |
| **Python** | Primary programming language for AI model and system logic. |
| **CNN Model (TrashNet)**| Pre-trained deep learning model for image-based waste classification. |

---

## Code and Functionality

The project is divided into two main components: the Raspberry Pi for AI processing and control, and the ESP32 for real-time monitoring.

### Raspberry Pi (`raspberry_pi_code/`)

This is the central brain of the operation, handling image processing and mechanical control.

*   **`main.py`**: The main script that orchestrates the entire process. It waits for a signal from the IR sensor, initiates image capture and classification, and controls the motors.
*   **`image_classification.py`**:
    *   `capture_image_from_esp32()`: Fetches a live image from the ESP32-CAM's web server.
    *   `classify_image()`: Preprocesses the captured image and feeds it into the pre-trained ONNX model. It returns the detected waste type, its broader category, and the corresponding angle for the stepper motor.
*   **`stepper_motor.py`**:
    *   `rotate_stepper(target_angle)`: Controls the stepper motor, rotating the sorting mechanism to the precise angle required to position the waste over the correct bin. It handles both direction and step counting.
*   **`servo_control.py`**:
    *   `control_lid()`: Manages the servo motor that opens and closes the flap, dropping the sorted waste into the bin below.
*   **`ir_sensor.py`**:
    *   `detect_object()`: A simple function that returns `True` when an object breaks the IR beam, signaling that a waste item has been placed and is ready for processing.

### ESP32 (`esp32_code/`)

This microcontroller works independently to handle real-time bin monitoring and alerts.

*   **`bin_monitor_esp32.ino`**:
    *   `setup()`: Initializes Wi-Fi connection, serial communication, and configures the GPIO pins for the four ultrasonic sensors[74].
    *   `loop()`: The main operational loop that runs continuously.
        *   It calls `readDistance()` for each of the four ultrasonic sensors to measure the fill level of each bin[77].
        *   It checks if any bin's distance is less than the `FULL_DISTANCE` threshold.
        *   If any bin is full, it compiles a list of the full bins and calls `sendAlert()`.
    *   `readDistance()`: A utility function that triggers an ultrasonic sensor and calculates the distance in centimeters based on the echo time[78].
    *   `sendAlert()`: Configures and sends an email using the `ESP_Mail_Client` library. The email contains the list of full bins, notifying maintenance staff automatically.

---

## How to Set Up and Run the Project

1.  **Hardware Setup:**
    *   Connect the camera, IR sensor, stepper motor, and servo motor to the Raspberry Pi according to the GPIO pin definitions in the Python scripts.
    *   Connect the four ultrasonic sensors to the ESP32 as defined in the `.ino` file.
    *   Power both the Raspberry Pi and the ESP32.

2.  **Software on Raspberry Pi:**
    *   Ensure Python and all necessary libraries (`opencv-python`, `numpy`, `onnxruntime`, `tensorflow`, `RPi.GPIO`) are installed.
    *   Place all the Python scripts in the `raspberry_pi_code` folder.
    *   Make sure the ONNX model (`Garbage_V2.onnx`) and categories file (`categories1.txt`) are in the correct path as specified in `image_classification.py`.
    *   Run the main program: `python main.py`

3.  **Software on ESP32:**
    *   Open `bin_monitor_esp32.ino` in the Arduino IDE.
    *   Install the `ESP_Mail_Client` library via the Library Manager.
    *   Fill in your Wi-Fi `ssid` and `password`.
    *   Update the `SENDER_EMAIL`, `SENDER_PASSWORD`, and `RECIPIENT_EMAIL` with your own credentials. **Important:** You will need to generate an "App Password" for your Gmail account to use for `SENDER_PASSWORD`.
    *   Upload the code to your ESP32 board.
    *   Open the Serial Monitor to view real-time distance readings and alert statuses.
