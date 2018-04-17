from network import *
from database import *
from classes import *
from featureExtractor import *
import tensorflow as tf
import numpy as np
import time
from scipy import misc
import gc 
import sys
import pygame

gc.enable()

par = { #parameters used for the program
	'ckpt_file':None,
	'num_episodes': 250000,
	'rms_decay':0.99,
	'rms_eps':1e-6,
	'db_size': 1000000, #database size for storing the state, next state, rewards and terminal values
	'batch': 32, #size of mini batch
	'num_act': 0,
	'input_dims' : [5],
	'input_dims_proc' : [5],
	'episode_max_length': 100000, #maximum length of a single episode
	'learning_interval': 1,
	'eps': 0.0,
	'eps_step':10000, #epsilon is decreased by this amount everytime
	'discount': 0.95, #discount value for updating the Q value
	'lr': 0.0002, #learning rate
	'save_interval':20, #model will be saved after this many iterations
	'train_start':20, #model will start training after this many iterations
	'eval_mode':False
}

class deep_pacman:
	def __init__(self,par):
		print 'Initializing Module...'
		self.par = par #to hold the parameters
		self.sess = tf.Session() #starting the session
		self.DB = database(self.par['db_size'], self.par['input_dims_proc']) 
		# self.engine = featureExtractor()
		# self.maze = MAZE()
		# self.pac = Pacman()
		# self.blinky = Blinky()
		# self.inky = Inky()
		self.par['num_act'] = 5 #number of possible actions
		self.build_nets() 
		self.Q_global = 0
		self.Q_temp = np.zeros(4) #to store Q_temp for every action
		self.state123 = np.zeros(5)
		self.cost_disp = 0 
		self.validactions = [] #if validactions[index] = 1, action corresponding to that index can't be taken

	def build_nets(self):
		print 'Building QNet and Targetnet...'
		self.qnet = network(self.par) #building the network		
	
	def start(self):
		print 'Start training...'
		cnt = self.qnet.sess.run(self.qnet.global_step)
		print 'Global step = ' + str(cnt)
		local_cnt = 0
		f1 = open("OUTPUT_1.txt","w+") #to write values for graph
		f2 = open("OUTPUT_2.txt","w+") 
		for numeps in range(self.par['num_episodes']):
			GAME = Maze() #declaring objects of the respective classes
			HERO = Pacman()
			VILLIAN = Blinky()
			VILLIAN2 = Inky()
			GAME.reset() #to initialize to new game state
			HERO.resetpacman()
			VILLIAN.resetblinky()
			VILLIAN2.resetinky()
			pygame.init()
			GAME.scorefont = pygame.font.Font(None,30)
			engine = featureExtractor()
			self.Q_global = 0
			state_proc = np.zeros((5)); state_proc_old = None; terminal = None; delay = 0; #to store current state to be used as old state
			state_proc = engine.newGame()
			total_reward_ep = 0
			s = time.time()	#to time for how long the agent was alive for a particular episode
			for maxl in range(self.par['episode_max_length']):
				GAME.dispmaze() #drawing the game elements
				GAME.drawwall() 
				HERO.draw(GAME)
				VILLIAN.draw(GAME)
				#VILLIAN2.draw(GAME)				
				if state_proc_old is not None: #if we have old state stored
					self.DB.insert(state_proc_old,reward,terminal,state_proc) #inserting the data in the database
				action = self.perceive(HERO,VILLIAN,VILLIAN2,GAME,engine,terminal) #function to select the action
				if action == 4:
					action = -1
				if action == None: #game over condition, break the loop, start new episode
					break				
				if local_cnt > self.par['train_start'] and local_cnt % self.par['learning_interval'] == 0:
					bat_s,bat_t,bat_n,bat_r = self.DB.get_batches(self.par['batch']) #retrieving mini batches from the database for training purposes
					cnt,self.cost_disp = self.qnet.train(bat_s,bat_t,bat_n,bat_r) #training the model
				if local_cnt > self.par['train_start'] and local_cnt % self.par['save_interval'] == 0:
					self.qnet.save_network('ckpt/model_'+str(cnt)) #saving the weights trained so far in the folder ckpt under the name model_iterationnumber
					print 'Model saved'
				
				state_proc_old = np.copy(state_proc) #copying the state in old state			
				state_proc = engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,action) #getting state features for current state
				reward, terminal = engine.next(HERO,VILLIAN,VILLIAN2,GAME,action) #performing the chosen action and saving reward
				total_reward_ep = total_reward_ep + reward
				local_cnt+=1
				self.par['eps'] = 0.0
				pygame.display.flip()
			#printing values for debugging
			sys.stdout.write("Epi: %d | frame: %d | train_step: %d | time: %f | reward: %f | eps: %f " % (numeps,local_cnt,cnt, time.time()-s, total_reward_ep,self.par['eps']))
			sys.stdout.write("| max_Q: %f\n" % (self.Q_global))			
			#sys.stdout.write("%f, %f, %f, %f, %f\n" % (self.t_e[0],self.t_e[1],self.t_e[2],self.t_e[3],self.t_e[4]))
			f1.write("%d, %d\n" % (numeps, GAME.score)) #writing score vs episode to build the graph
			f2.write("%d, %f\n" % (numeps, time.time() - s))
			f1.flush()
			f2.flush()
			sys.stdout.flush()
		f1.close() #closing the file
		f2.close()

	def perceive(self,HERO,VILLIAN,VILLIAN2,GAME,engine,terminal): #function outputs the action to be taken
		if not terminal:	
			#getting the valid actions
			self.validactions = engine.getValidActions(HERO,GAME)
			#choosing action acc. to epsilon greedy policy
			if np.random.rand() > self.par['eps']: #if random number is more than epsilon - exploitation
				#greedy with random tie-breaking
				'''Q_temp is a array which stores the Q values for every possible action from this state - return action for which Q_temp is max'''
				#storing the Q value obtained from the network in Q temp
				if self.validactions[0] == 1:
					self.state123 = engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,0)
					self.Q_temp[0] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: self.state123,self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
					engine.reward_update(self, HERO, VILLIAN, VILLIAN2, GAME, engine, 0)
				else:
					self.Q_temp[0] = -150
				if self.validactions[1] == 1:
					self.Q_temp[1] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,1),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
					engine.reward_update(self, HERO, VILLIAN, VILLIAN2, GAME, engine, 1)
				else:
					self.Q_temp[1] = -150
				if self.validactions[2] == 1:
					self.Q_temp[2] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,2),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
					engine.reward_update(self, HERO, VILLIAN, VILLIAN2, GAME, engine, 2)
				else:
					self.Q_temp[2] = -150
				if self.validactions[3] == 1:
					self.Q_temp[3] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,3),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
					engine.reward_update(self, HERO, VILLIAN, VILLIAN2, GAME, engine, 3)
				else:
					self.Q_temp[3] = -150
				'''self.Q_temp[4] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,-1),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check'''
				print self.Q_temp
				self.Q_global = max(self.Q_global,np.amax(self.Q_temp))
				#action with the maximum Q value is chosen
				action = self.Q_temp.tolist().index(max(self.Q_temp))
				return action
			else:
				#random action - exploration
				x = np.random.randint(0, 4) 
				while x != 4 and self.validactions[x] == 0:
					x = np.random.randint(0, 4)
				return x

if __name__ == "__main__":
	#using the saved model
	if len(sys.argv) > 1: 
		par['ckpt_file'] = sys.argv[1]
	da = deep_pacman(par)
	da.start() #starting the training
