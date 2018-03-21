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
        