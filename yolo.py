import cv2
import time
import torch
import subprocess
import pyttsx3  # Text-to-Speech library
from picamera2 import Picamera2
import config  # Import stop_threads

# Load YOLOv5 model (ensure you have the YOLOv5 repo installed)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/aiguide/Documents/best.pt', force_reload=True)
model.to(torch.device('cpu'))  # Ensure it runs on CPU
torch.backends.cudnn.benchmark = False  # Disable CUDA optimizations

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Text-to-Speech setup
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Adjust speaking speed

# Parameters
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CONFIDENCE_THRESHOLD = 0.60  # Min confidence for object detection
ALERT_COOLDOWN = 3  # Seconds between alerts
last_alert_time = 0  # Store last alert time

def yolo_detection():
    global last_alert_time

    if config.stop_threads:
        return False  

    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # Perform inference
    results = model(frame)

    closest_object = None
    max_box_size = 0

    for result in results.xyxy[0]:  # Iterate through detected objects
        x1, y1, x2, y2, conf, cls = result.tolist()

        if conf < CONFIDENCE_THRESHOLD:
            continue  

        box_size = (x2 - x1) * (y2 - y1)

        # Select the largest bounding box (assumed closest object)
        if box_size > max_box_size:
            max_box_size = box_size
            closest_object = model.names[int(cls)]  # Get object name

        # Draw bounding box
        label = f"{model.names[int(cls)]} {conf:.2f}"
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Announce closest object if it meets size criteria
    if closest_object and max_box_size > 15000:
        current_time = time.time()
        if current_time - last_alert_time > ALERT_COOLDOWN:
            alert_user(closest_object)
            last_alert_time = current_time  # Update cooldown timer

    #cv2.imshow("Obstacle Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False  

    return True

def alert_user(object_name):
    """Announces the detected object using text-to-speech."""
    message = f"Warning! {object_name} detected ahead."
    print("[ALERT]:", message)

    subprocess.run(["/usr/bin/aplay", "/usr/share/sounds/alsa/Front_Center.wav"], check=True)

    tts_engine.say(message)
    tts_engine.runAndWait()
