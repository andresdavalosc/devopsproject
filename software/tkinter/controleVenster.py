
import tkinter as tk
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

score = 0
def on_message(client, userdata, msg):
      global score
      print(str(msg.payload))
      score += 1
      print(score)

def timer(count):
      for i in range(count, -1, -1):
           m, s = divmod(i, 60)
           h, m = divmod(m, 60)
           time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
           print(time_left)
           time.sleep(1)
           if i == 0:
                print("Game over!")
           print(str(i))
           publish.single("Software/controller/timer", payload=i, hostname="anonymous10.ddns.net")


timer(20)
client = mqtt.Client()
client.on_message = on_message
client.connect(host="anonymous10.ddns.net")
client.subscribe("Software/controller/score")
client.loop_forever()


