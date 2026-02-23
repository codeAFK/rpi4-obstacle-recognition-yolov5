# AIGuide: Obstacle Recognition for the Visually Impaired

AIGuide is an AI-powered assistive device developed to help visually impaired individuals detect and avoid obstacles in real time. The system uses YOLOv5 for object detection and runs on a Raspberry Pi 4, making it portable, efficient, and cost-effective.

This project was developed as an undergraduate thesis requirement for the degree Bachelor of Science in Computer Engineering (BS CpE).

## Overview

AIGuide uses computer vision and ultrasonic sensing to detect and localize obstacles in the user's environment and provides feedback through audio output and vibration alerts.

The system detects and localizes 11 obstacle classes:

- Bench
- Bicycle
- Car
- Chair
- Fire Hydrant
- Motorcycle
- Person
- Pole
- Table
- Trash Bin
- Tricycle

Localization is achieved through bounding boxes, while distance estimation is supported using an ultrasonic sensor.

## Objectives

- Design an AI-driven obstacle recognition system that uses sensory computer vision 
and machine learning algorithm to accurately detect and classify potential hazards 
in the user’s environment.
- Implement a real-time feedback mechanism that provides auditory and tactile to 
inform the user of detected obstacles, ensuring timely and effective guidance
- Evaluate the system’s accuracy and responsiveness by testing in a controlled 
environment to ensure reliable performance in diverse environments, including 
indoor and outdoor spaces.
- Ensure user safety and comfort by developing a user-friendly interface that is 
adaptable to different levels of visual impairment and integrates seamlessly with 
wearable or portable devices; and 


## Hardware Components

1. Raspberry Pi 4  
2. Raspberry Pi Camera Module 2  
3. Earphone  
4. Ultrasonic Sensor  
5. Vibration Motor  
6. Power Bank  

## Software Requirements

1. Python  
2. YOLOv5  
3. OpenCV  
4. Roboflow  
5. Pygame  

## System Architecture

1. The Pi Camera captures live video input.
2. Frames are processed using YOLOv5 for object detection.
3. Detected objects are localized using bounding boxes.
4. The ultrasonic sensor measures object distance.
5. The system provides audio alerts via earphones and vibration alerts via a vibration motor.

## Academic Context

This project was developed as an undergraduate thesis in partial fulfillment of the requirements for the degree Bachelor of Science in Computer Engineering (BSCpE).

## Authors

Espares Christan C.  
Bantayan, Rex C.  
Bucay, Gerald C.  
Jerao, Jude G. 

Bicol University Polangui  
Adviser: MELISSA JEANKIE S. RELLON, MEng 
