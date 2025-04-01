import threading
import RPi.GPIO as GPIO
import time
import cv2
import subprocess
import pyttsx3
import config as config  # ✅ Import stop_threads from config
from yolo import yolo_detection
from sensor import ultrasonic_detection

def announce_startup():
    tts_engine = pyttsx3.init()
    tts_engine.say("Startup sequence initiated. Please stand by.")
    subprocess.run(["/usr/bin/aplay", "/usr/share/sounds/alsa/Front_Center.wav"], check=True)
    tts_engine.runAndWait()

announce_startup()

def run_yolo_detection():
    while not config.stop_threads:  # ✅ Use config.stop_threads
        if not yolo_detection():
            break

def run_ultrasonic_detection():
    while not config.stop_threads:
        ultrasonic_detection()

def main():
    yolo_thread = threading.Thread(target=run_yolo_detection)
    ultrasonic_thread = threading.Thread(target=run_ultrasonic_detection)

    yolo_thread.start()
    ultrasonic_thread.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        print("Exiting...")
        config.stop_threads = True  # ✅ Stop all threads

        yolo_thread.join()
        ultrasonic_thread.join()

        cv2.destroyAllWindows()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
