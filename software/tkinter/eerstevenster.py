import tkinter as tk
import os
import tkinter.font as tkFont
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

a = True

def main1():
    menuvenster = tk.Tk()

    kader = tk.Canvas(menuvenster, width = 1920, height = 990, background="black")

    kader.pack()

    coronaFont = tkFont.Font(family="Lucida Grande", size=30)



    titel = tk.PhotoImage(file="title.png")

    titel_w = kader.create_image(950, 550, image=titel)



    spelersKeuzeTxt = tk.Label(menuvenster, text= "Kies een speler",bg="black", fg="#c3081e", font=("Arial", 15))

    spelersKeuzeTxt.pack()

    spelersKeuzeTxt_w = kader.create_window(710, 220, window=spelersKeuzeTxt)



    wcrolImg = tk.PhotoImage(file="wcrol.png")



    karImg = tk.PhotoImage(file="car.png")



    virusImg = tk.PhotoImage(file="virus.png")


    
    playerNr = 0



    #hover functies

    def hover(e):
        if str(e) == "virusBtn":
            virusBtn.configure(

        bg="#f8f9f8",

        width="180",

        height="180"

            )
        elif str(e) == "karBtn":
            karBtn.configure(

        bg="#f8f9f8",

        width="180",

        height="180"

            )
        elif str(e) == "wcrolBtn":
            wcrolBtn.configure(

        bg="#f8f9f8",

        width="180",

        height="180"

            )



    def leave(e):
        if str(e) == "virusBtn":
            virusBtn.configure(

        bg="black",

        width="170",

        height="170"

            )
        elif str(e) == "karBtn":
            karBtn.configure(

        bg="black",

        width="200",

        height="200"

            )
        elif str(e) == "wcrolBtn":
            wcrolBtn.configure(

        bg="black",

        width="200",

        height="200"

            )




    def WcRol():
            playerNr = 1
            print("Je bent het toilet papier " + str(playerNr))
            menuvenster.destroy()
            #publish.single("Desktop/menuvenster2",payload= "wcrol", hostname="anonymous10.ddns.net")


    def Kar():

            playerNr = 2

            print("Je bent het karretje " + str(playerNr))
            menuvenster.destroy()


    def Virus():

            playerNr = 3

            print("Je bent het virus " + str(playerNr))
            menuvenster.destroy()


    wcrolBtn = tk.Button(menuvenster,width=200, height=200, image=wcrolImg, bg="black", border=0, command=WcRol)

    wcrolBtn.pack()

    wcrolBtn_w = kader.create_window(600,570, window=wcrolBtn)





    karBtn = tk.Button(menuvenster,width=200, height=200, image=karImg, bg="black", border=0, command=Kar)

    karBtn.pack()

    karBtn_w = kader.create_window(900,570, window=karBtn)







    virusBtn = tk.Button(menuvenster, width=200, height=200, image=virusImg, bg="black", border=0, command=Virus)

    virusBtn.pack()

    virusBtn_w = kader.create_window(1200, 570, window=virusBtn)


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
