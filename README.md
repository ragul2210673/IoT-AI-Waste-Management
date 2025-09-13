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

### Block Diagram

 
*(**Note:** You should replace this link with an actual image of your block diagram uploaded to a site like Imgur)*

## Hardware and Software Components

| Component | Function |
| :--- | :--- |
| **Raspberry Pi** | Central processing unit for running the AI model and controlling peripherals. |
| **Raspberry Pi Camera** | Captures images of waste for AI classification. |
| **RC522 RFID Reader** | Detects and identifies tagged e-waste. |
| **SG90 Servo Motor** | Physically moves flaps to sort waste into different bins. |
| **HC-SR04 Ultrasonic Sensor**| Measures the fill level of each waste bin. |
| **MQ-135 Gas Sensor** | Detects harmful gases and monitors air quality. |
| **ThingSpeak** | IoT cloud platform for data logging, visualization, and analysis. |
| **Twilio API** | Sends SMS alerts to authorities for immediate action. |
| **Python** | Primary programming language for AI model and system logic. |
| **CNN Model (TrashNet)** | Pre-trained deep learning model for image-based waste classification. |

## Expected Outcomes

*   A fully functional working prototype of the automated waste management system.
*   A 60% increase in waste processing efficiency through automated segregation.
*   A significant reduction in manual labor required for sorting.
*   An effective, real-time monitoring and alert system to prevent landfill overflow and mitigate hazardous conditions.


