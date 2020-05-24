import threading
import tkinter as tk
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import tkinter.font as tkFont
import random

class Player:

	def __init__(self, master = None, canvas = None, xpos = None, ypos = None, tkphoto = None, axis = None, playernumber = None, playertype = None):

		self.master = master # Needed to create new player by collision
		# Type Of Player (VIRUS, ROL, CART)
		self.type = playertype

		# Movement Propeties
		self.speed = 10
		self.acceleration = 1
		self.moveaxis = axis

		# Image File
		self.tkphoto = tkphoto

		# Image On Canvas
		self.created_img = self.Create(canvas, xpos, ypos, tkphoto)

		# Create Label If Player Number Is Specified
		self.hasLabel = False
		if not (playernumber is None):
			self.created_label = self.CreateLabel(canvas, xpos, ypos, playernumber)
			self.hasLabel = True

	def Create(self, canvas, xpos, ypos, tkphoto):
		created_img = canvas.create_image(xpos, ypos, anchor = tk.NW, image=tkphoto)
		return created_img

	def CreateLabel(self,canvas, xpos, ypos, playernumber):
		created_label = canvas.create_text(xpos, ypos+40,text = playernumber, font=('Times New Roman',20,'bold'), fill='white', anchor = tk.NW)
		return created_label

	def Move(self, canvas): # Keep moving left/right or up/down
		vector1 = self.acceleration * self.speed

		if self.moveaxis == "horizontal":
			if self.hasLabel == True: # Only Move Label If Its Created
				canvas.move(self.created_label, vector1, 0)
			canvas.move(self.created_img, vector1, 0 )
		elif self.moveaxis == "vertical":
			if self.hasLabel == True: # Only Move Label If Its Created
				canvas.move(self.created_label, 0, vector1)
			canvas.move(self.created_img, 0, vector1)

	def GetCreatedImage(self):
		return self.created_img

	def GetTkPhoto(self):
		return self.tkphoto

	def CheckCollision(self, otherplayer, canvas): # Check if the images (rectangles) intersect
		l1x, l1y = canvas.coords(self.GetCreatedImage())
		l2x, l2y = canvas.coords(otherplayer.GetCreatedImage())

		rh1 = self.GetTkPhoto().height()
		rw1 = self.GetTkPhoto().width()
		rh2 = otherplayer.GetTkPhoto().height()
		rw2 = otherplayer.GetTkPhoto().width()

		r1x = l1x + rw1
		r1y = l1y + rh1

		r2x = l2x + rw2
		r2y = l2y + rh2

		#If one rectangle is on left side of other
		if(l1x >= r2x or l2x >= r1x):
			return False

		# If one rectangle is above other
		elif(l1y >= r2y or l2y >= r1y):
			return False
		else:
			return True

	def Control(self, pressedbutton, canvas): # Move to the direction of the button
		#print(pressedbutton)
		if self.moveaxis == "horizontal":
			if pressedbutton == "UP":
				if self.hasLabel == True: # Only Move Label If Its Created
					canvas.move(self.created_label, 0, +10)
				canvas.move(self.created_img, 0, +10)
			elif pressedbutton == "DN":
				if self.hasLabel == True: # Only Move Label If Its Created
					canvas.move(self.created_label, 0, -10)
				canvas.move(self.created_img, 0, -10)

		elif self.moveaxis == "vertical":
			if pressedbutton == "UP":
				if self.hasLabel == True: # Only Move Label If Its Created
					canvas.move(self.created_label, +10, 0)
				canvas.move(self.created_img, +10, 0)
			elif pressedbutton == "DN":
				if self.hasLabel == True: # Only Move Label If Its Created
					canvas.move(self.created_label, -10, 0)
				canvas.move(self.created_img, -10, 0)


	def CheckEdges(self, canvas, canvas_width, canvas_height): # Check If Player Is Inside Canvas
		image_posx, image_posy = canvas.coords(self.created_img)
		image_width = self.tkphoto.width()
		image_height = self.tkphoto.height()

		if self.moveaxis == "horizontal":
			if self.type == "cart":
				if (image_posx < 850) or (image_posx > 900):
					self.acceleration = self.acceleration * -1 # Invert
					print("done")


			if (image_posx <  0) or (image_posx > canvas_width - image_width):
				self.acceleration = self.acceleration * -1 # Invert
				print("Collision Horizontal")

		elif self.moveaxis == "vertical":
			if (image_posy < 0) or (image_posy > canvas_height - image_height):
				self.acceleration = self.acceleration * -1 # Invert
				print("Collision Vertical")

class Game:
	def __init__(self, master = None):
		self.master = master
		self.counter = 0

	def CreateUI(self):

                # Create Canvas + Title + Score Text

		self.width = 1920
		self.height = 990

		tekst = tk.Label(master, text = "Welcome to corona Game")
		tekst.pack()
		kader = tk.Canvas(master, width=self.width, height=self.height, background="black")
		kader.pack()
		scoreBoard = tk.Label(self.master, text="Score: ", bg="black", fg="white", font=("Arial", 30))
		scoreBoard.pack()
		scoreBoard_w = kader.create_window(900, 50, window=scoreBoard)
		self.score = tk.Label(self.master, text = str(self.counter), bg="black", fg="white", font=("Arial", 30))
		self.score.pack()
		score_w = kader.create_window(1000, 50, window=self.score)

		self.timer = tk.Label(self.master, text = " ", bg="black", fg="white", font=("Arial", 30))
		self.timer.pack()
		timer_w = kader.create_window(1000, 900, window=self.timer)

		return kader


	def HandleControls(self, message): # Handle the message received from the broker
				 			# Full Message = b'3UP'
		playernumber = int(message[2:3])	# Player Number = 3
		pressedbutton = message [3:5]		# Pressed Button = UP
		print(message)
		#print(playernumber)
		#print(pressedbutton)

		if playernumber == 1:
			print("player 1 moved")
			self.RolPlayer.Control(pressedbutton, self.kader)
		if playernumber == 2:
			print("player 2 moved")
			self.CartPlayer.Control(pressedbutton, self.kader)
		if playernumber == 3:
			print("player 3 moved")
			self.VirusPlayer.Control(pressedbutton, self.kader)


	def HandleCollision(self, state, canvas, rolplayer):
		# Remove Roll Player And The Label (If Its Specified) #
		canvas.delete(rolplayer.created_img)

		# Create New Player
		randomx = random.randint(100,1800)
		randomy = random.randint(100, 700)
		rolPhoto = tk.PhotoImage(file="./img/wcrol.png")
		if rolplayer.hasLabel == False:
			#canvas.delete(rolplayer.created_label)
			self.allPlayers.remove(rolplayer)
			newComputerRol = Player(self.master, self.kader, randomx, randomy, rolPhoto, "horizontal", None, "rol")
			self.allPlayers.append(newComputerRol)

		elif rolplayer.hasLabel == True:
			canvas.delete(rolplayer.created_label)
			self.allPlayers[1] = None
			self.RolPlayer = Player(self.master, self.kader, randomx, randomy, rolPhoto, "horizontal", "1", "rol")
			self.allPlayers[1] = self.RolPlayer

		# Handle Score
		if state == "cart":
			print("Adding Score")
			self.counter += 1
		if state == "virus":
			print("Dont Add Score")
			self.counter -= 1
		self.score['text'] = str(self.counter)
		print(str(self.counter))
		# Publish Score
		publish.single("Desktop/score", payload=1, hostname="anonymous10.ddns.net")

	def GameTimer(self, count):
		for i in range(count, -1, -1):
			m, s = divmod(i, 60)
			h, m = divmod(m, 60)
			time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
			print(time_left)
			sleep(1)
			if i == 0:
				print("Game over!")
			print(str(i))
			self.timer['text'] = str(i)
			#publish.single("Software/controller/timer", payload=i, hostname="anonymous10.ddns.net")def timer(count):


	def Start(self):

		#Create UI

		kader = self.CreateUI()
		self.kader = kader

		# Create Game Players

		virusPhoto = tk.PhotoImage(file="./img/virus.png")
		cartPhoto = tk.PhotoImage(file="./img/cart.png")
		rolPhoto = tk.PhotoImage(file = "./img/wcrol.png")

		self.VirusPlayer = Player(master, kader, 1700, 450, virusPhoto, "horizontal", "3", "virus")
		self.RolPlayer = Player(master, kader, 200, 450, rolPhoto, "horizontal", "1", "rol")
		self.CartPlayer = Player(master, kader, 900, 450, cartPhoto, "horizontal", "2", "cart")
		self.allPlayers = [self.VirusPlayer, self.RolPlayer, self.CartPlayer]

		# Created Dummy Players
		for x in range (0,3):
			randomx = random.randint(1350, 1750)
			randomy = random.randint(50, 750)
			viruscomputer = Player(master, kader, randomx, randomy, virusPhoto, "horizontal", None , "virus")
			self.allPlayers.append(viruscomputer)

		for x in range(0,3):
			randomx = random.randint(200, 400)
			randomy = random.randint(50, 900)
			rolcomputer = Player(master, kader, randomx, randomy, rolPhoto, "horizontal", None , "rol")
			self.allPlayers.append(rolcomputer)


		# Start Gameloop

		loop_thread = threading.Thread(target=self.Loop, args=(kader,self.allPlayers))
		loop_thread.start()
		loop_thread_timer = threading.Thread(target=self.GameTimer, args=[180])
		loop_thread_timer.start()

	def Loop(self, kader ,allPlayers): # Gameloop
		while True:

			# Check Collision Of Roll With Other Players (Dummy and Real)

			isCollided = False
			typeOfCollidedPlayer = " "
			wcrolPlayer = allPlayers[1]

			for otherPlayer in allPlayers:
				if otherPlayer != wcrolPlayer and isCollided == False and otherPlayer.type != "rol":
					typeOfCollidedPlayer = otherPlayer.type
					isCollided = wcrolPlayer.CheckCollision(otherPlayer, kader)


			for player in allPlayers:
				for otherplayer in allPlayers:
					if player != otherplayer and isCollided == False and player.type == "rol" and otherplayer.type != "rol":
						typeOfCollidedPlayer = otherplayer.type
						wcrolPlayer = player
						isCollided = player.CheckCollision(otherplayer, kader)
						if isCollided == True:
							print("dummy rol")

			if isCollided == True:
				self.HandleCollision(typeOfCollidedPlayer, kader, wcrolPlayer)


			for obj in allPlayers:

				# Check Collision With Edges Of Screen
				obj.CheckEdges(kader, self.width, self.height)
				# Keep Moving UP/DOWN or LEFT/RIGHT
				obj.Move(kader)

			sleep(0.5)


if __name__ == "__main__":

	# GameSetup

	master = tk.Tk()
	game = Game(master)

	def on_message(client, userdata, msg):
		#print(str(msg.payload))
		game.HandleControls(str(msg.payload))

	# MQTT SETUP

	client = mqtt.Client()
	client.on_message = on_message
	client.connect(host="anonymous10.ddns.net")
	client.subscribe("Hardware/console/bediening")

	# Start Loops

	client.loop_start()
	game.Start()
	tk.mainloop()
