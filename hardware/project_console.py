#!/usr/bin/python3/
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import os
import paho.mqtt.publish as publish
import sys
from time import sleep

led = [10,9,11,5,6,13,19]
prevcount = 0
ab = False
count = 1
start = 0
begin = True
knop1,knop2=3,2
GPIO.setmode(GPIO.BCM)
GPIO.setup(knop1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(knop2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
for x in led:
    GPIO.setup(x,GPIO.OUT,initial=GPIO.LOW)
def Up(a):
    if GPIO.event_detected(knop1):
        global begin
        if begin == True:
            begin = False
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
        sleep(1)

def nummereen():
  GPIO.output(led[0],GPIO.LOW)
  GPIO.output(led[1],GPIO.HIGH)
  GPIO.output(led[2],GPIO.HIGH)
  GPIO.output(led[3],GPIO.LOW)
  GPIO.output(led[6],GPIO.LOW)
  GPIO.output(led[4],GPIO.LOW)
def nummertwee():
  GPIO.output(led[0],GPIO.HIGH)
  GPIO.output(led[1],GPIO.HIGH)
  GPIO.output(led[3],GPIO.HIGH)
  GPIO.output(led[4],GPIO.HIGH)
  GPIO.output(led[6],GPIO.HIGH)
  GPIO.output(led[2],GPIO.LOW)

def nummerdrie():
  GPIO.output(led[0],GPIO.HIGH)
  GPIO.output(led[1],GPIO.HIGH)
  GPIO.output(led[2],GPIO.HIGH)
  GPIO.output(led[3],GPIO.HIGH)
  GPIO.output(led[6],GPIO.HIGH)
  GPIO.output(led[4],GPIO.LOW)


try:
    os.system('clear')
    GPIO.add_event_detect(knop1,GPIO.RISING,callback=Up)
    GPIO.add_event_detect(knop2,GPIO.RISING,callback=Dn)
    print("""welcome to the..
                             ~~~~~CORONA GAME~~~~~"""
                                )
    print("""choose your character with the up button, PRESS down to select
           (1)Virus  (2)toilet paper (3)shopping Car
                                                     """)
    #begin = True
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
except KeyboardInterrupt:
    print("close")
finally:
    GPIO.remove_event_detect(knop1)
    GPIO.remove_event_detect(knop2)
    GPIO.cleanup()
