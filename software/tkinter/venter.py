import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tkinter.font as tkFont




message = " "
player = 0
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
      if message == "b'UP'":
          kader.move(virus, 0, -35)
      if message == "b'DN'":
          kader.move(virus, 0, 35)

def toiletrol(message):
    if message == "b'UP'":
        kader.move(wcrol, 0, -35)
    if message == "b'DN'":
        kader.move(wcrol, 0, 35)

def karretje(message):
    if message == "b'UP'":
        kader.move(car, 0, -35)
    if message == "b'DN'":
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
foto = tk.PhotoImage( file = "wcrol.png" )
wcrol = kader.create_image( 10, 50, anchor = tk.NW, image=foto )
fotocar = tk.PhotoImage( file = "cart.png" )
car = kader.create_image( 400, 200, anchor = tk.NW, image=fotocar )
fotovirus = tk.PhotoImage( file = "virus.png" )
virus = kader.create_image( 700, 80, anchor = tk.NW, image=fotovirus )
scoreBoard = tk.Label(venster, text="Score: ", bg="black", fg="white", font=("Arial", 30))
scoreBoard.pack()
scoreBoard_w = kader.create_window(1700,50, window=scoreBoard)
score = tk.Label(venster, text="0", bg="black", fg="white", font = ("Arial", 30))
score.pack()
score_w = kader.create_window(1790, 50, window=score)



def on_message(client, userdata, msg):
      print(str(msg.payload))
      global message,player
      message = str(msg.payload)
      if str(msg.payload) == "b'3'":
          player = 1
          BeweegVirus()
          print(str(player))
      elif str(msg.payload) == "b'1'":
          print("erin")
          player = 2
          BeweegWcrol()
      elif str(msg.payload) == "b'2'":
          player = 3
          BeweegKar()
      elif player == 1:
          print("ok")
          coronavirus(str(msg.payload))
      elif player == 2:
          toiletrol(str(msg.payload))
      elif player == 3:
          karretje(str(msg.payload))


client = mqtt.Client()
client.on_message = on_message
client.connect(host="anonymous10.ddns.net")
client.subscribe("Desktop/project")
client.subscribe("Desktop/venster2")
client.loop_start()
venster.mainloop()
  


