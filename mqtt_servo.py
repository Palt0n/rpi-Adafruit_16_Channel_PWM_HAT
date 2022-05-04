import time
from adafruit_servokit import ServoKit
import paho.mqtt.client as mqttClient
import time
import os
import json


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
        client.publish(MQTT_TOPIC_CAMERA, json.dumps({"move_camera_pan": SERVO_PAN_ANGLE}))
    if "camera_tilt" in data_json:
        camera_tilt_angle = data_json["camera_tilt"]
        SERVO_TILT_ANGLE = int(camera_tilt_angle)
        kit.servo[SERVO_INDEX_TILT].angle = SERVO_TILT_ANGLE
        client.publish(MQTT_TOPIC_CAMERA, json.dumps({"move_camera_tilt": SERVO_TILT_ANGLE}))
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
        client.publish(MQTT_TOPIC_CAMERA, json.dumps({"move_camera_pan": SERVO_PAN_ANGLE}))
        kit.servo[SERVO_INDEX_TILT].angle = SERVO_TILT_ANGLE
        client.publish(MQTT_TOPIC_CAMERA, json.dumps({"move_camera_tilt": SERVO_TILT_ANGLE}))
  
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
  
try:
    while True:
        time.sleep(1)
        # client.publish(MQTT_TOPIC_CAMERA, "1")
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()