from django.apps import AppConfig
from tensorflow.keras.utils import CustomObjectScope
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from tensorflow.keras import initializers, regularizers, constraints
from tensorflow.keras.layers import Layer
from django.urls import path
import os

class Attention(Layer):
	def __init__(self, step_dim,
				 W_regularizer=None, b_regularizer=None,
				 W_constraint=None, b_constraint=None,
				 bias=True, **kwargs):
 
		self.supports_masking = True
		self.init = initializers.get('glorot_uniform')

		self.W_regularizer = regularizers.get(W_regularizer)
		self.b_regularizer = regularizers.get(b_regularizer)

		self.W_constraint = constraints.get(W_constraint)
		self.b_constraint = constraints.get(b_constraint)

		self.bias = bias
		self.step_dim = step_dim
		self.features_dim = 0
		super(Attention, self).__init__(**kwargs)

	def get_config(self):
		config = super().get_config().copy()
		config.update({
				#'supports_masking':self.supports_masking,
				#'init':self.init,
				'W_regularizer': self.W_regularizer,
				'b_regularizer': self.b_regularizer,
				'W_constraint': self.W_constraint,
				'b_constraint': self.b_constraint,
				'bias': self.bias,
				'step_dim':self.step_dim,
				#'features_dim':self.features_dim,
		})
		return config

	def build(self, input_shape):
		assert len(input_shape) == 3

		self.W = self.add_weight(shape=(input_shape[-1],),
								 initializer=self.init,
								 name='{}_W'.format(self.name),
								 regularizer=self.W_regularizer,
								 constraint=self.W_constraint)
		self.features_dim = input_shape[-1]

		if self.bias:
			self.b = self.add_weight(shape=(input_shape[1],),
									 initializer='zero',
									 name='{}_b'.format(self.name),
									 regularizer=self.b_regularizer,
									 constraint=self.b_constraint)
		else:
			self.b = None

		self.built = True

	def compute_mask(self, input, input_mask=None):
		return None

	def call(self, x, mask=None):

		features_dim = self.features_dim
		step_dim = self.step_dim

		eij = K.reshape(K.dot(K.reshape(x, (-1, features_dim)), K.reshape(self.W, (features_dim, 1))), (-1, step_dim))

		if self.bias:
			eij += self.b

		eij = K.tanh(eij)
		a = K.exp(eij)
		a /= K.cast(K.sum(a, axis=1, keepdims=True) + K.epsilon(), K.floatx())

		a = K.expand_dims(a)
		weighted_input = x * a
		return K.sum(weighted_input, axis=1)

	def compute_output_shape(self, input_shape):
		return input_shape[0],  self.features_dim

class NamegeneratorConfig(AppConfig):

	def __init__(self, model_name):

		self.PRETRAINED_MODEL = "ImageCaptioning/models/{}".format(model_name)
		
	def model(self):
		with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
			model = load_model(self.PRETRAINED_MODEL, 
				custom_objects={'Attention':Attention})

		return model