#!/usr/bin/python3/
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import os
import paho.mqtt.publish as publish
import sys
from time import sleep

led = [10,9,11,5,6,13,19]
virus = 22
wcrol = 27
kar  = 17
prevcount = 0
count = 1
start = False
begin = True
knop1,knop2=3,2
GPIO.setmode(GPIO.BCM)
GPIO.setup(knop1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(knop2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
for x in led:
    GPIO.setup(x,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(virus,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(wcrol,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(kar,GPIO.OUT,initial=GPIO.LOW)

#def on_connect(client, userdata, flags, rc):
#    client.subscribe("Desktop/project")


def Up(a):
    if GPIO.event_detected(knop1):
        global begin,count
        if begin == True:
            begin = False
            publish.single("Hardware/console",payload= "start"+str(count), hostname="anonymous10.ddns.net")
            sleep(3)
            publish.single("Hardware/console/bediening",payload= count, hostname="anonymous10.ddns.net")
        elif start == True:
            print("Up")
            publish.single("Hardware/console/bediening",payload= repr(count) + "UP", hostname="anonymous10.ddns.net")
        sleep(1)
        
def Dn(a):
    if GPIO.event_detected(knop2):
        global begin
        if begin == True:
            global count
            #print("gedrukt")
            count+=1
            if count > 3:
                count = 1;
            publish.single("Hardware/console",payload= count, hostname="anonymous10.ddns.net")

        elif start == True:
            print("Dn")
            publish.single("Hardware/console/bediening",payload= repr(count) + "DN", hostname="anonymous10.ddns.net")
        sleep(1)


def nummereen():
  GPIO.output(wcrol,GPIO.LOW)
  GPIO.output(kar,GPIO.LOW)
  GPIO.output(virus,GPIO.HIGH)
  for x in range(0,7):
      if x == 1 or x == 2:
          GPIO.output(led[x],GPIO.HIGH)
      else:
          GPIO.output(led[x], GPIO.LOW)

def nummertwee():
  GPIO.output(virus,GPIO.LOW)
  GPIO.output(kar,GPIO.LOW)
  GPIO.output(wcrol,GPIO.HIGH)
  for x in range(0,7):
      if x == 2:
         GPIO.output(led[x],GPIO.LOW)
      else:
         GPIO.output(led[x], GPIO.HIGH)


def nummerdrie():
  GPIO.output(virus,GPIO.LOW)
  GPIO.output(wcrol,GPIO.LOW)
  GPIO.output(kar,GPIO.HIGH)

  for x in range(0,7):
      if x == 4:
         GPIO.output(led[x],GPIO.LOW)
      else:
         GPIO.output(led[x], GPIO.HIGH)

try:
    os.system('clear')
    GPIO.add_event_detect(knop1,GPIO.RISING,callback=Up)
    GPIO.add_event_detect(knop2,GPIO.RISING,callback=Dn)
    client = mqtt.Client()
    #client.on_connect = on_connect
    client.connect(host="anonymous10.ddns.net")
    print("""welcome to the
                             ~~~~~CORONA GAME~~~~~
                                """)
    print("""choose your character with the up button, PRESS down to select
           (1)Virus  (2)toilet paper (3)shopping Car
                                                     """)

    
    while begin == True:
       if count == prevcount:
           sys.stdout.flush()
       elif(count != prevcount):
           print(str(count))
           prevcount = count
           if prevcount == 1:
              nummereen()
           elif prevcount == 2:
             nummertwee()
           elif prevcount == 3:
             nummerdrie()
           sleep(1)

    print("start the game.. You chose "+ str(count))
    while 1:
        start = True

    client.loop_forever()
except KeyboardInterrupt:
    print("close")
finally:
    GPIO.remove_event_detect(knop1)
    GPIO.remove_event_detect(knop2)
    GPIO.cleanup()
