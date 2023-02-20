
# from network import *
from gates import *
from connection import *
import random

import time

seed = random.randint(0, 1000000)



setSeed = 0



if setSeed != 0:
    seed = setSeed

random.seed(seed)
print("\nSeed: " + str(seed) + "\n")


def map(x, a, b , c, d):
    return (x-a)/(b-a) * (d-c) + c

def mapFunc(x, func, a, b, c, d):
    return func(map(x, a, b, c, d))

rules = [
    ["Input Pin", "Input Pin (Gate)"],
    ["Output Pin (Gate)", "Output Pin"],
    ["Output Pin (Gate)", "Input Pin (Gate)"]
]


def newPinSet(inputPinCount, outputPinCount):
    inputPins = [Pin(i, label = "In_" + str(i)) for i in range(inputPinCount)]
    outputPins = [Pin(i, label = "Out_" + str(i)) for i in range(outputPinCount)]
    return inputPins, outputPins


def replicateGates(gates):
    newGates = []
    for gate in gates:
        newGates.append(gate.copyGate())
    return newGates


class Package:

    def __init__(self, iD, truthTable, GATES):

        self.iD = iD
        self.truthTable = truthTable
        self.GATES = GATES

        self.CONNECTIONS = Connections()
        self.CONNECTIONS_BITMAP = []

        self.inputPins, self.outputPins = None, None
        self.fitness = 0
        self.groupFitness = 0

       
        
    def gatePinPair(self, gate, pin):
            return "__".join([str(gate), str(pin)])


    def reverseGatePinPair(self, pair):
        gate, pin = pair.split("__")
        for g in self.GATES:
            if(str(g.label) == gate):
                return g, int(pin)
    


    def initialize(self, CONNECTIONS, inputPins, outputPins):

        CONNECTIONS = CONNECTIONS.fullCopy()

        CONNECTIONS.reset()

        self.CONNECTIONS_BITMAP = [0 for _ in range(len(CONNECTIONS))]
        SAMPLE, BITMAP = CONNECTIONS.__sample__(random.random(), returnBitMap = True)

        self.CONNECTIONS = SAMPLE
        self.CONNECTIONS_BITMAP = BITMAP


        self.exc = execute(self.GATES, inputPins, outputPins, self.CONNECTIONS)
        self.fitness = compareTruthTables(self.exc, self.truthTable)
        return self.fitness
        
            
                
        

    def makeModify(self):
        pass
        

    
                

            




    def linker(self):
        pass

    def execute(self, verbose = False):
        pass
        

    def evaluate(self, execution):
        self.fitness = compareTruthTables(compactTruthTable(execution), self.truthTable)
        return self.fitness

    def reproduce(self):
        pass



        
def solve(truthTable, gates, numberOfInstances = 1, displayEveryPercent = 0):

    startTime = time.time()

    numInputPins = len(list(truthTable.keys())[0])
    numOutputPins = len(list(truthTable.values())[0])

    inputPins, outputPins = newPinSet(numInputPins, numOutputPins)
    CONNECTIONS = Connections()

    for gate in gates:

        gateInputCount = gate.inputCount
        gateOutputCount = gate.outputCount

        for i in range(gateInputCount):
            for pin in inputPins:
                CONNECTIONS.addConnection(pin, 0, gate, i)

        for i in range(gateOutputCount):
            for pin in outputPins:
                CONNECTIONS.addConnection(gate, i, pin, 0)

        for g in gates:
            if g != gate:
                for i in range(gateOutputCount):
                    for j in range(g.inputCount):
                        CONNECTIONS.addConnection(gate, i, g, j)

    # print("Number of Input Pins: " + str(numInputPins), "Number of Output Pins: " + str(numOutputPins))

    group = []
    for i in range(numberOfInstances):
        newGates = replicateGates(gates)
        random.shuffle(newGates)
        group.append(Package(i, truthTable, newGates))

    generation = []
    G = []

    displayRate = numberOfInstances * displayEveryPercent

    for i in range(numberOfInstances):

        if displayEveryPercent != 0 and i % displayRate == 0:
            print("Instance:", i, "of", numberOfInstances)

        indv = group[i]
        e = indv.initialize(CONNECTIONS, inputPins, outputPins)
        generation.append(e)
        G.append(indv)

        


        # indv.makeModify()
        # indv.linker()
        # execution = indv.execute(False)
        # fitness = indv.evaluate(execution)
        # generation.append([indv, fitness])


    # generation.sort(key = lambda x: x[1], reverse = True)
    # best = generation[0]

    # print("\n\nBest:", best[0].iD, ":", best[1])

    # displayTruthTable(compactTruthTable(execute(best[0].inputPins, best[0].outputPins)))
    # easyReadConnections(best[0])

    # print()

    # for g in best[0].gates:
    #     print("Gate:", g)
    #     print("Inputs:", g.inputConnections)
    #     print("Outputs:", g.outputConnections)
    #     print()



    T = 0
    
    
    for g in group:
        if len(g.CONNECTIONS) > T:
            T = len(g.CONNECTIONS)
    
    M = T
    for g in group:
        if len(g.CONNECTIONS) < M:
            M = len(g.CONNECTIONS)

    ratio = .75

    for g in group:
        g.groupFitness = (((ratio) * g.fitness) + ((1 - ratio) * (1 - map(len(g.CONNECTIONS), M, T, 0, 1))))
        g.groupFitness = round(g.groupFitness, 3)

    sort_ = []

    for g in group:
        sort_.append([g, g.groupFitness])

    sort_.sort(key = lambda x: x[1], reverse = True)

    best = sort_[0]

    for s in sort_[:10]:
        print(s[0].iD, "\t:\t", s[1], "\t:\t", len(s[0].CONNECTIONS), "\t:\t", s[0].fitness)



    
    endTime = time.time()
    timeSecond = endTime - startTime

    print("\n\nBest:", best[0].iD, ":", best[1])
    

        
    
    return group



def easyReadConnections(package):
    connections = []
    print()
    for c in package.fullConnections:
        if(c[2]):
            print(c[1][0][0], ":", c[1][0][1], "\t->\t", c[1][1][0], ":", c[1][1][1])

    return connections