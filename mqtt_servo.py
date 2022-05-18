import time
from adafruit_servokit import ServoKit
import paho.mqtt.client as mqttClient
import time
import os
import json
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
RELAY_IN1_GPIO = 16
RELAY_IN2_GPIO = 19
RELAY_IN3_GPIO = 20
RELAY_IN4_GPIO = 21
GPIO.setup(RELAY_IN1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.setup(RELAY_IN2_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.setup(RELAY_IN3_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.setup(RELAY_IN4_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAY_IN1_GPIO, GPIO.LOW)
GPIO.output(RELAY_IN2_GPIO, GPIO.LOW)
GPIO.output(RELAY_IN3_GPIO, GPIO.LOW)
GPIO.output(RELAY_IN4_GPIO, GPIO.LOW)
MQTT_BROKER_ADDRESS = os.environ.get("MQTT_BROKER_ADDRESS")
MQTT_BROKER_PORT = os.environ.get("MQTT_BROKER_PORT")
MQTT_BROKER_USER = os.environ.get("MQTT_BROKER_USER")
MQTT_BROKER_PASSWORD = os.environ.get("MQTT_BROKER_PASSWORD")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC")
MQTT_CLIENT_NAME = os.environ.get("MQTT_CLIENT_NAME")
assert MQTT_BROKER_ADDRESS
assert MQTT_BROKER_PORT
assert MQTT_BROKER_USER
assert MQTT_BROKER_PASSWORD
assert MQTT_TOPIC
assert MQTT_CLIENT_NAME

MQTT_BROKER_PORT = int(MQTT_BROKER_PORT)

SERVO_INDEX_PAN = 0
SERVO_INDEX_TILT = 1

SERVO_PAN_ANGLE = 90
SERVO_TILT_ANGLE = 90
kit = ServoKit(channels=8)
def move_servo(index, angle):
    """
    Angle moves from 0 to 180
    """
    kit.servo[index].angle = 0

def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")
  
def on_message(client, userdata, message):
    data_json = json.loads(message.payload)
    move_servo(data_json)

def move_servo(data_json):
    global SERVO_PAN_ANGLE
    global SERVO_TILT_ANGLE
    if "camera_pan" in data_json:
        camera_pan_angle = data_json["camera_pan"]
        SERVO_PAN_ANGLE = int(camera_pan_angle)
        kit.servo[SERVO_INDEX_PAN].angle = SERVO_PAN_ANGLE
        client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"move_camera_pan": SERVO_PAN_ANGLE}))
    if "camera_tilt" in data_json:
        camera_tilt_angle = data_json["camera_tilt"]
        SERVO_TILT_ANGLE = int(camera_tilt_angle)
        kit.servo[SERVO_INDEX_TILT].angle = SERVO_TILT_ANGLE
        client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"move_camera_tilt": SERVO_TILT_ANGLE}))
    if "relay_1" in data_json:
        relay_1_state = data_json["relay_1"]
        if relay_1_state == 0:
            GPIO.output(RELAY_IN1_GPIO, GPIO.LOW)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_1_state": relay_1_state}))
        elif relay_1_state == 1:
            GPIO.output(RELAY_IN1_GPIO, GPIO.HIGH)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_1_state": relay_1_state}))
    if "relay_2" in data_json:
        relay_2_state = data_json["relay_2"]
        if relay_2_state == 0:
            GPIO.output(RELAY_IN2_GPIO, GPIO.LOW)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_2_state": relay_2_state}))
        elif relay_2_state == 1:
            GPIO.output(RELAY_IN2_GPIO, GPIO.HIGH)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_2_state": relay_2_state}))
    if "relay_3" in data_json:
        relay_3_state = data_json["relay_3"]
        if relay_3_state == 0:
            GPIO.output(RELAY_IN3_GPIO, GPIO.LOW)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_3_state": relay_3_state}))
        elif relay_3_state == 1:
            GPIO.output(RELAY_IN3_GPIO, GPIO.HIGH)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_3_state": relay_3_state}))
    if "relay_4" in data_json:
        relay_4_state = data_json["relay_4"]
        if relay_4_state == 0:
            GPIO.output(RELAY_IN4_GPIO, GPIO.LOW)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_4_state": relay_4_state}))
        elif relay_4_state == 1:
            GPIO.output(RELAY_IN4_GPIO, GPIO.HIGH)
            client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"relay_4_state": relay_4_state}))
    if "action" in data_json:
        action = data_json["action"]
        if action == "UP":
            SERVO_TILT_ANGLE += 1
        elif action == "DOWN":
            SERVO_TILT_ANGLE -= 1
        elif action == "LEFT":
            SERVO_PAN_ANGLE += 1
        elif action == "RIGHT":
            SERVO_PAN_ANGLE -= 1
        elif action == "MIDDLE":
            SERVO_PAN_ANGLE = 90
            SERVO_TILT_ANGLE = 90
        else:
            assert False
        if SERVO_PAN_ANGLE < 0:
            SERVO_PAN_ANGLE = 0
        if SERVO_TILT_ANGLE < 0:
            SERVO_TILT_ANGLE = 0
        if SERVO_PAN_ANGLE > 180:
            SERVO_PAN_ANGLE = 180
        if SERVO_TILT_ANGLE > 180:
            SERVO_TILT_ANGLE = 180
        kit.servo[SERVO_INDEX_PAN].angle = SERVO_PAN_ANGLE
        client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"move_camera_pan": SERVO_PAN_ANGLE}))
        kit.servo[SERVO_INDEX_TILT].angle = SERVO_TILT_ANGLE
        client.publish(MQTT_TOPIC_CAMERA_MOVE, json.dumps({"move_camera_tilt": SERVO_TILT_ANGLE}))
  
Connected = False   #global variable for the state of the connection
  
broker_address = MQTT_BROKER_ADDRESS
port = MQTT_BROKER_PORT
user = MQTT_BROKER_USER
password = MQTT_BROKER_PASSWORD

client = mqttClient.Client(MQTT_CLIENT_NAME)               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message                      #attach function to callback

client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
MQTT_TOPIC_CAMERA = MQTT_TOPIC + "/camera"
print(MQTT_TOPIC_CAMERA)
client.subscribe(MQTT_TOPIC_CAMERA)
MQTT_TOPIC_CAMERA_MOVE = MQTT_TOPIC + "/camera_move"
  
try:
    while True:
        time.sleep(1)
        # client.publish(MQTT_TOPIC_CAMERA, "1")
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()