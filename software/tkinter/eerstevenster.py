import tkinter as tk
import os
import tkinter.font as tkFont
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

a = True

def main1():
    width = 1600
    height = 990

    menuvenster = tk.Tk()
    kader = tk.Canvas(menuvenster, width = width, height = height, background="black")
    kader.pack()

    coronaFont = tkFont.Font(family="Lucida Grande", size=30)
    titel = tk.PhotoImage(file="./img/title.png")

    titel_w = kader.create_image(850,350, image=titel)

    spelersKeuzeTxt = tk.Label(menuvenster, text= "Kies een speler",bg="black", fg="#c3081e", font=("Arial", 15))
    spelersKeuzeTxt.pack()
    spelersKeuzeTxt_w = kader.create_window(710, 220, window=spelersKeuzeTxt)

    wcrolImg = tk.PhotoImage(file="./img/wcrol.png")
    karImg = tk.PhotoImage(file="./img/car.png")
    virusImg = tk.PhotoImage(file="./img/virus.png")

    playerNr = 0
    counter = 0

    #hover functies
    def hover(e):
        if str(e) == "virusBtn":
           virusBtn.configure(bg="#f8f9f8",width="180",height="180")
        elif str(e) == "karBtn":
            karBtn.configure(bg="#f8f9f8",width="180",height="180")
        elif str(e) == "wcrolBtn":
            wcrolBtn.configure(bg="#f8f9f8",width="180",height="180")

    def leave(e):
        if str(e) == "virusBtn":
            virusBtn.configure(bg="black",width="170",height="170")
        elif str(e) == "karBtn":
            karBtn.configure(bg="black",width="200",height="200")
        elif str(e) == "wcrolBtn":
            wcrolBtn.configure(bg="black",width="200",height="200")

    def WcRol():
            playerNr = 1
            print("Je bent het toilet papier " + str(playerNr))
            kader.create_rectangle(500, 400, 750, 450, fill='green')
            kader.create_text((625, 425), text="Roll got picked and is ready to roll!")
            wcrolBtn.configure(state="disabled")
            print(playerNr)
            return playerNr

    def Kar():
            playerNr = 2
            print("Je bent het karretje " + str(playerNr))
            kader.create_rectangle(755, 400, 1050, 450, fill='green')
            kader.create_text((900, 425), text="Car got picked and is ready!")
            karBtn.configure(state="disabled")

    def Virus():
            playerNr = 3
            print("Je bent het virus " + str(playerNr))
            kader.create_rectangle(1055, 400, 1303, 450, fill='green')
            kader.create_text((1185, 425), text="Virus got picked and is ready!")
            virusBtn.configure(state = "disabled")

    def countdown(count): 
            label['text'] = 'Ready to play in ' + str(count)

            if count > 0:
        # call countdown again after 1000ms (1s)
                menuvenster.after(1000, countdown, count-1)
            if count == 0:
                menuvenster.destroy()
    
    label = tk.Label(menuvenster)
    label.place(x=830, y=770)

    wcrolBtn = tk.Button(menuvenster,width=200, height=200, image=wcrolImg, bg="black", border=0, command=WcRol)
    wcrolBtn.pack()
    wcrolBtn_w = kader.create_window(600,570, window=wcrolBtn)

    karBtn = tk.Button(menuvenster,width=200, height=200, image=karImg, bg="black", border=0, command=Kar)
    karBtn.pack()
    karBtn_w = kader.create_window(900,570, window=karBtn)

    virusBtn = tk.Button(menuvenster, width=200, height=200, image=virusImg, bg="black", border=0, command=Virus)
    virusBtn.pack()
    virusBtn_w = kader.create_window(1200, 570, window=virusBtn)

    countdown(30)

    def on_closing():
        global a
        a = False
        menuvenster.destroy()
    menuvenster.protocol("WM_DELETE_WINDOW", on_closing)


    def on_message(client, userdata, msg):
        print(str(msg.payload))
        if str(msg.payload) == "b'1'":
            hover("wcrolBtn")
            leave("virusBtn")
            leave("karBtn")
        elif str(msg.payload) == "b'2'":
            hover("karBtn")
            leave("wcrolBtn")
            leave("virusBtn")
        elif str(msg.payload) == "b'3'":
            hover("virusBtn")
            leave("wcrolBtn")
            leave("karBtn")
        elif str(msg.payload) == "b'start1'":
            WcRol()
        elif str(msg.payload) == "b'start2'":
            Kar()
        elif str(msg.payload) == "b'start3'":
            Virus()
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host="anonymous10.ddns.net")
    client.subscribe("Desktop/project1")
    client.loop_start()

    menuvenster.mainloop()

main1()
if a == True:
 os.system("python3 venter.py 1")


