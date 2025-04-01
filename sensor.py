import RPi.GPIO as GPIO
import time
import config  # ✅ Import stop_threads from config

# Sensor 1
TRIG_1 = 23  # Pin 16
ECHO_1 = 8   # Pin 24
MOTOR_SIG_1 = 18  # Pin 12

# Sensor 2
TRIG_2 = 24  # Pin 18
ECHO_2 = 25  # Pin 22
MOTOR_SIG_2 = 12  # Pin 32

GPIO.setmode(GPIO.BCM)

# Set up Sensor 1
GPIO.setup(TRIG_1, GPIO.OUT)
GPIO.setup(ECHO_1, GPIO.IN)
GPIO.setup(MOTOR_SIG_1, GPIO.OUT)

# Set up Sensor 2
GPIO.setup(TRIG_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)
GPIO.setup(MOTOR_SIG_2, GPIO.OUT)

# Initialize motors
motor_1 = GPIO.PWM(MOTOR_SIG_1, 100)
motor_2 = GPIO.PWM(MOTOR_SIG_2, 100)

motor_1.start(0)
motor_2.start(0)

def get_distance(trig, echo):
    """Measures distance for a given ultrasonic sensor."""
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    timeout = start_time + 0.1  
    while GPIO.input(echo) == 0:
        start_time = time.time()
        if time.time() > timeout:
            return -1  

    stop_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()
        if time.time() > timeout:
            return -1  

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  
    return round(distance, 1)

def control_motor(distance, motor):
    """Controls vibration motor based on distance."""
    if distance < 10:
        duty_cycle = 100
    elif distance < 30:
        duty_cycle = 75
    elif distance < 50:
        duty_cycle = 50
    elif distance < 70:
        duty_cycle = 25
    else:
        duty_cycle = 0

    motor.ChangeDutyCycle(duty_cycle)

def ultrasonic_detection():
    """Runs both sensors in a loop."""
    while not config.stop_threads:  
        dist_1 = get_distance(TRIG_1, ECHO_1)
        dist_2 = get_distance(TRIG_2, ECHO_2)

        control_motor(dist_1, motor_1)
        control_motor(dist_2, motor_2)

        time.sleep(0.1)
