import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=8)

while True:
    # kit.servo[0].angle = 0
    kit.servo[1].angle = 0
    time.sleep(5)
    # kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    time.sleep(5)
    # kit.servo[0].angle = 180
    kit.servo[1].angle = 180
    time.sleep(5)
