
# from network import *
from gates import *
import random

class Solvers:

    def __init__(self, iD, truthtable, allowedGates, inputCount, outputCount):
        self.truthtable = truthtable
        self.allowedGates = allowedGates
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.iD = iD

        

        self.fitness = 0
        self.circuit = []

    def __repr__(self):
        print("Solver " + str(self.iD) + " Fitness: " + str(self.fitness))
        return ""
        

    def arange(self, inputConnections, outputConnections, firstPass = False):

        if firstPass != False:   
            # determine a list of all connections which need to be made:
                # A list from all inputs to all input pins on all gates (besides thier own)
                # A list from all output pins on all gates to all outputs (besides thier own)
                # From all Input Pins to all input pins on all gates 
                # From all Output pins to all output pins on all gates

            # Connect a certin percentage of them randomly based on "firstPass" (a percentage)
            # Return the list of connections made

            print(inputConnections)
            print(outputConnections)
            pass

            totalNumberOfConnections = len(inputConnections) * len(outputConnections)
            numberOfConnections = random.randint(int(totalNumberOfConnections * .1), int(totalNumberOfConnections * .9))
        

            connections = []


            rules = [
                ["Input Pin", "Output Pin"],
                ["Input Pin", "Input Pin (Gate)"],
                ["Output Pin (Gate)", "Output Pin"],
                ["Output Pin (Gate)", "Input Pin (Gate)"]
            ]

            

            def generatePinPair():

                input_ = None
                output_ = None

                rule = random.choice(rules)

                if rule[0] == "Input Pin":
                    while True:
                        input_ = random.choice(inputConnections)
                        if type(input_[0]) == Pin:
                            break

                elif rule[0] == "Output Pin (Gate)":

                    while True:
                        input_ = random.choice(outputConnections)
                        if type(input_[0]) != Pin:
                            break

                

                if rule[1] == "Output Pin":
                    while True:
                        output_ = random.choice(outputConnections)
                        if type(output_[0]) == Pin:
                            break

                elif rule[1] == "Input Pin (Gate)":
                    while True:
                        output_ = random.choice(inputConnections)
                        if type(output_[0]) != Pin:
                            break   

                

                return input_, output_


            c = 0
            for i in range(numberOfConnections):

                input_ = None
                output_ = None

                while True:

                    c += 1

                    if c > 100:
                        # print("Failed to generate a valid connection")
                        break

                    input_, output_ = generatePinPair()
                    if input_[0] != output_[0] and [input_, output_] not in connections and [output_, input_] not in connections:
                        break

                # print(input_, output_, "")

                input_[0].addConnection(input_[1], output_[0], output_[1])
    
                connections.append([input_, output_])

            print("Connections:")
            for i in connections:
                print(i[0][0], i[0][1], " -> ", i[1][0], i[1][1])
            return

        else:
            # Reconnect the list of connections made in the first pass based on the fitness of the circuit
                # It should be as the fitness increases, the less reconnections are made

            # Return the list of connections made
            pass

        return 

    def determineFitness(self, inputPins, outputPins, basetable):
        pass

    def mutate(self, mutationRate = .01):
        pass




class Solve:

    def __init__(self, truthtable, allowedGates, solverCount = 100):
        self.truthtable = truthtable
        self.allowedGates = allowedGates

        self.inputCount = len(list(self.truthtable.keys())[0])
        self.outputCount = len(list(self.truthtable.values())[0])

        self.group = [Solvers(i, truthtable, allowedGates, self.inputCount, self.outputCount) for i in range(solverCount)]

    def singlePass(self, inputPins, outputPins, inputConnections, outputConnections, firstPass = False, allowedSolutionsAsPercentage = .1):

        for i in self.group:
            i.arange(inputConnections, outputConnections, firstPass)
            # i.determineFitness()
            execution = execute(inputPins, outputPins)

        self.group.sort(key=lambda x: x.fitness, reverse=True)

        p = int(len(self.group) * allowedSolutionsAsPercentage)
        return self.group[:p]

    def mutate(self, desiredGroupSize):
        
        while len(self.group) < desiredGroupSize:
            pass

    def solve(self, evolv = 100):

        inputPins = [Pin(i, label = "Input Pin " + str(i)) for i in range(self.inputCount)]
        outputPins = [Pin(i, label = "Output Pin " + str(i)) for i in range(self.outputCount)]

        inputs_ = [[p, 0] for p in inputPins]
        outputs_ = [[p, 0] for p in outputPins]

        gateInputs = []
        gateOutputs = []
        for gate in self.allowedGates:
            for i in range(gate.inputCount):
                gateInputs.append([gate, i])

            for i in range(gate.outputCount):
                gateOutputs.append([gate, i])

        inputs_.extend(gateInputs)
        outputs_.extend(gateOutputs)

        for i in range(evolv):
            self.group = self.singlePass(inputPins, outputPins, inputs_, outputs_, firstPass = .5, allowedSolutionsAsPercentage = .5)

        return self.group

        