import math
import pylab as pl
import numpy as np


class MatrixOP:
	def __init__(self):
		pass

	@staticmethod
	def apply(matrix, fn):
		for x in np.nditer(matrix, op_flags=['readwrite']):
			x[...] = fn(x)

	@staticmethod
	def pipe(matrix, fn):
		newMatrix = np.copy(matrix)
		for x in np.nditer(newMatrix, op_flags=['readwrite']):
			x[...] = fn(x)

		return newMatrix
 
class ActivationFunction:
	def __init__(self, activate, derInY, derivative):
		self.activate = activate

		# derivative in y or x expression
		self.derInY = derInY 
		self.derivative = derivative

class Layer:
	def __init__(self, preSize, mySize, nnFun):
		self.size = mySize
		self.neurons = np.zeros((mySize, 1), dtype=float) 
		self.outputs = np.zeros((mySize, 1), dtype=float)

		magicNumber = np.sqrt(float(6) / float(preSize + mySize));
		self.weight = (np.random.random((mySize, preSize)) - 0.5) * magicNumber  #np.zeros((mySize, preSize), dtype=float)
		# self.weight = 2 * self.weight - 1
		self.bias = np.zeros((mySize, 1), dtype=float) #np.zeros((mySize, 1), dtype=float)
		# self.bias = 2 * self.bias - 1
		# self.weight = np.zeros((mySize, preSize), dtype=float)
		# self.bias = np.zeros((mySize, 1), dtype=float)

		self.nnFun = nnFun

	def receiveSignal(self, signals):
		self.neurons = np.dot(self.weight, signals) + self.bias
		
		self.outputs = MatrixOP.pipe(self.neurons, self.nnFun.activate)
		# print("neurons:")
		# print(self.neurons)
		# print("outputs:")
		# print(self.outputs)

	def dspreceiveSignal(self, signals):
		self.neurons = np.dot(self.weight, signals) + self.bias
		print("self.weight\n", self.weight)
		print("self.neurons\n", self.neurons)
		self.outputs = MatrixOP.pipe(self.neurons, self.nnFun.activate)
		# print("neurons:")
		# print(self.neurons)
		# print("outputs:")
		# print(self.outputs)

	def getDiagDerivativeMatrix(self):
		
		diags = None

		if self.nnFun.derInY == True:
			diags = np.copy(self.outputs)	
			MatrixOP.apply(diags, self.nnFun.derivative)
		else:
			diags = np.copy(self.neurons)
			MatrixOP.apply(diags, self.nnFun.derivative)

		if diags.shape == (1, 1):
			return diags
		
		return np.diag(np.squeeze(np.asarray(diags)))
		

	def learnWeight(self, adjust):
		self.weight = self.weight + adjust;

	def learnBias(self, adjust):
		self.bias = self.bias + adjust;


class Network:
	"""NN"""
	def __init__(self, sizeOfLayers, activationFunctions):

		""" sizeOfLayers 
			#0 -> input size

			#last -> output size
		"""


		# L
		self.nnDepth = len(sizeOfLayers)
		self.outputIndex = self.nnDepth - 1

		self.sizeOfLayers = sizeOfLayers
		
	