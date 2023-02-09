
# from network import *
from gates import *

class Solvers:

    def __init__(self, iD, truthtable, allowedGates, inputCount, outputCount):
        self.truthtable = truthtable
        self.allowedGates = allowedGates
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.iD = iD

        self.inputPins = [Pin(i, label = "Input Pin " + str(i)) for i in range(inputCount)]
        self.outputPins = [Pin(i, label = "Output Pin " + str(i)) for i in range(outputCount)]

        self.fitness = 0
        self.circuit = []
        

    def arange(self, firstPass = False):

        if firstPass != False:   
            # determine a list of all connections which need to be made:
                # A list from all inputs to all input pins on all gates (besides thier own)
                # A list from all output pins on all gates to all outputs (besides thier own)
                # From all Input Pins to all input pins on all gates 
                # From all Output pins to all output pins on all gates

            # Connect a certin percentage of them randomly based on "firstPass" (a percentage)
            # Return the list of connections made
            pass

        else:
            # Reconnect the list of connections made in the first pass based on the fitness of the circuit
                # It should be as the fitness increases, the less reconnections are made

            # Return the list of connections made
            pass

    def determineFitness(self, inputPins, outputPins, basetable):
        pass

    def mutate(self, mutationRate = .01):
        pass




class Solve:

    def __init__(self, truthtable, allowedGates, solverCount):
        self.truthtable = truthtable
        self.allowedGates = allowedGates

        self.group = [Solvers(i, truthtable, allowedGates) for i in range(solverCount)]

    def singlePass(self, allowedSolutionsAsPercentage = .1):

        for i in self.group:
            i.arange()
            i.determineFitness()

        self.group.sort(key=lambda x: x.fitness, reverse=True)

        p = int(len(self.group) * allowedSolutionsAsPercentage)
        return self.group[:p]

    def mutate(self, desiredGroupSize):
        
        while len(self.group) < desiredGroupSize:
            pass

    def solve(self, evolv = 100):

        for i in range(evolv):
            self.group = self.singlePass()

        return self.group[0]

        