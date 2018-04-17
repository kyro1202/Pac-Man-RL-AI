import numpy as np
import gc
import time

class database:
	def __init__(self, size, input_dims):
		'''size stores the total size of the database
		counter is to keep track of overflow in size'''
		self.size = size 
		self.states = np.zeros([self.size,5],dtype='float')
		self.nextstates = np.zeros([self.size,5],dtype='float')
		self.terminals = np.zeros(self.size,dtype='float')
		self.rewards = np.zeros(self.size,dtype='float')
		self.counter = 0
		self.batch_counter = 0
		self.rand_idxs = np.arange(3,300)
		self.flag = False

	def get_four(self,idx):
		'''it returns the state nextstate reward terminal corresponding to the index in database'''
		four_s = np.zeros([5])
		four_n = np.zeros([5])
		four_s = self.states[idx]
		four_n = self.nextstates[idx]
		return four_s,self.terminals[idx],four_n,self.rewards[idx]

	def get_batches(self, bat_size):
		bat_s = np.zeros([bat_size,5])
		bat_t = np.zeros([bat_size])
		bat_n = np.zeros([bat_size,5])
		bat_r = np.zeros([bat_size])
		ss = time.time()
		#mini batches of data are formed from taking the jumbled data in the database
		for i in range(bat_size):
			if self.batch_counter >= len(self.rand_idxs) - bat_size :
				self.rand_idxs = np.arange(3,self.get_size()-1)
				np.random.shuffle(self.rand_idxs)
				self.batch_counter = 0
			s,t,n,r = self.get_four(self.rand_idxs[self.batch_counter])
			bat_s[i] = s; bat_t[i] = t; bat_n[i] = n; bat_r[i] = r
			self.batch_counter += 1

		e3 = time.time()-ss
		return bat_s,bat_t,bat_n,bat_r

	def insert(self, prevstate_proc,reward,terminal,newstate_proc): 
		#inserting the data in the database
		self.states[self.counter] = prevstate_proc
		self.nextstates[self.counter] = newstate_proc
		self.rewards[self.counter] = reward
		self.terminals[self.counter] = terminal

		self.counter += 1
		if self.counter >= self.size:
			self.flag = True
			self.counter = 0
		return

	def get_size(self):
		if self.flag == False:
			return self.counter
		else:
			return self.size
