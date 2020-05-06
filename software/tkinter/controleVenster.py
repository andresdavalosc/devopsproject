
import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

counter = 0
def on_message(client, userdata, msg):
      global counter
      print(str(msg.payload))
      counter += 1
      print(counter)

client = mqtt.Client()
client.on_message = on_message
client.connect(host="anonymous10.ddns.net")
client.subscribe("Desktop/score")
client.loop_forever()


