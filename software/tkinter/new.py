import threading
import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tkinter.font as tkFont

class Object:

	def __init__(self, master = None, canvas = None, xpos = None, ypos = None, tkphoto = None):
		self.master = master
		#self.kader = kader
		self.xpos = xpos
		self.ypos = ypos
		self.created_img = self.Create(canvas, xpos, ypos, tkphoto)

	def Create(self, canvas, xpos, ypos, tkphoto):
		created_img = canvas.create_image(xpos, ypos, anchor = tk.NW, image=tkphoto)
		return created_img

	def Move(self, canvas):
		canvas.move(self.created_img, 2, 2)

class Game:

	def __init__(self, master = None):
		self.master = master

	def Start(self):
		width = 1920
		height = 990

		tekst = tk.Label(master, text = "Welcome to corona Game") 
		tekst.pack()
		kader = tk.Canvas(master, width=width, height=height, background="black")
		kader.pack()

		# Create Game Objects

		self.virus = tk.PhotoImage(file="./img/virus.png")
		self.cart = tk.PhotoImage(file="./img/cart.png")
		self.rol = tk.PhotoImage(file = "./img/wcrol.png")

		Virus = Object(master, kader, 0, 0, self.virus)
		Rol = Object(master, kader, 0, 180, self.rol)
		Cart = Object(master, kader, 0, 280, self.cart)

		allObjects = [Virus, Rol, Cart]

		x = threading.Thread(target=self.loop, args=(kader, allObjects))
		x.start()

	def loop(self, kader, allObjects):
		while True:
			for obj in allObjects:
				obj.Move(kader)

			sleep(0.25)


if __name__ == "__main__":
	master = tk.Tk()
	game = Game(master)
	game.Start()
	tk.mainloop()
