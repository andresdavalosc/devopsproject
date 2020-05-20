import tkinter as tk
import os
import tkinter.font as tkFont
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from threading import Thread

a = False

class Button:
  def __init__(self, master = None, playerType = None, kader = None, Btn = None):
    self.master = master
    self.Btn = Btn
    self.kader = kader
    self.playerType = playerType

  def CreateButton(self, width, height, img, window_x, window_y):
    kader = self.kader

    self.Btn = tk.Button(master,width=width, height=height, image=img, bg="black", border=0, command=self.ClickEvent)
    self.Btn.pack()
    self.Btn_w = kader.create_window(window_x, window_y, window=self.Btn)

  def ClickEvent(self):
      kader = self.kader
      playertype = self.playerType
      if playertype == "Roll":
           kader.create_rectangle(500, 400, 750, 450, fill='green')
           kader.create_text((625, 425), text = playertype + " got picked and is ready to roll!")

      if playertype == "Virus":
           kader.create_rectangle(1055, 400, 1303, 450, fill='green')
           kader.create_text((1185, 425), text="Virus got picked and is ready!")

      if playertype == "Kar":
           kader.create_rectangle(755, 400, 1050, 450, fill='green')
           kader.create_text((900, 425), text="Car got picked and is ready!")
      self.Btn.destroy()

  def hoverButton(self):
     self.Btn.configure(bg="#f8f9f8",width="180",height="180")

  def leaveButton(self):
     self.Btn.configure(bg="black",width="170",height="170")

class CountdownTimer:
    def __init__(self, master = None):
       self.master = master
       self.label = tk.Label(master)

    def Countdown(self, count):
      self.label['text'] = 'Ready to play in ' + str(count)
      if count > 0:
          master.after(1000, self.Countdown, count-1)
      if count == 0:
          os.system("python3 spel.py 1")
          self.master.destroy()

      self.label.place(x=830, y=770)

class Menu:
  def __init__(self, master = None):
    self.master = master

  def Main1(self):
       width = 1900
       height = 900

       kader = tk.Canvas(master, width=width, height=height, background="black")
       kader.pack()

       coronaFont = tkFont.Font(family="Lucida Grande", size=30)
       self.titel = tk.PhotoImage(file="./img/title.png")
       titel_w = kader.create_image(850,350, image=self.titel)

       spelersKeuzeTxt = tk.Label(master, text= "Kies een speler",bg="black", fg="#c3081e", font=("Arial", 15))
       spelersKeuzeTxt.pack()
       spelersKeuzeTxt_w = kader.create_window(710, 220, window=spelersKeuzeTxt)

       self.wcrolImg = tk.PhotoImage(file="./img/wcrol.png")
       self.karImg = tk.PhotoImage(file="./img/cart.png")
       self.virusImg = tk.PhotoImage(file="./img/virus.png")

       Roll = Button(master, "Roll", kader, tk.Button())
       Virus = Button(master, "Virus", kader, tk.Button())
       Kar = Button(master, "Kar", kader, tk.Button())

       Roll.CreateButton(200, 200, self.wcrolImg, 600, 570)
       Virus.CreateButton(200, 200, self.virusImg, 1200, 570)
       Kar.CreateButton(200, 200, self.karImg, 900, 570)

       MenuTimer = CountdownTimer(master)
       MenuTimer.Countdown(15)

       def on_closing():
         global a
         a = False
         master.destroy()
       master.protocol("WM_DELETE_WINDOW", on_closing)


       def on_message(client, userdata, msg):
           print(str(msg.payload))
           if str(msg.payload) == "b'1'":
               Roll.hoverButton()
               Kar.leaveButton()
               Virus.leaveButton()
           elif str(msg.payload) == "b'2'":
               Kar.hoverButton()
               Virus.leaveButton()
               Roll.leaveButton()
           elif str(msg.payload) == "b'3'":
               Virus.hoverButton()
               Kar.leaveButton()
               Roll.leaveButton()
           elif str(msg.payload) == "b'start1'":
               Roll.ClickEvent()
           elif str(msg.payload) == "b'start2'":
               Kar.ClickEvent()
           elif str(msg.payload) == "b'start3'":
               Virus.ClickEvent()
       client = mqtt.Client()
       client.on_message = on_message
       client.connect(host="anonymous10.ddns.net")
       client.subscribe("Hardware/console")
       client.loop_start()

  def Main2(self):
       os.system("python3 /home/pi/Desktop/NewRaspProjectFile/Raspi-project-game/hardware/project_console.py")

if __name__ == "__main__":
  master = tk.Tk()
  menu = Menu(master)

  job1 = Thread(target=menu.Main2)
  job2 = Thread(target=menu.Main1)

  job1.start()
  job2.start()

  tk.mainloop()
