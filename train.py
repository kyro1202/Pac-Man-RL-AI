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

par = {
	'ckpt_file':None,
	'num_episodes': 250000,
	'rms_decay':0.99,
	'rms_eps':1e-6,
	'db_size': 1000000,
	'batch': 32,
	'num_act': 0,
	'input_dims' : [5],
	'input_dims_proc' : [5],
	'episode_max_length': 100000,
	'learning_interval': 1,
	'eps': 0.7,
	'eps_step':10000,
	'discount': 0.95,
	'lr': 0.0002,
	'save_interval':20,
	'train_start':20,
	'eval_mode':False
}

class deep_pacman:
	def __init__(self,par):
		print 'Initializing Module...'
		self.par = par
		self.sess = tf.Session()
		self.DB = database(self.par['db_size'], self.par['input_dims_proc'])
		# self.engine = featureExtractor()
		# self.maze = MAZE()
		# self.pac = Pacman()
		# self.blinky = Blinky()
		# self.inky = Inky()
		self.par['num_act'] = 5
		self.build_nets()
		self.Q_global = 0
		self.Q_temp = np.zeros(5)
		self.cost_disp = 0
		self.validactions = []

	def build_nets(self):
		print 'Building QNet and Targetnet...'
		self.qnet = network(self.par)		
	
	def start(self):
		print 'Start training...'
		cnt = self.qnet.sess.run(self.qnet.global_step)
		print 'Global step = ' + str(cnt)
		local_cnt = 0
		s = time.time()		
		for numeps in range(self.par['num_episodes']):
			GAME = Maze()
			HERO = Pacman()
			VILLIAN = Blinky()
			VILLIAN2 = Inky()
			GAME.reset()
			HERO.resetpacman()
			VILLIAN.resetblinky()
			VILLIAN2.resetinky()
			pygame.init()
			GAME.scorefont = pygame.font.Font(None,30)
			engine = featureExtractor()
			self.Q_global = 0
			state_proc = np.zeros((5)); state_proc_old = None; terminal = None; delay = 0;
			state_proc = engine.newGame()
			total_reward_ep = 0
			for maxl in range(self.par['episode_max_length']):
				GAME.dispmaze()
				GAME.drawwall() 
				HERO.draw(GAME)
				VILLIAN.draw(GAME)
				#VILLIAN2.draw(GAME)				
				if state_proc_old is not None:
					self.DB.insert(state_proc_old,reward,terminal,state_proc)
				action = self.perceive(HERO,VILLIAN,VILLIAN2,GAME,engine,terminal)
				if action == 4:
					action = -1
				if action == None: #TODO - check [terminal condition]
					break				
				if local_cnt > self.par['train_start'] and local_cnt % self.par['learning_interval'] == 0:
					bat_s,bat_t,bat_n,bat_r = self.DB.get_batches(self.par['batch'])
					cnt,self.cost_disp = self.qnet.train(bat_s,bat_t,bat_n,bat_r)
				if local_cnt > self.par['train_start'] and local_cnt % self.par['save_interval'] == 0:
					self.qnet.save_network('ckpt/model_'+str(cnt))
					print 'Model saved'
				
				state_proc_old = np.copy(state_proc)			
				state_proc = engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,action) 
				reward, terminal = engine.next(HERO,VILLIAN,VILLIAN2,GAME,action) #IMP: newstate contains terminal info
				total_reward_ep = total_reward_ep + reward
				local_cnt+=1	
				self.par['eps'] = max(0.2,1.0 - float(cnt)/float(self.par['eps_step']))
				pygame.display.flip()

			sys.stdout.write("Epi: %d | frame: %d | train_step: %d | time: %f | reward: %f | eps: %f " % (numeps,local_cnt,cnt, time.time()-s, total_reward_ep,self.par['eps']))
			sys.stdout.write("| max_Q: %f\n" % (self.Q_global))			
			#sys.stdout.write("%f, %f, %f, %f, %f\n" % (self.t_e[0],self.t_e[1],self.t_e[2],self.t_e[3],self.t_e[4]))
			sys.stdout.flush()
			

	def perceive(self,HERO,VILLIAN,VILLIAN2,GAME,engine,terminal):
		if not terminal:				
			self.validactions = engine.getValidActions(HERO,GAME)
			if np.random.rand() > self.par['eps']:
				#greedy with random tie-breaking
				'''Q_temp is a array which stores the Q values for every possible action from this state - return action for which Q_temp is max'''
				if self.validactions[0] == 1:
					self.Q_temp[0] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,0),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
				else:
					self.Q_temp[0] = -150
				if self.validactions[1] == 1:
					self.Q_temp[1] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,1),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
				else:
					self.Q_temp[1] = -150
				if self.validactions[2] == 1:
					self.Q_temp[2] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,2),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
				else:
					self.Q_temp[2] = -150
				if self.validactions[3] == 1:
					self.Q_temp[3] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,3),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
				else:
					self.Q_temp[3] = -150
				self.Q_temp[4] = self.qnet.sess.run(self.qnet.y, feed_dict = {self.qnet.x: engine.getFeatures(HERO,VILLIAN,VILLIAN2,GAME,-1),self.qnet.q_value: np.zeros(1) , self.qnet.rewards: np.zeros(1)})[0] #TODO check
				self.Q_global = max(self.Q_global,np.amax(self.Q_temp))
				action = self.Q_temp.tolist().index(max(self.Q_temp))
				return action
			else:
				x = np.random.randint(0, 5)
				while x != 4 and self.validactions[x] == 0:
					x = np.random.randint(0, 5)
				return x

if __name__ == "__main__":
	if len(sys.argv) > 1:
		par['ckpt_file'] = sys.argv[1]
	da = deep_pacman(par)
	da.start()
