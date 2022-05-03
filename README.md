# rpi-Adafruit_16_Channel_PWM_HAT

Following https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/attach-and-test-the-hat

test


Creating python venv
```
sudo apt-get install python3-venv
python -m venv env
```
Create `var.env`
```
MQTT_BROKER_ADDRESS="192.168.XX.XX"
MQTT_BROKER_PORT="1883"
MQTT_BROKER_USER="XXXX"
MQTT_BROKER_PASSWORD="XXXX"
MQTT_TOPIC="XXX"
MQTT_CLIENT_NAME="XXX"
MJPEG_ADDRESS="192.168.XX.XX"
MJPEG_PORT="XXXX"
```
Edit `env/bin/activate` to load env variables
Add these lines at the bottom
```
set -o allexport
source var.env
set +o allexport
```
Activate python venv
```
source env/bin/activate
```
Libraries needed
```
sudo apt-get install python3-dev
pip install wheel
pip install adafruit-circuitpython-pca9685
pip install adafruit-circuitpython-servokit
```

Setup as service
```
cd /lib/systemd/system/
sudo nano mqtt_listen.service
```
```
[Unit]
Description=Runs the MQTT Listen Service
After=multi-user.target

[Service]
Type=simple
EnvironmentFile=/home/pi/rpi-Adafruit_16_Channel_PWM_HAT/env/bin/var.env
ExecStart=/home/pi/rpi-Adafruit_16_Channel_PWM_HAT/env/bin/python /home/pi/rpi->
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

```
sudo chmod 644 /lib/systemd/system/mqtt_listen.service
chmod +x /home/pi/rpi-Adafruit_16_Channel_PWM_HAT/mqtt_servo.py
sudo systemctl daemon-reload
sudo systemctl enable mqtt_listen.service
sudo systemctl start mqtt_listen.service
```
Service Tasks
For every change that we do on the /lib/systemd/system folder we need to execute a daemon-reload (third line of previous code). If we want to check the status of our service, you can execute:
```
sudo systemctl status mqtt_listen.service
```
In general:
Check status
```
sudo systemctl status mqtt_listen.service
```
Start service
```
sudo systemctl start mqtt_listen.service
```
Stop service
```
sudo systemctl stop mqtt_listen.service
```
Check service's log
```
sudo journalctl -f -u mqtt_listen.service
```