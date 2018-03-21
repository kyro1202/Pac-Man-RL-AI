import numpy as np
import tensorflow as tf
from featureExtractor import *

class network:
    def __init__(self,par):
        self.par = par
        self.name = 'net'
        self.sess = tf.Session()
        self.x = tf.placeholder(tf.float32,[None,5],name=self.name + '_x')
        self.q_value = tf.placeholder(tf.float32,[None],name=self.name + '_q_value')
        self.actions = tf.placeholder(tf.float32,[None,par['num_act']],name=self.name + '_actions')
        self.rewards = tf.placeholder(tf.float32,[None],name=self.name + '_rewards')
        self.terminals = tf.placeholder(tf.float32, [None],name=self.name + '_terminals')

        #layer1
        layer_name = 'layer1'; size1 = 5; size2 = 10; 
        self.w1 = tf.Variable(tf.random_normal([size1,size2],stddev=0.01),name=self.name + '_' + layer_name + '_weights')
        self.b1 = tf.Variable(tf.constant(0.1, shape=[size2]),name=self.name + '_'+layer_name+'_biases')
        self.z1 = tf.add(tf.matmul(self.x,self.w1),self.b1)
        self.o1 = tf.nn.relu(self.z1,name=self.name + '_'+layer_name+'_activations')

        #layer2
        layer_name = 'layer2'; size1 = 10; size2 = 1; 
        self.w2 = tf.Variable(tf.random_normal([size1,size2],stddev=0.01),name=self.name + '_' + layer_name + '_weights')
        self.b2 = tf.Variable(tf.constant(0.1, shape=[size2]),name=self.name + '_'+layer_name+'_biases')
        self.z2 = tf.add(tf.matmul(self.o1,self.w2),self.b2)
        self.y = tf.nn.relu(self.z2,name=self.name + '_outputs')

        #Q,cost,optimizer
        self.discount = tf.constant(self.par['discount'])
        self.y_updated = tf.add(self.rewards, tf.mul(1.0-self.terminals, tf.mul(self.discount, self.q_value)))
        self.Q_pred = tf.reduce_sum(tf.mul(self.y,self.actions), reduction_indices=1)
        self.cost = tf.reduce_sum(tf.pow(tf.sub(self.y_updated, self.Q_pred), 2))
        if self.par['ckpt_file'] is not None:
            self.global_step = tf.Variable(int(self.par['ckpt_file'].split('_')[-1]),name='global_step', trainable=False)
		else:
			self.global_step = tf.Variable(0, name='global_step', trainable=False)
        self.rmsprop = tf.train.RMSPropOptimizer(self.par['lr'],self.par['rms_decay'],0.0,self.par['rms_eps']).minimize(self.cost,global_step=self.global_step)
        self.saver = tf.train.Saver()
        self.sess.run(tf.global_variables_initializer())
        if self.par['ckpt_file'] is not None:
            print 'loading checkpoint...'
            self.saver.restore(self.sess,self.par['ckpt_file'])

    def train(self,bat_s,bat_a,bat_t,bat_n,bat_r):
        feed_dict={self.x: bat_n, self.q_value: np.zeros(bat_n.shape[0]), self.actions: bat_a, self.terminals: bat_t, self.rewards: bat_r}
        q_value = self.sess.run(self.y,feed_dict = feed_dict)
        q_value = np.amax(q_value,axis = 1)
        feed_dict={self.x: bat_s, self.q_value: q_value, self.actions: bat_a, self.terminals:bat_t, self.rewards: bat_r}
        _,cnt,cost = self.sess.run([self.rmsprop,self.global_step,self.cost],feed_dict=feed_dict)
        return cnt,cost

    def save_network(self,filename):
        self.saver.save(self.sess,filename)