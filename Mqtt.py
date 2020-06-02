import paho.mqtt.client as paho
import time
import numpy as np
import matplotlib.pyplot as plt

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "Mbed"

t = np.arange(1, 21, 1)
tilt = np.zeros(20)
num = 0
# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
      global num, tilt
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
      tilt[num] = int(msg.payload)
      num += 1

def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# Publish messages from Python
while num < 20:
      mqttc.loop()
      time.sleep(1)

plt.stem(t, tilt)
plt.show()