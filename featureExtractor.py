import pygame
from classes import *
import math
import inspect
import heapq, random
import cStringIO


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

	def getInkyDist(self, pac, ink, g):
		## BFS
		visited = [[0 for i in range(1000)] for j in range(1000)]
		Q = Queue()
		dist = 0
		Q.push([pac.x, pac.y, dist])
		visited[pac.x][pac.y] = 1
		while 1:
			[X, Y, DIST] = Q.pop()
			visited[X][Y] = 1
			if [X, Y] == [ink.x, ink.y]:
				return DIST
			if [X + 1, Y] not in g.wall and visited[X + 1][Y] == 0:
				Q.push([X + 1, Y, DIST + 1])
			if [X, Y + 1] not in g.wall and visited[X][Y + 1] == 0:
				Q.push([X, Y + 1, DIST + 1])
			if [X - 1, Y] not in g.wall and visited[X - 1][Y] == 0:
				Q.push([X - 1, Y, DIST + 1])
			if [X, Y - 1] not in g.wall and visited[X][Y - 1] == 0:
				Q.push([X, Y - 1, DIST + 1])

	def getBlinkyDist(self, pac, blink, g):
		## BFS
		visited = [[0 for i in range(1000)] for j in range(1000)]
		Q = Queue()
		dist = 0
		Q.push([pac.x, pac.y, dist])
		visited[pac.x][pac.y] = 1
		while 1:
			[X, Y, DIST] = Q.pop()
			visited[X][Y] = 1
			if [X, Y] == [blink.x, blink.y]:
				return DIST
			if [X + 1, Y] not in g.wall and visited[X + 1][Y] == 0:
				Q.push([X + 1, Y, DIST + 1])
			if [X, Y + 1] not in g.wall and visited[X][Y + 1] == 0:
				Q.push([X, Y + 1, DIST + 1])
			if [X - 1, Y] not in g.wall and visited[X - 1][Y] == 0:
				Q.push([X - 1, Y, DIST + 1])
			if [X, Y - 1] not in g.wall and visited[X][Y - 1] == 0:
				Q.push([X, Y - 1, DIST + 1])

	def dispInky(self, pac, ink, g):
		distext = g.scorefont.render("Inky Distance: "+(str)(self.getInkyDist(pac, ink, g)), 1, g.WHITE)
       		g.screen.blit(distext, (280, 630))
	def dispBlinky(self, pac, blink, g):
		distext = g.scorefont.render("Blinky Distance: "+(str)(self.getBlinkyDist(pac, blink, g)), 1, g.WHITE)
       		g.screen.blit(distext, (280, 670))




