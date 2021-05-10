import os
import time
import sys
import paho.mqtt.client as mqtt
import json


def SendTemperature(msg):
    try:
        host = '129.126.163.157'
        # Under Demo Device Credentials
        token = 'Za6VeCvsyi6suny9dXdE'
        sensorData = {'temperature': msg}
        client = mqtt.Client()
        # Set access token
        client.username_pw_set(token)
        # Connect to ThingsBoard using default MQTT port and 10 seconds keepalive interval
        client.connect(host, 1883, 15)
        client.loop_start()
        # Sending temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensorData), 1)
        client.loop_stop()
        client.disconnect()
        return True
    except:
        return False


def SendUltrasonicPercentage(msg):
    try:
        host = '129.126.163.157'
        # Under Demo Device Credentials
        token = 'VTI0A7mIBgS2Xl7xHemL'
        sensorData = {'ultrasonic': msg}
        client = mqtt.Client()
        # Set access token
        client.username_pw_set(token)
        # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
        client.connect(host, 1883, 15)
        client.loop_start()
        # Sending data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensorData), 1)
        client.loop_stop()
        client.disconnect()
        return True
    except:
        return False
