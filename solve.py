
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

    def __init__(self, iD, truthTable, gates, inputPins, outputPins):
        self.iD = iD
        self.truthTable = truthTable
        self.gates = gates
        self.inputPins = inputPins
        self.outputPins = outputPins

        self.gateInputs = []
        self.gateOutputs = []

    def retrieveGateIO(self, gate):
        gateInputs = []
        gateOutputs = []
        for i in range(gate.inputCount):
            gateInputs.append([gate, i])
        for i in range(gate.outputCount):
            gateOutputs.append([gate, i])
        return gateInputs, gateOutputs



    def formAllConnections(self):
        connections = []

        # connect all input pins to all gate inputs
        for i in self.inputPins:
            for j in self.gateInputs:
                connections.append([[i, 0], j])

        # connect all gate outputs to all output pins
        for j in self.outputPins:
            i = random.choice(self.gateOutputs)
            connections.append([i, [j, 0]])

        # connect all gate outputs to all gate inputs
        for i in self.gateOutputs:
            for j in self.gateInputs:

                if(i[0] == j[0]):
                    continue

                connections.append([i, j])

        return connections


    def pruneOutput(self, truthTable):

        for k, v in truthTable.items():
            if(v == [] or v == None):
                return "Invalid Table"

            print(k, v)

            truthTable[k] = v[:len(self.outputPins)]

        return truthTable


    def arange(self):

        for g in self.gates:
            gateInputs_, gateOutputs_ = self.retrieveGateIO(g)
            self.gateInputs.extend(gateInputs_)
            self.gateOutputs.extend(gateOutputs_)

        connections = self.formAllConnections()

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
        



def solve(truthTable, gates, numberOfInstances, fitnessTolerance = .9):
    
    numInputPins = len(list(truthTable.keys())[0])
    numOutputPins = len(list(truthTable.values())[0])

    print("Number of Input Pins: " + str(numInputPins), "Number of Output Pins: " + str(numOutputPins))


    group = []
    for i in range(numberOfInstances):
        inputPins, outputPins = newPinSet(numInputPins, numOutputPins)
        newGates = replicateGates(gates)
        group.append(Package(i, truthTable, newGates, inputPins, outputPins))

    for i in group:
        i.arange()
        print()




    return group