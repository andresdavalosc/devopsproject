import tkinter as tk
import tkinter.font as tkFont
venster = tk.Tk()
kader = tk.Canvas(venster, width = 800, height = 420, background="black")
kader.pack()
coronaFont = tkFont.Font(family="Lucida Grande", size=30)

titel = tk.PhotoImage(file="./img/title.png")
titel_w = kader.create_image(400, 75, image=titel)

spelersKeuzeTxt = tk.Label(venster, text= "Kies een speler",bg="black", fg="#c3081e", font=("Arial", 15))
spelersKeuzeTxt.pack()
spelersKeuzeTxt_w = kader.create_window(410, 120, window=spelersKeuzeTxt)

wcrolImg = tk.PhotoImage(file="wcrol.png")

karImg = tk.PhotoImage(file="cart.png")

virusImg = tk.PhotoImage(file="virus.png")

playerNr = 0

#hover functies
def on_enter_wc(e):
	wcrolBtn.configure(
		bg="#c3081e",
		width="180",
		height="180"
	)
	
def on_leave_wc(e):
	wcrolBtn.configure(
		bg="black",
		width="170",
		height="170"
	)
	
def on_enter_kar(e):
	karBtn.configure(
		bg="#c3081e",
		width="180",
		height="180"
	)
	
def on_leave_kar(e):
	karBtn.configure(
		bg="black",
		width="170",
		height="170"
	)

def on_enter_virus(e):
	virusBtn.configure(
		bg="#c3081e",
		width="180",
		height="180"
	)
	
def on_leave_virus(e):
	virusBtn.configure(
		bg="black",
		width="170",
		height="170"
	)
	
def WcRol():
	playerNr = 1
	print("Je bent het toilet papier " + str(playerNr))
	
def Kar():
	playerNr = 2
	print("Je bent het karretje " + str(playerNr))	
	
def Virus():
	playerNr = 3
	print("Je bent het virus " + str(playerNr))

wcrolBtn = tk.Button(venster,width=170, height=170, image=wcrolImg, bg="black", border=0, command=WcRol)
wcrolBtn.pack()
wcrolBtn_w = kader.create_window(200,270, window=wcrolBtn)
wcrolBtn.bind("<Enter>", on_enter_wc)
wcrolBtn.bind("<Leave>", on_leave_wc)
nr1Label = tk.Label(venster, text="(1)", bg="black", fg="#c3081e", font=("Arial", 20))
nr1Label.pack()
nr1Label_w = kader.create_window(200, 380, window=nr1Label)

karBtn = tk.Button(venster,width=170, height=170, image=karImg, bg="black", border=0, command=Kar)
karBtn.pack()
karBtn_w = kader.create_window(400,270, window=karBtn)
karBtn.bind("<Enter>", on_enter_kar)
karBtn.bind("<Leave>", on_leave_kar)
nr2Label = tk.Label(venster, text="(2)", bg="black", fg="#c3081e", font=("Arial", 20))
nr2Label.pack()
nr2Label_w = kader.create_window(400, 380, window=nr2Label)


virusBtn = tk.Button(venster, width=170, height=170, image=virusImg, bg="black", border=0, command=Virus)
virusBtn.pack()
virusBtn_w = kader.create_window(600, 270, window=virusBtn)
virusBtn.bind("<Enter>", on_enter_virus)
virusBtn.bind("<Leave>", on_leave_virus)
nr3Label = tk.Label(venster, text="(3)", bg="black", fg="#c3081e", font=("Arial", 20))
nr3Label.pack()
nr3Label_w = kader.create_window(600, 380, window=nr3Label)






venster.mainloop()

