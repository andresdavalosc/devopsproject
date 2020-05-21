import threading
import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tkinter.font as tkFont

class Object:

	def __init__(self, master = None, canvas = None, xpos = None, ypos = None, tkphoto = None, axis = None):

		self.master = master
		self
		# Movement Propeties
		self.speed = 10
		self.acceleration = 1
		self.moveaxis = axis

		# Image On Canvas
		self.created_img = self.Create(canvas, xpos, ypos, tkphoto)

	def Create(self, canvas, xpos, ypos, tkphoto):
		created_img = canvas.create_image(xpos, ypos, anchor = tk.NW, image=tkphoto)
		return created_img

	def Move(self, canvas):
		vector1 = self.acceleration * self.speed

		if self.moveaxis == "vertical":
			canvas.move(self.created_img, vector1, 0 )
		elif self.moveaxis == "horizontal":
			canvas.move(self.created_img, 0, vector1)

	def CheckEdges(self, canvas, width, height):
		x1, y1 = canvas.coords(self.created_img)

		if self.moveaxis == "vertical":

			if (x1 <  0) or x1 > (width):
				self.acceleration = self.acceleration * -1
				print("Collision Vertical")

		elif self.moveaxis == "horizontal":
			if (y1 < 0) or (y1 > height):
				self.acceleration = self.acceleration * -1
				print("Collision Horizontal")

class Game:

	def __init__(self, master = None):
		self.master = master

	def Start(self):
		self.width = 1920
		self.height = 990

		tekst = tk.Label(master, text = "Welcome to corona Game") 
		tekst.pack()
		kader = tk.Canvas(master, width=self.width, height=self.height, background="black")
		kader.pack()

		# Create Game Objects

		self.virus = tk.PhotoImage(file="./img/virus.png")
		self.cart = tk.PhotoImage(file="./img/cart.png")
		self.rol = tk.PhotoImage(file = "./img/wcrol.png")

		Virus = Object(master, kader, 0, 0, self.virus, "horizontal")
		Rol = Object(master, kader, 0, 180, self.rol, "vertical")
		Cart = Object(master, kader, 0, 280, self.cart, "horizontal")

		allObjects = [Virus, Rol, Cart]

		x = threading.Thread(target=self.loop, args=(kader, allObjects))
		x.start()

	def loop(self, kader, allObjects):
		while True:
			for obj in allObjects:
				obj.CheckEdges(kader, self.width, self.height)
				obj.Move(kader)

			sleep(0.25)


if __name__ == "__main__":
	master = tk.Tk()
	game = Game(master)
	game.Start()
	tk.mainloop()
