import tkinter as tk 
from time import sleep 
import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish 
import tkinter.font as tkFont

venster = tk.Tk()
player1=0
player2=0
player3=0
venster.counter = 0

def Collision(obj,bool):
     global score,wcrol
     kader.delete(obj)
     wcrol = kader.create_image( 10, 250, anchor = tk.NW, image=foto )
     if bool == True:
       venster.counter += 1
     elif bool == False:
       venster.counter -= 1
     publish.single("Desktop/score", payload=venster.counter, hostname="anonymous10.ddns.net")
     score['text'] = str(venster.counter)
     print(venster.counter)

def BeweegKar():
        global kar_speed,h
        global kar_move_right
        kader.move(car, 0,kar_speed)
        x1, y1 = kader.coords(car)
        if kar_move_right:

                if y1 > h-220:
                        kar_move_right = not kar_move_right
                        kar_speed = -kar_speed
        else:
                if y1 < 10:
                        kar_move_right = not kar_move_right
                        kar_speed = -kar_speed
        venster.after(25, BeweegKar)

def BeweegWcrol():
        global wcrol_speed,w
        global wcrol_move_right
        kader.move(wcrol, wcrol_speed, 0)
        x1, y1 = kader.coords(wcrol)
        x2, y2 = kader.coords(car)
        x3, y3 = kader.coords(virus)
        if wcrol_move_right:

                if x1 > w-35:
                        print("groter")
                        wcrol_move_right = not wcrol_move_right
                        wcrol_speed = -wcrol_speed
        else:
                if x1 < 0:
                        wcrol_move_right = not wcrol_move_right
                        wcrol_speed = -wcrol_speed
       # venster.after(25, BeweegWcrol)
        if  x1 < x2+100 and x1 > x2 and y1 < y2+100 and y1 > y2:
            Collision(wcrol,True)
        elif  x1 < x3+100 and x1 > x3 and y1 < y3+100 and y1 > y3:
            Collision(wcrol,False)
        venster.after(25, BeweegWcrol)


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
          kader.move(car,-35,0)
     if message == "b'2DN'":
          kader.move(car,35,0)

kar_speed=2
kar_move_right = True
wcrol_speed=2
wcrol_move_right = True
virus_speed=-2
virus_move_left = True
w = 1920
h = 990
posy =250
posx=10
tekst = tk.Label( venster, text = "Welcome to corona Game")
tekst.pack()
kader = tk.Canvas(venster, width = w, height = h, bg ="black")
kader.pack()
foto = tk.PhotoImage( file = "./img/wcrol.png" )
wcrol = kader.create_image( posx, posy, anchor = tk.NW, image=foto )
fotocar = tk.PhotoImage( file = "./img/cart.png" )
car = kader.create_image( 400, 200, anchor = tk.NW, image=fotocar )
fotovirus = tk.PhotoImage( file = "./img/virus.png" )
virus = kader.create_image( 700, 80, anchor = tk.NW, image=fotovirus )
scoreBoard = tk.Label(venster, text="Score: ", bg="black", fg="white", font=("Arial", 30))
scoreBoard.pack()
scoreBoard_w = kader.create_window(1700,50, window=scoreBoard)
score = tk.Label(venster, text ='0', bg="black", fg="white", font=("Arial", 30))
score.pack()
score_w = kader.create_window(1780,50, window=score)
BeweegVirus()
BeweegWcrol()
BeweegKar()

def on_message(client, userdata, msg):
      print(str(msg.payload))
      global player1,player2,player3

      if str(msg.payload) == "b'3UP'" or str(msg.payload) == "b'3DN'":
          print("ok")
          coronavirus(str(msg.payload))
      elif str(msg.payload) == "b'1UP'" or str(msg.payload) == "b'1DN'":
          print("erin")
          toiletrol(str(msg.payload))
      elif str(msg.payload) == "b'2UP'" or str(msg.payload) == "b'2DN'":
          karretje(str(msg.payload))
      else:
          print(str(tijd))
          tijd = tk.Label( venster, text = str(msg.payload))
          tijd.pack()

client = mqtt.Client()
client.on_message = on_message
client.connect(host="anonymous10.ddns.net")
client.subscribe("Hardware/console/bediening")
client.subscribe("Software/controller/timer")
#client.subscribe("Desktop/venster2")
client.loop_start()
venster.mainloop()
 


