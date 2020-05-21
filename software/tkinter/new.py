import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tkinter.font as tkFont

class Object:

	def __init__(self, master = None, kader = None, x = None, y = None, img = None):
		self.master = master
		self.kader = kader
		self.x = x
		self.y = y
		self.created_img = self.Create(x, y, img)

	def Create(self, x, y, img):
		return self.kader.create_image(x, y, anchor = tk.NW, image=img)

class Game:

	def __init__(self, master = None):
		self.master = master

	def Main1(self):
		width = 1920
		height = 990

		tekst = tk.Label(master, text = "Welcome to corona Game") 
		tekst.pack()
		kader = tk.Canvas(master, width=width, height=height, background="black")
		kader.pack()

		self.virus = tk.PhotoImage(file="./img/virus.png")
		self.cart = tk.PhotoImage(file="./img/cart.png")
		self.rol = tk.PhotoImage(file = "./img/wcrol.png")

		Virus = Object(master, kader, 0, 0, self.virus)
		Rol = Object(master, kader, 0, 180, self.rol)
		Cart = Object(master, kader, 0, 280, self.cart)

if __name__ == "__main__":
	master = tk.Tk() 
	game = Game(master)
	game.Main1()
	tk.mainloop()
