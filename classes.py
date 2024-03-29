import pygame
from pygame.locals import * 
from random import randint
import math

class Maze():

	def __init__(self):
		self.BLACK = (0,0,0) #coding or the required colors
		self.GOLD = (246,253,49)
		self.GREY = (50,50,50)
		self.RED = (255,0,0)
		self.BLUE = (20,27,229)
		self.WHITE = (255,255,255)	
		self.GREEN = (0,255,0)
		self.CYAN = (0,255,255)	
		self.width  = 20 #maze dimensions
		self.height = 20
		self.margin = 1	
		self.score = 0
		self.level = 1	
		self.num_wall = 0
		self.grid = []
		self.wall = []
		self.WALL = [[0 for i in range(1000)] for j in range(1000)] #2D array for wall
		#to store the intersections
		self.intersections = [(1,5),(4,3),(4,7),(3,5),(6,3),(6,5),(6,7),(13,3),(13,5),(13,7),(15,3),(15,7),(16,5),(18,5)]
		self.countfinal = 0
		self.make()
		self.size = [1200, 700]
		self.screen = pygame.display.set_mode(self.size)

	def make(self):
		#appending the coordinates of Walls in the array and list
		for i in range(0,20):
			self.wall.append([i,0])
			self.wall.append([i,10])
			self.WALL[i][0] = 1
			self.WALL[i][10] = 1
			self.num_wall += 2
		for j in range(0,11):
			self.wall.append([0,j])
			self.wall.append([19,j])
			self.WALL[0][j] = 1
			self.WALL[19][j] = 1
			self.num_wall += 2
		for j in range(1,3):
			self.wall.append([5,j])
			self.wall.append([14,j])
			self.WALL[5][j] = 1
			self.WALL[14][j] = 1
			self.num_wall += 2	
		for i in range(2,4):
			self.wall.append([i,2])
			self.WALL[i][2] = 1
			self.num_wall += 1
		for i in range(7,13):
			self.wall.append([i,2])
			self.WALL[i][2] = 1
			self.num_wall += 1
		for i in range(16,18):
			self.wall.append([i,2])
			self.WALL[i][2] = 1
			self.num_wall += 1
		for j in range(3,5):
			self.wall.append([2,j])
			self.wall.append([17,j])
			self.WALL[2][j] = 1
			self.WALL[17][j] = 1
			self.num_wall += 2
		for i in range(4,6):
			self.wall.append([i,4])
			self.wall.append([i,6])
			self.WALL[i][4] = 1
			self.WALL[i][6] = 1
			self.num_wall += 2
		for i in range(14,16):
			self.wall.append([i,4])
			self.wall.append([i,6])
			self.WALL[i][4] = 1
			self.WALL[i][6] = 1
			self.num_wall += 2
		for i in range(7,9):
			self.wall.append([i,4])
			self.WALL[i][4] = 1
			self.num_wall += 1
		for i in range(11,13):
			self.wall.append([i,4])
			self.WALL[i][4] = 1
			self.num_wall += 1
		for i in range(7,13):
			self.wall.append([i,6])
			self.WALL[i][6] = 1
			self.num_wall += 1
		self.wall.append([7,5])
		self.WALL[7][5] = 1
		self.wall.append([12,5])
		self.WALL[12][5] = 1
		self.num_wall += 2
		for j in range(6,8):
			self.wall.append([2,j])
			self.wall.append([17,j])
			self.WALL[2][j] = 1
			self.WALL[17][j] = 1
			self.num_wall += 2
		for i in range(7,13):
			self.wall.append([i,8])
			self.WALL[i][8] = 1
			self.num_wall += 1
		self.wall.append([2,8])
		self.WALL[2][8] = 1
		self.wall.append([3,8])
		self.WALL[3][8] = 1
		self.wall.append([16,8])
		self.WALL[16][8] = 1
		self.wall.append([17,8])
		self.WALL[17][8] = 1
		self.num_wall += 4
		for j in range(8,10):
			self.wall.append([5,j])
			self.wall.append([14,j])
			self.WALL[5][j] = 1
			self.WALL[14][j] = 1
			self.num_wall += 2
		for row in range(11):
			self.grid.append([])
			for column in range(20):
				self.grid[row].append(0)
		for wall in self.wall:
			self.grid[wall[1]][wall[0]]=1 	
		return self

	def reset(self): #to reset the game
		self.grid = []
		self.wall = []
		self.WALL = [[0 for i in range(1000)] for j in range(1000)]
		self.countfinal = 0
		self.make()	
		return self

	#the following functions are for drawing the respective objects
	def scoredisp(self):
	        scoretext=self.scorefont.render("Score: "+(str)(self.score), 1,self.WHITE)
	        self.screen.blit(scoretext, (30, 650))

	def leveldisp(self):
	        leveltext=self.scorefont.render("Level: "+(str)(self.level), 1,self.WHITE)
	        self.screen.blit(leveltext, (600, 650))

	def dispmaze(self):
		for row in range(11):
			for column in range(20):
				color = self.GREY
				pygame.draw.rect(self.screen,color,[(self.margin+self.width)*column+self.margin,(self.margin+self.height)*row+self.margin,self.width,self.height])
				color = self.GOLD
				if self.grid[row][column] == 1:
					self.countfinal=self.countfinal+1
				else:
					pygame.draw.rect(self.screen,color,[(self.margin+self.width)*column+self.margin+7,(self.margin+self.height)*row+self.margin+7,self.width-14,self.height-14])

	def drawwall(self):
		for wall in self.wall:
			pygame.draw.rect(self.screen,self.BLUE,[(self.margin+self.width)*wall[0]+self.margin,(self.margin+self.height)*wall[1]+self.margin,self.width,self.height])

class Object(Maze):

	def __init__(self,x,y):
		self.x = x	
		self.y = y
	
	def checkWall(self,x,y,W):
		if [x,y] in W:
			return True
		else:
			return False

	def moveleft(self,W):
		if self.x > 0:
			if self.checkWall(self.x-1,self.y,W):                
				self.x=self.x
			else:
				self.x=(self.x)-1
		return self		

	def moveright(self,W):
		if self.x < 19:
			if self.checkWall(self.x+1,self.y,W):
				self.x=self.x
			else:
				self.x=(self.x)+1
		return self

	def moveup(self,W):
		if self.y > 0:
			if self.checkWall(self.x,self.y-1,W):
				self.y=self.y
			else:
				self.y=(self.y)-1
		return self

	def movedown(self,W):
		if self.y < 10:
			if self.checkWall(self.x,self.y+1,W):
				self.y=self.y
			else:
				self.y=(self.y)+1
		return self

#inherits the functions of Object
class Pacman(Object):

	def __init__(self):
		x = 9
		y = 7
		self.dirc = -1;
		Object.__init__(self,x,y)
	
	def resetpacman(self):
		x = 9
		y = 7
		self.dirc = -1;
		Object.__init__(self,x,y)
	
	def collectCoin(self,Wa):
		if Wa.grid[self.y][self.x] == 0:
			return True
		else:
			return False

	def pacleft(self,Wa):
		Object.moveleft(self,Wa.wall)
		if self.collectCoin(Wa):	    
			Wa.grid[self.y][self.x]=1
			Wa.score += 1
		return self

	def pacright(self,Wa):
		Object.moveright(self,Wa.wall)
		if self.collectCoin(Wa):	    
			Wa.grid[self.y][self.x]=1
			Wa.score += 1
		return self

	def pacup(self,Wa):
		Object.moveup(self,Wa.wall)
		if self.collectCoin(Wa):	    
			Wa.grid[self.y][self.x]=1
			Wa.score += 1
		return self

	def pacdown(self,Wa):
		Object.movedown(self,Wa.wall)
		if self.collectCoin(Wa):	    
			Wa.grid[self.y][self.x]=1
			Wa.score += 1
		return self

	def draw(self,G):
		pygame.draw.rect(G.screen,G.GREEN,[(G.margin+G.width)*self.x+G.margin,(G.margin+G.height)*self.y+G.margin,G.width,G.height])

	def checkGhost(self,V):
		if [self.x,self.y] == [V.x,V.y]:
			return True
		else:
			return False

	def pacmove(self,G,action):
		# keys = pygame.key.get_pressed()
		# if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		# 	self.pacleft(G)
		# 	self.dirc = 0
		# elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		# 	self.pacright(G)
		# 	self.dirc = 1
		# elif keys[pygame.K_UP] or keys[pygame.K_w]:
		# 	self.pacup(G)
		# 	self.dirc = 2
		# elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
		# 	self.pacdown(G)
		# 	self.dirc = 3
		if action is 0:
			self.pacright(G)
			self.dirc = 1
		elif action is 1:
			self.pacleft(G)
			self.dirc = 0
		elif action is 2:
			self.pacup(G)
			self.dirc = 2
		elif action is 3:
			self.pacdown(G)
			self.dirc = 3

#The Red Ghost
class Blinky(Object,Pacman):

	def __init__(self):
		x = 9
		y = 3
		self.prev = -1
		self.speedlim = 0
		Object.__init__(self,x,y)
	
	def resetblinky(self):
		x = 9
		y = 3
		prev = 0
		Object.__init__(self,x,y)
		return self

	def bleft(self,Wa):
		Object.moveleft(self,Wa.wall)
		return self

	def bright(self,Wa):
		Object.moveright(self,Wa.wall)
		return self

	def bup(self,Wa):
		Object.moveup(self,Wa.wall)
		return self

	def bdown(self,Wa):
		Object.movedown(self,Wa.wall)
		return self

	def draw(self,G):
		pygame.draw.rect(G.screen,G.RED,[(G.margin+G.width)*self.x+G.margin,(G.margin+G.height)*self.y+G.margin,G.width,G.height])
 
	def blinkymove(self,G,pac):
		#if blinky not on intersection it has to follow the path
		if (self.x,self.y) not in G.intersections:
			if ([self.x-1,self.y] not in G.wall and self.prev != 1) :
				move = 0
			elif ([self.x+1,self.y] not in G.wall and self.prev != 0):
				move = 1
			elif ([self.x,self.y-1] not in G.wall and self.prev != 3):
				move = 2
			elif ([self.x,self.y+1] not in G.wall and self.prev != 2):
				move = 3
			self.prev = move
		else:
			#blinky moves to the tile from which the straight line distance from pacman is the least
			dist = [1000,1000,1000,1000]
			if [self.x-1,self.y] not in G.wall:
				dist[0] = math.sqrt((pac.x-self.x+1)*(pac.x-self.x+1)+(pac.y-self.y)*(pac.y-self.y))
			if [self.x+1,self.y] not in G.wall:
				dist[1] = math.sqrt((pac.x-self.x-1)*(pac.x-self.x-1)+(pac.y-self.y)*(pac.y-self.y))
			if [self.x,self.y-1] not in G.wall:
				dist[2] = math.sqrt((pac.x-self.x)*(pac.x-self.x)+(pac.y-self.y+1)*(pac.y-self.y+1))
			if [self.x,self.y+1] not in G.wall:
				dist[3] = math.sqrt((pac.x-self.x)*(pac.x-self.x)+(pac.y-self.y-1)*(pac.y-self.y-1))
			#print dist
			move = dist.index(min(dist))
			#print move
			self.prev = move
		if move == 0:
			self.bleft(G)
		elif move == 1:
			self.bright(G)
		elif move == 2:
			self.bup(G)
		elif move == 3:
			self.bdown(G)

#The blue ghost
class Inky(Object,Pacman):
    
	def __init__(self):
		x = 10
		y = 3
		self.prev = -1
		Object.__init__(self,x,y)
	
	def resetinky(self):
		x = 10
		y = 3
		self.prev = -1 
		Object.__init__(self,x,y)
		return self

	def ileft(self,Wa):
		Object.moveleft(self,Wa.wall)
		return self

	def iright(self,Wa):
		Object.moveright(self,Wa.wall)
		return self

	def iup(self,Wa):
		Object.moveup(self,Wa.wall)
		return self

	def idown(self,Wa):
		Object.movedown(self,Wa.wall)
		return self

	def draw(self,G):
		pygame.draw.rect(G.screen,G.CYAN,[(G.margin+G.width)*self.x+G.margin,(G.margin+G.height)*self.y+G.margin,G.width,G.height])
 
	def inkymove(self,G,pac):
		#if inky not on interection it has to follow the path
		if (self.x,self.y) not in G.intersections:
			if ([self.x-1,self.y] not in G.wall and self.prev != 1) :
				move = 0
			elif ([self.x+1,self.y] not in G.wall and self.prev != 0):
				move = 1
			elif ([self.x,self.y-1] not in G.wall and self.prev != 3):
				move = 2
			elif ([self.x,self.y+1] not in G.wall and self.prev != 2):
				move = 3
			self.prev = move
		else:
			#inky moves to the tile from which straight line distance to the target tile is the least
			#target tile is the second tile infront of pacman
			dist = [1000,1000,1000,1000]
			tx = 0
			ty = 0
			if pac.dirc is 2:
    				ty = pac.y
				tx = max(0,pac.x-2)
			elif pac.dirc is 0:
				ty = pac.y
				tx = min(19,pac.x+2)
			elif pac.dirc is 1:
				tx = pac.x
				ty = max(0,pac.y - 2)
			elif pac.dirc is 3:
				tx = pac.x
				ty = min(10,pac.y+2)
			if [self.x-1,self.y] not in G.wall:
				dist[0] = math.sqrt((tx-self.x+1)*(tx-self.x+1)+(ty-self.y)*(ty-self.y))
			if [self.x+1,self.y] not in G.wall:
				dist[1] = math.sqrt((tx-self.x-1)*(tx-self.x-1)+(ty-self.y)*(ty-self.y))
			if [self.x,self.y-1] not in G.wall:
				dist[2] = math.sqrt((tx-self.x)*(tx-self.x)+(ty-self.y+1)*(ty-self.y+1))
			if [self.x,self.y+1] not in G.wall:
				dist[3] = math.sqrt((tx-self.x)*(tx-self.x)+(ty-self.y-1)*(ty-self.y-1))
			#print dist
			move = dist.index(min(dist))
			#print move
			self.prev = move
		if move == 0:
			self.ileft(G)
		elif move == 1:
			self.iright(G)
		elif move == 2:
			self.iup(G)
		elif move == 3:
			self.idown(G)
