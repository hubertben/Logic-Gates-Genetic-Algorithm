
# from network import *
from gates import *
import random


# class Solvers:

#     def __init__(self, iD, truthtable, allowedGates, inputCount, outputCount):
#         self.truthtable = truthtable
#         self.allowedGates = allowedGates
#         self.inputCount = inputCount
#         self.outputCount = outputCount
#         self.iD = iD

#         self.fitness = 0
#         self.circuit = None

#     def __repr__(self):
#         print("Solver " + str(self.iD) + " Fitness: " + str(self.fitness))
#         return ""
        

#     def arange(self, inputConnections, outputConnections, firstPass = False):

#         if firstPass != False:   

#             totalNumberOfConnections = len(inputConnections) * len(outputConnections)
#             numberOfConnections = random.randint(int(totalNumberOfConnections * .3), int(totalNumberOfConnections * .8))
        
#             connections = []

#             rules = [
#                 # ["Input Pin", "Output Pin"],
#                 ["Input Pin", "Input Pin (Gate)"],
#                 ["Output Pin (Gate)", "Output Pin"],
#                 ["Output Pin (Gate)", "Input Pin (Gate)"]
#             ]

#             def generatePinPair():

#                 input_ = None
#                 output_ = None

#                 rule = random.choice(rules)

#                 if rule[0] == "Input Pin":
#                     breaker = 0
#                     while True:
#                         breaker += 1
#                         if breaker > 100:
#                             print("Failed to generate a valid connection")
#                             return 0, 0
#                         input_ = random.choice(inputConnections)
#                         if type(input_[0]) == Pin:
#                             break

#                 elif rule[0] == "Output Pin (Gate)":
#                     breaker = 0
#                     while True:
#                         breaker += 1
#                         if breaker > 100:
#                             print("Failed to generate a valid connection")
#                             return 0, 0
#                         input_ = random.choice(outputConnections)
#                         if type(input_[0]) != Pin:
#                             break

                

#                 if rule[1] == "Output Pin":
#                     breaker = 0
#                     while True:
#                         breaker += 1
#                         if breaker > 100:
#                             print("Failed to generate a valid connection")
#                             return 0, 0
#                         output_ = random.choice(outputConnections)
#                         if type(output_[0]) == Pin:
#                             break

#                 elif rule[1] == "Input Pin (Gate)":
#                     breaker = 0
#                     while True:
#                         breaker += 1
#                         if breaker > 100:
#                             print("Failed to generate a valid connection")
#                             return 0, 0
#                         output_ = random.choice(inputConnections)
#                         if type(output_[0]) != Pin:
#                             break   

#                 return input_, output_


#             for i in range(numberOfConnections):
                
#                 c = 0
#                 input_ = None
#                 output_ = None

#                 while True:
#                     c += 1
#                     if c > 100:
#                         # print("Failed to generate a valid connection")
#                         break

#                     input_, output_ = generatePinPair()
#                     if input_[0] != output_[0] and [input_, output_] not in connections and [output_, input_] not in connections:
#                         break


#                 input_[0].addConnection(input_[1], output_[0], output_[1])
#                 connections.append([input_, output_])

#             print("Connections:")
#             for i in connections:
#                 print(i[0][0], i[0][1], " -> ", i[1][0], i[1][1])
            
#             return connections

#         else:
#             # Reconnect the list of connections made in the first pass based on the fitness of the circuit
#                 # It should be as the fitness increases, the less reconnections are made

#             # Return the list of connections made
#             pass

#         return 

#     def determineFitness(self, inputPins, outputPins, basetable):
#         pass

#     def mutate(self, mutationRate = .01):
#         pass




# class Solve:

#     def __init__(self, truthtable, allowedGates, solverCount = 100):
#         self.truthtable = truthtable
#         self.allowedGates = allowedGates

#         self.inputCount = len(list(self.truthtable.keys())[0])
#         self.outputCount = len(list(self.truthtable.values())[0])

#         self.group = [Solvers(i, truthtable, allowedGates, self.inputCount, self.outputCount) for i in range(solverCount)]

#     def singlePass(self, firstPass = False, allowedSolutionsAsPercentage = .1):
        
#         inputPins = [Pin(i, label = "Input Pin " + str(i)) for i in range(self.inputCount)]
#         outputPins = [Pin(i, label = "Output Pin " + str(i)) for i in range(self.outputCount)]

#         inputs_ = [[p, 0] for p in inputPins]
#         outputs_ = [[p, 0] for p in outputPins]

#         gateInputs = []
#         gateOutputs = []
#         for gate in self.allowedGates:
#             for i in range(gate.inputCount):
#                 gateInputs.append([gate, i])

#             for i in range(gate.outputCount):
#                 gateOutputs.append([gate, i])

#         inputs_.extend(gateInputs)
#         outputs_.extend(gateOutputs)

#         inputConnections = inputs_
#         outputConnections = outputs_
        
#         for i in self.group:

#             truthTable = {}

#             connections = i.arange(inputConnections, outputConnections, firstPass)
#             execution = execute(inputPins, outputPins)

#             validTable = True
#             for k, v in execution.items():
#                 if(v == [] or v == None):
#                     validTable = False
#                     break

#                 truthTable[str(k)] = v[:len(outputPins)]

#             print("EXECUTION")
#             if validTable:
#                 displayTruthTable(truthTable)
#             else:
#                 print("Invalid Table")


#         if validTable:
#             truthTable = compactTruthTable(truthTable)
#             displayTruthTable(truthTable)
#             print(compareTruthTables(self.truthtable, truthTable))
        

#         self.group.sort(key=lambda x: x.fitness, reverse=True)

#         p = int(len(self.group) * allowedSolutionsAsPercentage)
#         return self.group[:p]

#     def mutate(self, desiredGroupSize):
        
#         while len(self.group) < desiredGroupSize:
#             break

#     def solve(self, evolv = 100):

#         for i in range(evolv):
#             self.group = self.singlePass(firstPass = .5, allowedSolutionsAsPercentage = .5)

#         return self.group

        







rules = [
    ["Input Pin", "Input Pin (Gate)"],
    ["Output Pin (Gate)", "Output Pin"],
    ["Output Pin (Gate)", "Input Pin (Gate)"]
]


def newPinSet(inputPinCount, outputPinCount):
    inputPins = [Pin(i, label = "Input Pin " + str(i)) for i in range(inputPinCount)]
    outputPins = [Pin(i, label = "Output Pin " + str(i)) for i in range(outputPinCount)]
    return inputPins, outputPins


def replicateGates(gates):
    newGates = []
    for gate in gates:
        newGates.append(gate.copyGate())
    return newGates


class Package:

    def __init__(self, iD, truthTable, gates, numInputPins, numOutputPins):

        self.iD = iD
        self.truthTable = truthTable
        self.gates = gates
        self.numInputPins = numInputPins
        self.numOutputPins = numOutputPins

        self.inputPins, self.outputPins = None, None

        self.gateInputs = []
        self.gateOutputs = []
        self.fullConnections = []



        self.firstPass = True
        

    def retrieveGateIO(self, gate):
        gateInputs = []
        gateOutputs = []
        for i in range(gate.inputCount):
            gateInputs.append([gate, i])
        for i in range(gate.outputCount):
            gateOutputs.append([gate, i])
        return gateInputs, gateOutputs

    def printConnections(self):
        print("\nConnections:")
        for c in self.fullConnections:
            print(c)
        print("")

    def initialize(self):
        
        self.inputPins, self.outputPins = newPinSet(self.numInputPins, self.numOutputPins)

        for g in self.gates:
            gateInputs_, gateOutputs_ = self.retrieveGateIO(g)
            self.gateInputs.extend(gateInputs_)
            self.gateOutputs.extend(gateOutputs_)

        # connect all input pins to all gate inputs
        for i in self.inputPins:
            for j in self.gateInputs:
                self.fullConnections.append([0, ([i, 0], j), False])

        # connect all gate outputs to all output pins
        for j in self.outputPins:
            for i in self.gateOutputs:
                self.fullConnections.append([1, (i, [j, 0]), False])

        # connect all gate outputs to all gate inputs
        for i in self.gateOutputs:
            for j in self.gateInputs:

                if(i[0] == j[0]):
                    continue

                self.fullConnections.append([2, (i, j), False])

        


    def makeModify(self):
        
        if self.firstPass:
            
            self.firstPass = False

            for c in self.fullConnections:
                rule = c[0]

                if(rule == 0):
                    if(random.randint(0, 1) == 0):
                        c[2] = True

                if(rule == 2):
                    if(random.randint(0, 1) == 0):
                        c[2] = True

            outputs = {}
            for c in self.fullConnections:
                if(c[0] == 1):
                    if(c[1][1][0] in outputs):
                        outputs[c[1][1][0]].append(c)
                    else:
                        outputs[c[1][1][0]] = [c]

            for o in outputs:
                connections = outputs[o]
                chosenConnection = random.choice(connections)
                for c in connections:
                    if(c == chosenConnection):
                        c[2] = True
                    else:
                        c[2] = False

        else:
            pass



    def connect(self):
        for c in self.fullConnections:
            if(c[2]):
                c[1][0][0].addConnection(c[1][0][1], c[1][1][0], c[1][1][1])

    def execute(self, verbose = False):
        execution = execute(self.inputPins, self.outputPins)
        if(verbose):
            displayTruthTable(execution)
        return execution
        

    def evaluate(self, execution):
        pass

    def reproduce(self):
        pass



    def arange(self):

        

        connections = self.initialize()

        for c in connections:
            print(c)

        connectionCount = random.randint(1, len(connections))
        chosenConnections = random.sample(connections, connectionCount)

        for c in chosenConnections:
            c[0][0].addConnection(c[0][1], c[1][0], c[1][1])

        evaluation = execute(self.inputPins, self.outputPins)
        pruned = self.pruneOutput(evaluation)
        
        if(pruned == "Invalid Table"):
            print("Invalid Table")
            return None
        else:
            displayTruthTable(pruned)
            return pruned
        



def solve(truthTable, gates, numberOfInstances = 1, fitnessTolerance = .9):
    
    numInputPins = len(list(truthTable.keys())[0])
    numOutputPins = len(list(truthTable.values())[0])

    print("Number of Input Pins: " + str(numInputPins), "Number of Output Pins: " + str(numOutputPins))

    group = []
    for i in range(numberOfInstances):
        newGates = replicateGates(gates)
        group.append(Package(i, truthTable, newGates, numInputPins, numOutputPins))

    for i in range(numberOfInstances):
        group[i].initialize()

        group[i].makeModify()

        group[i].printConnections()

        group[i].connect()

        execution = group[i].execute(True)

        group[i].evaluate(execution)

        group[i].reproduce()


    return group