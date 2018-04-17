import numpy as np
import tensorflow as tf
from featureExtractor import *

class network:
	def __init__(self,par):
		#name of the network is net
		self.par = par
		self.name = 'net'
		#starting the session
		self.sess = tf.Session()
		#x holds the input features
		self.x = tf.placeholder(tf.float32,[None,5],name=self.name + '_x')
		#q_value is used to compute the cost
		self.q_value = tf.placeholder(tf.float32,[None],name=self.name + '_q_value')
		self.rewards = tf.placeholder(tf.float32,[None],name=self.name + '_rewards')
		self.terminals = tf.placeholder(tf.float32, [None],name=self.name + '_terminals')

		#layer1
		'''layer 1 uses 10 hidden units 
			and Relu function for activation'''
		layer_name = 'layer1'; size1 = 5; size2 = 10; 
		self.w1 = tf.Variable(tf.random_normal([size1,size2],stddev=0.01),name=self.name + '_' + layer_name + '_weights')
		self.b1 = tf.Variable(tf.constant(0.1, shape=[size2]),name=self.name + '_'+layer_name+'_biases')
		self.z1 = tf.add(tf.matmul(self.x,self.w1),self.b1)
		self.o1 = tf.nn.relu(self.z1,name=self.name + '_'+layer_name+'_activations')

		#layer2
		'''layer2 produces output and 
		uses ReLu function for activation'''
		layer_name = 'layer2'; size1 = 10; size2 = 1; 
		self.w2 = tf.Variable(tf.random_normal([size1,size2],stddev=0.01),name=self.name + '_' + layer_name + '_weights')
		self.b2 = tf.Variable(tf.constant(0.1, shape=[size2]),name=self.name + '_'+layer_name+'_biases')
		self.z2 = tf.add(tf.matmul(self.o1,self.w2),self.b2)
		self.y = tf.nn.relu(self.z2,name=self.name + '_outputs')

		#Q,cost,optimizer
		#discount value for updating the Q values
		self.discount = tf.constant(self.par['discount'])
		# Q = Rewards + (1-terminal)*Discount*max(Q_nextstate)
		self.y_updated = tf.add(self.rewards, tf.multiply(1.0-self.terminals, tf.multiply(self.discount, self.q_value)))
		self.Q_pred = tf.reduce_sum(self.y, reduction_indices=1)
		# cost = (Q - Q_predicted)^2
		self.cost = tf.reduce_sum(tf.pow(tf.subtract(self.y_updated, self.Q_pred), 2))
		if self.par['ckpt_file'] is not None:
			self.global_step = tf.Variable(int(self.par['ckpt_file'].split('_')[-1]),name='global_step', trainable=False)
		else:
			self.global_step = tf.Variable(0, name='global_step', trainable=False)
		#to train the model RMSprop is used
		self.rmsprop = tf.train.RMSPropOptimizer(self.par['lr'],self.par['rms_decay'],0.0,self.par['rms_eps']).minimize(self.cost,global_step=self.global_step)
		self.saver = tf.train.Saver()
		self.sess.run(tf.global_variables_initializer())
		if self.par['ckpt_file'] is not None:
			print 'loading checkpoint...'
			self.saver.restore(self.sess,self.par['ckpt_file']) #saving the network

	def train(self,bat_s,bat_t,bat_n,bat_r):
		'''training the network 
		inputs to the network are given using feed_dict'''
		feed_dict={self.x: bat_n, self.q_value: np.zeros(bat_n.shape[0]), self.terminals: bat_t, self.rewards: bat_r}
		q_value = self.sess.run(self.y,feed_dict = feed_dict)
		q_value = np.amax(q_value,axis = 1)
		feed_dict={self.x: bat_s, self.q_value: q_value, self.terminals:bat_t, self.rewards: bat_r}
		_,cnt,cost = self.sess.run([self.rmsprop,self.global_step,self.cost],feed_dict=feed_dict)
		return cnt,cost

	def save_network(self,filename):
		#to save the network
		self.saver.save(self.sess,filename)
