
# from network import *
from gates import *
from connection import *
import random

seed = random.randint(0, 1000000)



setSeed = 0 # 865515



if setSeed != 0:
    seed = setSeed

random.seed(seed)
print("\nSeed: " + str(seed) + "\n")

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
        self.INPUT_NUM = len(list(truthTable.keys())[0])
        self.OUTPUT_NUM = len(list(truthTable.values())[0])

        self.CONNECTIONS = Connections()

        self.inputPins, self.outputPins = None, None



       
        
    def gatePinPair(self, gate, pin):
            return "__".join([str(gate), str(pin)])


    def reverseGatePinPair(self, pair):
        gate, pin = pair.split("__")
        for g in self.GATES:
            if(str(g.label) == gate):
                return g, int(pin)
    


    def initialize(self):

        self.inputPins, self.outputPins = newPinSet(self.INPUT_NUM, self.OUTPUT_NUM)

        for gate in self.GATES:

            gateInputCount = gate.inputCount
            gateOutputCount = gate.outputCount

            for i in range(gateInputCount):
                
                for p in self.inputPins:
                    if p.label == "In_" + str(i):
                        gate.inputs[i] = p.label
                        self.CONNECTIONS.addConnection(p, gate, i)
                        break


            print(gate.label, gateInputCount, gateOutputCount)

            
                
        

    def makeModify(self):
        pass
        

    
                

            




    def linker(self):
        pass

    def execute(self, verbose = False):
        pass
        

    def evaluate(self, execution):
        fitness = compareTruthTables(compactTruthTable(execution), self.truthTable)
        return fitness

    def reproduce(self):
        pass



        
def solve(truthTable, gates, numberOfInstances = 1, displayEveryPercent = 0):
    
    numInputPins = len(list(truthTable.keys())[0])
    numOutputPins = len(list(truthTable.values())[0])

    # print("Number of Input Pins: " + str(numInputPins), "Number of Output Pins: " + str(numOutputPins))

    group = []
    for i in range(numberOfInstances):
        newGates = replicateGates(gates)
        random.shuffle(newGates)
        group.append(Package(i, truthTable, newGates))

    generation = []

    displayRate = numberOfInstances * displayEveryPercent

    for i in range(numberOfInstances):

        if displayEveryPercent != 0 and i % displayRate == 0:
            print("Instance:", i, "of", numberOfInstances)

        indv = group[i]
        indv.initialize()

        


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
    
    return group



def easyReadConnections(package):
    connections = []
    print()
    for c in package.fullConnections:
        if(c[2]):
            print(c[1][0][0], ":", c[1][0][1], "\t->\t", c[1][1][0], ":", c[1][1][1])

    return connections