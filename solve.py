
# from network import *
from gates import *
import random

seed = random.randint(0, 1000000)



setSeed = 0



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

            '''
            
            Connections that need to be made:

                1)  All input pins need to be connected to at least one gate input, 
                    but 2 different inputs cannot be connected to the same gate input

                2)  All output pins need to be connected to at least one gate output,
                    but 2 different gate outputs cannot be connected to the same output pin

                3)  No gate can have any input or output not connected to anything 
                    (all inputs and outputs must be connected to something)
            
            '''

            def gatePinPair(gate, pin):
                return "__".join([str(gate), str(pin)])


            def reverseGatePinPair(gatePinPair):
                gate, pin = gatePinPair.split("__")
                for g in self.gates:
                    if(str(g) == gate):
                        return g, int(pin)
                    

            def findConnection(connectionInput, connectionInputPin, connectionOutput, connectionOutputPin):
                for c in self.fullConnections:
                    if connectionInput == c[1][0][0] and connectionInputPin == c[1][0][1] and connectionOutput == c[1][1][0] and connectionOutputPin == c[1][1][1]:
                        return c
                

            sampleAmmount = {}
            inputsNotChosen = [gatePinPair(s[0], s[1]) for s in self.gateInputs]

            for i in self.inputPins:
                r = random.randint(1, len(self.gateInputs) - 1)
                sample = random.sample(self.gateInputs, r)

                for s in sample:
                    s_ = gatePinPair(s[0], s[1])
                    if s_ in sampleAmmount:
                        sampleAmmount[s_].append(i)
                    else:
                        sampleAmmount[s_] = [i]

                
            for k, v in sampleAmmount.items():
                gate, pin = reverseGatePinPair(k)
                
                r = None
                if len(v) == 1:           
                    r = v[0]
                else:
                    r = random.choice(v)
                
                connection = findConnection(r, 0, gate, pin)
                connection[2] = True
                inputsNotChosen.remove(k)

            inputsNotChosen = [reverseGatePinPair(s) for s in inputsNotChosen]
            random.shuffle(inputsNotChosen)

            # print("Inputs Not Chosen:", inputsNotChosen)

            for i in inputsNotChosen:
                # print(i[0], "at pin", i[1])

                input__ = inputsNotChosen.pop(0)

                iAncestors = input__[0].getAncestors()

                # print("Descendants:")
                DNC = []
                for d in input__[0].getDescendants():
                    for c in self.fullConnections:
                        if c[1][1][0] == d and c[1][0][0] == input__[0]:
                            # print("-----------------", c)
                            DNC.append(d)

                # print("DNC:", DNC)
                # for g in self.gates:
                    # print(g in DNC)

                choice__ = [g for g in self.gates if g not in iAncestors and g != input__[0] and g not in DNC]

                # print("Ancestors:", iAncestors)
                # print("Choice:", choice__)

                if len(choice__) == 0:
                    # print("No Choice")
                    continue

                r = random.choice(choice__)
                # print("Random:", r)

                connection = findConnection(r, random.randint(0, r.outputCount - 1), input__[0], input__[1])
                # print("Connection:", connection)
                connection[2] = True

                input__[0].ancestors.append(r)
                r.descendants.append(input__[0])
                iAncestors = input__[0].getAncestors()
                # print("Ancestors:", iAncestors)


            # print("Inputs not chosen:", inputsNotChosen)

            for i in inputsNotChosen:
                r = random.choice(self.inputPins)
                connection = findConnection(r, 0, i[0], i[1])
                connection[2] = True


            for o in self.outputPins:
                r = random.choice(self.gateOutputs)
                connection = findConnection(r[0], r[1], o, 0)
                connection[2] = True
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
            displayTruthTable(compactTruthTable(execution))
        return execution
        

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
        group.append(Package(i, truthTable, newGates, numInputPins, numOutputPins))

    generation = []

    displayRate = numberOfInstances * displayEveryPercent

    for i in range(numberOfInstances):

        if displayEveryPercent != 0 and i % displayRate == 0:
            print("Instance:", i, "of", numberOfInstances)

        indv = group[i]

        indv.initialize()

        indv.makeModify()

        # indv.printConnections()

        indv.connect()

        execution = indv.execute(False)

        fitness = indv.evaluate(execution)
        
        # print("Fitness:", fitness)

        # indv.reproduce()

        generation.append([indv, fitness])


    generation.sort(key = lambda x: x[1], reverse = True)
    best = generation[0]

    print("\n\nBest:", best[0].iD, ":", best[1])

    displayTruthTable(compactTruthTable(execute(best[0].inputPins, best[0].outputPins)))

    easyReadConnections(best[0])
    

    return group



def easyReadConnections(package):

    connections = []

    for c in package.fullConnections:
        if(c[2]):
            print(c[1][0][0], "at pin", c[1][0][1], "to", c[1][1][0], "at pin", c[1][1][1])

    return connections