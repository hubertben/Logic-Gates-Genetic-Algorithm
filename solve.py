
# from network import *
from gates import *
import random



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
            print(inputsNotChosen)

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