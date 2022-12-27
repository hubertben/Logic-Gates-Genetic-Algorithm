
import random
import math
import copy

class Layer:

    def __init__(self, inputSize, outputSize, init_random = False):
        self.inputSize = inputSize
        self.outputSize = outputSize

        self.weights = [[0 for _ in range(outputSize)] for _ in range(inputSize)]
        self.biases = [0 for _ in range(outputSize)]

        if init_random:
            for i in range(inputSize):
                for j in range(outputSize):
                    self.weights[i][j] = random.random() * 2 - 1
            for j in range(outputSize):
                self.biases[j] = random.random() * 2 - 1


    def __str__(self):
        s = "\tWeights:\n"
        for i in range(self.inputSize):
            for j in range(self.outputSize):
                s += "\t * " + str(round(self.weights[i][j], 5)) + " "
            s += "\n"
        s += "\tBiases:\n"
        for j in range(self.outputSize):
            s += "\t * " + str(round(self.biases[j], 5)) + " "
        return s

    def __getitem__(self, key):
        i, j = key
        return self.weights[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self.weights[i][j] = value

    def _sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def _sigmoidList(self, x):
        return [self._sigmoid(x) for x in x]

    def forward(self, input):
        output = [0 for _ in range(self.outputSize)]
        for j in range(self.outputSize):
            for i in range(self.inputSize):
                output[j] += input[i] * self.weights[i][j]
            output[j] += self.biases[j]
        return self._sigmoidList(output)

    def copy(self):
        return copy.copy(self)


class Network:

    def __init__(self, layer_sizes, init_random = False):

        self.layer_sizes = layer_sizes
        self.layers = []

        for i in range(len(layer_sizes) - 1):
            self.layers.append(Layer(layer_sizes[i], layer_sizes[i + 1], init_random))


    def __str__(self):
        s = ""
        for i in range(len(self.layers)):
            s += "Layer " + str(i) + ":\n" + str(self.layers[i]) + "\n"
        return s

    def forward(self, input):
        for layer in self.layers:
            input = layer.forward(input)
        return input

    def copy(self):
        return copy.copy(self)