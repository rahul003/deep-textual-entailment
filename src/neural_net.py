import numpy as np
from abc import ABCMeta, abstractmethod
from keras.models import load_model
import math

class NeuralNet:
	__metaclass__ = ABCMeta

	def __init__(self, data, num_targets, lstm_size=20, dense_size=32, dense_activation='relu',batch_size=10000, num_epochs=50):
		self.data = data
		self.num_targets = num_targets
		self.maxLengths = data.getMaxLengths()

		self.dense_activation = dense_activation
		self.lstm_size = lstm_size
		self.dense_size = dense_size
		self.batch_size = batch_size
		self.num_epochs = num_epochs

		self.train_size = len(self.data.data['X']['train'])
		self.test_size = len(self.data.data['X']['test'])

		self.print_params()
	
	def print_params(self):
		print 'lstm_size:',self.lstm_size
		print 'dense_size:',self.dense_size
		print 'dense_activation:', self.dense_activation
		print 'batch_size:',self.batch_size
		print 'num_epochs:',self.num_epochs

		print 'train_size:',self.train_size
		print 'test_size:',self.test_size
	
	def train(self):
		self.build_model()
		self.model.fit_generator(self.batch_generator('train'), self.train_size, self.num_epochs)

	def test(self):
		print self.model.evaluate_generator(self.batch_generator('test'), self.test_size)

	@abstractmethod
	def build_model(self):
		pass

	def load_model(self,path):
		self.model = load_model(path)

	def retrain(self, num_epochs):
		self.model.fit_generator(self.batch_generator('train'), self.train_size, num_epochs)

	def load_retrain(self, path, num_epochs):
		self.load_model(path)
		self.retrain(num_epochs)
		
	@abstractmethod
	def sequence_padding(self, data):
		pass

	def batch_generator(self, dataset):	
		y = self.data.getY(dataset)
		while True:
			for i in range(int(math.ceil(len(y)/float(self.batch_size)))):
				start_index = (i*self.batch_size)
				end_index = ((i+1)*self.batch_size)
				if end_index>len(y):
					end_index = len(y)
				yield (self.sequence_padding(self.data.getX(dataset, start_index, end_index)), self.data.getY(dataset,start_index,end_index))

