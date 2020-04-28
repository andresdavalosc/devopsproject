import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tkinter.font as tkFont




message = " "
player1=0
player2=0
player3=0

def Collision(obj):
      kader.delete(obj)
    
def BeweegKar():
        global kar_speed
        global kar_move_right
        kader.move(car, kar_speed, 0)
        x1, y1 = kader.coords(car)
        if kar_move_right:

                if x1 > 550:
                        kar_move_right = not kar_move_right
                        kar_speed = -kar_speed
        else:
                if x1 < 310:
                        kar_move_right = not kar_move_right
                        kar_speed = -kar_speed
        venster.after(25, BeweegKar)
        
def BeweegWcrol():
        global wcrol_speed,w
        global wcrol_move_right
        kader.move(wcrol, wcrol_speed, 0)
        x1, y1 = kader.coords(wcrol)
        x2, y2 = kader.coords(car)
        if wcrol_move_right:

                if x1 > w-35:
                        print("groter")
                        wcrol_move_right = not wcrol_move_right
                        wcrol_speed = -wcrol_speed
        else:
                if x1 < 0:
                        wcrol_move_right = not wcrol_move_right
                        wcrol_speed = -wcrol_speed
        venster.after(25, BeweegWcrol)
        if  x1 < x2+220 and x1 > x2 and y1 < y2+235 and y1 > y2:
            Collision(wcrol)
            venster.after_cancel(BeweegWcrol)
        

def BeweegVirus():
        global virus_speed,w
        global virus_move_left
        kader.move(virus, virus_speed, 0)
        x1, y1 = kader.coords(virus)
        if virus_move_left:

                if x1 < -10:
                        virus_move_left = not virus_move_left
                        virus_speed = -virus_speed
        else:
                if x1 > w-120:
                        virus_move_left = not virus_move_left
                        virus_speed = -virus_speed
        venster.after(25, BeweegVirus)

def coronavirus(message):
      if message == "b'3UP'":
          kader.move(virus, 0, -35)
      if message == "b'3DN'":
          kader.move(virus, 0, 35)

def toiletrol(message):
    if message == "b'1UP'":
        kader.move(wcrol, 0, -35)
    if message == "b'1DN'":
        kader.move(wcrol, 0, 35)

def karretje(message):
    if message == "b'2UP'":
        kader.move(car, 0, -35)
    if message == "b'2DN'":
        kader.move(car, 0, 35)


venster = tk.Tk()
kar_speed=2
kar_move_right = True
wcrol_speed=2
wcrol_move_right = True
virus_speed=-2
virus_move_left = True
w = 1920
h = 990
tekst = tk.Label( venster, text = "Welcome to corona Game")
tekst.pack()
kader = tk.Canvas(venster, width = w, height = h, bg ="black")
kader.pack()
foto = tk.PhotoImage( file = "./img/wcrol.png" )
wcrol = kader.create_image( 10, 50, anchor = tk.NW, image=foto )
fotocar = tk.PhotoImage( file = "./img/car.png" )
car = kader.create_image( 400, 200, anchor = tk.NW, image=fotocar )
fotovirus = tk.PhotoImage( file = "./img/virus.png" )
virus = kader.create_image( 700, 80, anchor = tk.NW, image=fotovirus )

BeweegVirus()
BeweegWcrol()
BeweegKar()

def on_message(client, userdata, msg):
      print(str(msg.payload))
      global message,player1,player2,player3
      message = str(msg.payload)
      
      if str(msg.payload) == "b'3UP'" or str(msg.payload) == "b'3DN'":
          print("ok")
          coronavirus(str(msg.payload))
      elif str(msg.payload) == "b'1UP'" or str(msg.payload) == "b'1DN'":
          print("erin")
          toiletrol(str(msg.payload))
      elif str(msg.payload) == "b'2UP'" or str(msg.payload) == "b'2DN'":
          karretje(str(msg.payload))


client = mqtt.Client()
client.on_message = on_message
client.connect(host="anonymous10.ddns.net")
client.subscribe("Desktop/project")
client.subscribe("Desktop/venster2")
client.loop_start()
venster.mainloop()
  


