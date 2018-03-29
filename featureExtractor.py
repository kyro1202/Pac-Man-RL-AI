import pygame
from classes import *
import math
import inspect
import heapq, random
import cStringIO
import numpy as np


class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

class featureExtractor:
	
	def Action(self, action):
		if action == -1:
			return [0, 0]
		elif action == 0:
			return [1, 0]
		elif action == 1:
			return [-1, 0]
		elif action == 2:
			return [0, -1]
		elif action == 3:
 			return [0, 1]

	def nextState(self, pac, blink, ink, g, action):
		pac.pacmove(g, action)
		blink.blinkymove(g, pac)
		#ink.inkymove(g, pac)
		
	def getBlinkyNewPos(self, pac, blink, G, action):
		## ACTION SHOULD BE VALID
		[dx, dy] = self.Action(action)
		if (blink.x, blink.y) not in G.intersections:
			if ([blink.x-1, blink.y] not in G.wall and blink.prev != 1) :
				move = 0
			elif ([blink.x+1, blink.y] not in G.wall and blink.prev != 0):
				move = 1
			elif ([blink.x, blink.y-1] not in G.wall and blink.prev != 3):
				move = 2
			elif ([blink.x, blink.y+1] not in G.wall and blink.prev != 2):
				move = 3
		else:
			dist = [1000,1000,1000,1000]
			if [blink.x-1, blink.y] not in G.wall:
				dist[0] = math.sqrt((pac.x + dx -blink.x+1)*(pac.x + dx -blink.x+1)+(pac.y + dy -blink.y)*(pac.y + dy -blink.y))
			if [blink.x+1, blink.y] not in G.wall:
				dist[1] = math.sqrt((pac.x + dx -blink.x-1)*(pac.x + dx -blink.x-1)+(pac.y + dy -blink.y)*(pac.y + dy -blink.y))
			if [blink.x,blink.y-1] not in G.wall:
				dist[2] = math.sqrt((pac.x + dx -blink.x)*(pac.x + dx -blink.x)+(pac.y + dy -blink.y+1)*(pac.y + dy -blink.y+1))
			if [blink.x,blink.y+1] not in G.wall:
				dist[3] = math.sqrt((pac.x + dx -blink.x)*(pac.x + dx - blink.x)+(pac.y + dy -blink.y-1)*(pac.y + dy -blink.y-1))
			#print dist
			move = dist.index(min(dist))
			#print move
		if move == 0:
			return [blink.x - 1, blink.y]
		elif move == 1:
			return [blink.x + 1, blink.y]
		elif move == 2:
			return [blink.x, blink.y - 1]
		elif move == 3:
			return [blink.x, blink.y + 1]

	def getInkyNewPos(self, pac, ink, G, action):
		## ACTION SHOULD BE VALID
		[dx, dy] = self.Action(action)
		'''if (ink.x,ink.y) not in G.intersections:
			if ([ink.x-1,ink.y] not in G.wall and ink.prev != 1) :
				move = 0
			elif ([ink.x+1,ink.y] not in G.wall and ink.prev != 0):
				move = 1
			elif ([ink.x,ink.y-1] not in G.wall and ink.prev != 3):
				move = 2
			elif ([ink.x,ink.y+1] not in G.wall and ink.prev != 2):
				move = 3
		else:
			dist = [1000,1000,1000,1000]
			tx = 0
			ty = 0
			if pac.dirc is 0:
				ty = pac.y
				tx = max(0,pac.x + dx -2)
			elif pac.dirc is 1:
				ty = pac.y
				tx = min(19,pac.x + dx +2)
			elif pac.dirc is 2:
				tx = pac.x
				ty = max(0,pac.y + dy - 2)
			elif pac.dirc is 3:
				tx = pac.x
				ty = min(10,pac.y + dy +2)
			if [ink.x-1,ink.y] not in G.wall:
				dist[0] = math.sqrt((tx-ink.x+1)*(tx-ink.x+1)+(ty-ink.y)*(ty-ink.y))
			if [ink.x+1,ink.y] not in G.wall:
				dist[1] = math.sqrt((tx-ink.x-1)*(tx-ink.x-1)+(ty-ink.y)*(ty-ink.y))
			if [ink.x,ink.y-1] not in G.wall:
				dist[2] = math.sqrt((tx-ink.x)*(tx-ink.x)+(ty-ink.y+1)*(ty-ink.y+1))
			if [ink.x,ink.y+1] not in G.wall:
				dist[3] = math.sqrt((tx-ink.x)*(tx-ink.x)+(ty-ink.y-1)*(ty-ink.y-1))
			#print dist
			move = dist.index(min(dist))
			#print move
		if move == 0:
			return [ink.x - 1, ink.y]
		elif move == 1:
			return [ink.x + 1, ink.y]
		elif move == 2:
			return [ink.x, ink.y - 1]
		elif move == 3:
			return [ink.x, ink.y + 1]'''
		return [10, 3]
		

	def getInkyDist(self, pac, ink, g, action):
		## ACTION SHOULD BE VALID
		## BFS
		visited = [[0 for i in range(1000)] for j in range(1000)]
		Q = Queue()
		dist = 0
		[dx, dy] = self.Action(action)
		Q.push([pac.x + dx, pac.y + dy, dist])
		visited[pac.x + dx][pac.y + dy] = 1
		if g.WALL[pac.x + dx][pac.y + dy] == 1:
			print pac.x, pac.y, action
		inky_x, inky_y = self.getInkyNewPos(pac, ink, g, action)
		while 1:
			[X, Y, DIST] = Q.pop()
			visited[X][Y] = 1
			if [X, Y] == [inky_x, inky_y]:
				return DIST
			if g.WALL[X + 1][Y] == 0 and visited[X + 1][Y] == 0:
				Q.push([X + 1, Y, DIST + 1])
			if g.WALL[X][Y + 1] == 0 and visited[X][Y + 1] == 0:
				Q.push([X, Y + 1, DIST + 1])
			if g.WALL[X - 1][Y] == 0 and visited[X - 1][Y] == 0:
				Q.push([X - 1, Y, DIST + 1])
			if g.WALL[X][Y - 1] == 0 and visited[X][Y - 1] == 0:
				Q.push([X, Y - 1, DIST + 1])
			if Q.isEmpty():
				print g.WALL[pac.x + dx][pac.y + dy], g.WALL[inky_x][inky_y]

	def getBlinkyDist(self, pac, blink, g, action):
		## ACTION SHOULD BE VALID
		## BFS
		visited = [[0 for i in range(1000)] for j in range(1000)]
		Q = Queue()
		dist = 0
		[dx, dy] = self.Action(action)
		Q.push([pac.x + dx, pac.y + dy, dist])
		visited[pac.x + dx][pac.y + dy] = 1
		if g.WALL[pac.x + dx][pac.y + dy] == 1:
			print pac.x, pac.y, action
		blinky_x, blinky_y = self.getBlinkyNewPos(pac, blink, g, action)
		while 1:
			[X, Y, DIST] = Q.pop()
			visited[X][Y] = 1
			if [X, Y] == [blinky_x, blinky_y]:
				return DIST
			if g.WALL[X + 1][Y] == 0 and visited[X + 1][Y] == 0:
				Q.push([X + 1, Y, DIST + 1])
			if g.WALL[X][Y + 1] == 0 and visited[X][Y + 1] == 0:
				Q.push([X, Y + 1, DIST + 1])
			if g.WALL[X - 1][Y] == 0 and visited[X - 1][Y] == 0:
				Q.push([X - 1, Y, DIST + 1])
			if g.WALL[X][Y - 1] == 0 and visited[X][Y - 1] == 0:
				Q.push([X, Y - 1, DIST + 1])
			if Q.isEmpty():
				print g.WALL[pac.x + dx][pac.y + dy], g.WALL[blinky_x][blinky_y]
	def getCoinDist(self, pac, g, action):
		## ACTION SHOULD BE VALID
		## BFS
		visited = [[0 for i in range(1000)] for j in range(1000)]
		Q = Queue()
		dist = 0
		[dx, dy] = self.Action(action)
		Q.push([pac.x + dx, pac.y + dy, dist])
		visited[pac.x + dx][pac.y + dy] = 1
		while 1:
			[X, Y, DIST] = Q.pop()
			visited[X][Y] = 1
			if g.grid[Y][X] == 0 and X != pac.x + dx and Y != pac.y + dy:
				return DIST
			if g.WALL[X + 1][Y] == 0 and visited[X + 1][Y] == 0:
				Q.push([X + 1, Y, DIST + 1])
			if g.WALL[X][Y + 1] == 0 and visited[X][Y + 1] == 0:
				Q.push([X, Y + 1, DIST + 1])
			if g.WALL[X - 1][Y] == 0 and visited[X - 1][Y] == 0:
				Q.push([X - 1, Y, DIST + 1])
			if g.WALL[X][Y - 1] == 0 and visited[X][Y - 1] == 0:
				Q.push([X, Y - 1, DIST + 1])
			if Q.isEmpty():
				return 0

	def getIntDist(self, pac, g, action):
		## ACTION SHOULD BE VALID
		## BFS
		visited = [[0 for i in range(1000)] for j in range(1000)]
		Q = Queue()
		dist = 0
		[dx, dy] = self.Action(action)
		Q.push([pac.x + dx, pac.y + dy, dist])
		visited[pac.x + dx][pac.y + dy] = 1
		while 1:
			[X, Y, DIST] = Q.pop()
			visited[X][Y] = 1
			if [X, Y] in g.intersections and X != pac.x + dx and Y != pac.y + dy:
				return DIST
			if g.WALL[X + 1][Y] == 0 and visited[X + 1][Y] == 0:
				Q.push([X + 1, Y, DIST + 1])
			if g.WALL[X][Y + 1] == 0 and visited[X][Y + 1] == 0:
				Q.push([X, Y + 1, DIST + 1])
			if g.WALL[X - 1][Y] == 0 and visited[X - 1][Y] == 0:
				Q.push([X - 1, Y, DIST + 1])
			if g.WALL[X][Y - 1] == 0 and visited[X][Y - 1] == 0:
				Q.push([X, Y - 1, DIST + 1])
			if Q.isEmpty():
				return 0

	def getProg(self, pac, g, action):
		## ACTION SHOULD BE VALID
		[dx, dy] = self.Action(action)
		if g.grid[pac.y + dy][pac.x + dx] == 0:
			return (g.score + 1)
		return g.score
		
	def getFeatures(self, pac, blink, ink, g, action):
		## ACTION SHOULD BE VALID
		if self.getBlinkyDist(pac, blink, g, action) == 0:
			blinky_dist = -1
		else:
			blinky_dist = 1/self.getBlinkyDist(pac, blink, g, action)
		if self.getInkyDist(pac, ink, g, action) == 0:
			inky_dist = -1
		else:
			inky_dist = 1/self.getInkyDist(pac, ink, g, action)
		if self.getCoinDist(pac, g, action) == 0:
			coin_dist = -1
		else:
			coin_dist = 1/self.getCoinDist(pac, g, action)
		if self.getIntDist(pac, g, action) == 0:
			int_dist = -1
		else:
			int_dist = 1/self.getIntDist(pac, g, action)
		prog = self.getProg(pac, g, action)/106
		return np.transpose([[blinky_dist], [inky_dist], [coin_dist], [int_dist], [prog]])

	def newGame(self):
		return [9, 10, 1, 3, 0] 
	
	def getValidActions(self, pac, g):
		right = 1
		left = 1
		down = 1
		up = 1
		if g.WALL[pac.x + 1][pac.y] == 1:
			right = 0
		if g.WALL[pac.x - 1][pac.y] == 1:
			left = 0
		if g.WALL[pac.x][pac.y + 1] == 1:
			down = 0
		if g.WALL[pac.x][pac.y - 1] == 1:
			up = 0
		return [right, left, up, down]
	
	def next(self, pac, blink, ink, g, action):
		terminal = 0
		[dx, dy] = self.Action(action)
		
		if [pac.x + dx, pac.y + dy] == self.getBlinkyNewPos(pac, blink, g, action) or [pac.x + dx, pac.y + dy] == [blink.x, blink.y]:
			self.nextState(pac, blink, ink, g, action)
			return [-100.0, 1.0]
		if self.getProg(pac, g, action) == 106:
			self.nextState(pac, blink, ink, g, action)
			return [100.0, 1.0]
		if self.getProg(pac, g, action) == g.score + 1:
			self.nextState(pac, blink, ink, g, action)
			return [20.0, 0.0]
		if self.getProg(pac, g, action) == g.score:
			self.nextState(pac, blink, ink, g, action)
			return [-5.0, 0.0]
		
	'''def dispInky(self, pac, ink, g):
		distext = g.scorefont.render("Inky Distance: "+(str)(self.getInkyDist(pac, ink, g, 0)), 1, g.WHITE)
       		g.screen.blit(distext, (280, 610))
	def dispBlinky(self, pac, blink, g):
		distext = g.scorefont.render("Blinky Distance: "+(str)(self.getBlinkyDist(pac, blink, g, 0)), 1, g.WHITE)
       		g.screen.blit(distext, (280, 630))
	def dispCoin(self, pac, g):
		distext = g.scorefont.render("Coin Distance: "+(str)(self.getCoinDist(pac, g, 0)), 1, g.WHITE)
       		g.screen.blit(distext, (280, 650))
	def dispDir(self, pac, g):
		distext = g.scorefont.render("Coin Direction: "+(str)(self.getDirToCoin(pac, g, 0)), 1, g.WHITE)
       		g.screen.blit(distext, (280, 670))'''




