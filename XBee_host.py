import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho

mqttc = paho.Client()
host = "localhost"
topic = "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

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

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x148\r\n".encode())
char = s.read(3)
print("Set MY 0x148.")
print(char.decode())

s.write("ATDL 0x248\r\n".encode())
char = s.read(3)
print("Set DL 0x248.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

t = np.arange(1, 21, 1)
times = np.zeros(20)
# tilt = np.zeros(20)

print("start sending RPC")
s.write("\r".encode())
time.sleep(1)

for i in range(0, 20):
    # send RPC to remote
    s.write("/getStatus/run\r".encode())
    times[i] = int(s.readline().decode())
    x = float(s.readline().decode())
    y = float(s.readline().decode())
    z = float(s.readline().decode())
    if (abs(x) > 0.707 or abs(y) > 0.707):
        tilt = "1"
    else:
        tilt = "0"
    mqttc.publish(topic, tilt)
    print(tilt)
    time.sleep(1)

plt.plot(t, times)
plt.show()

s.close()

