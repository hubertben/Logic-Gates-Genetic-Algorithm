import ast
import copy
import ast

def require(exp, label = ""):
    if not exp:
        print("[Error]: " + label)
        exit()

def decToBin(n, inputCount):
    return bin(n).replace("0b", "").zfill(inputCount)


class LogicGate:

    def __init__(self, ID, n, inputCount, outputCount):
        self.ID = ID
        self.label = n
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.truthTable = {}

        self.inputs = ["-1" for _ in range(inputCount)]
        self.outputs = ["-1" for _ in range(outputCount)]

        for i in range(2 ** self.inputCount):
            self.truthTable[str(decToBin(i, self.inputCount))] = "0"

        self.inputConnections = {}
        self.outputConnections = {}

        for i in range(inputCount):
            self.inputConnections[str(i)] = []

        for i in range(outputCount):
            self.outputConnections[str(i)] = []


    def addConnection(self, myOutIndex, connectee, connecteeInIndex):

        myOutIndex = str(myOutIndex)
        connecteeInIndex = str(connecteeInIndex)
        
        if myOutIndex not in self.outputConnections:
            self.outputConnections[myOutIndex] = []

        if connecteeInIndex not in connectee.inputConnections:
            connectee.inputConnections[connecteeInIndex] = []

        self.outputConnections[myOutIndex].append(connectee)
        connectee.inputConnections[connecteeInIndex].append(self)

    def setInput(self, from_, value):
        for i in range(self.inputCount):
            if from_ in self.inputConnections[str(i)] and self.inputs[i] == "-1":
                self.inputs[i] = str(value)

    def __str__(self):
        s = "Gate: " + self.label + " ID: " + str(self.ID)
        return s

    def __repr__(self):
        return self.__str__()

    def displayGate(self):
        s = "~~~~~~~~~~~~~~~~~~\n"
        s += "Gate: " + self.label + " ID: " + str(self.ID) + "\n"
        s += "Inputs: " + str(self.inputs) + "\n"
        s += "Outputs: " + str(self.outputs) + "\n"
        s += "~~~~~~~~~~~~~~~~~~\n"
        return s

    def evaluate(self, inputs):
        s = ""
        if(type(inputs) == list):
            for i in inputs:
                s += str(i)
        else:
            s = str(inputs)
        return self.truthTable[s]

    def evaluateInputs(self):
        s = ""
        for i in self.inputs:
            s += str(i)

        out = self.truthTable[s]
        
        for i in range(self.outputCount):
            self.outputs[i] = out[i]
    
    def process(self):
        self.evaluateInputs()
        outputs = {}
        for i in range(self.outputCount):
            for j in self.outputConnections[str(i)]:
                
                if type(j) == Pin:
                    j.value = self.outputs[i]
                    outputs[str(j.label)] = self.outputs[i]

                else:
                    j.setInput(self, self.outputs[i])

        return outputs

    def copyGate(self):
        return copy.deepcopy(self)


class AND(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "AND", 2, 1)

        self.truthTable = {
            "00": "0",
            "01": "0",
            "10": "0",
            "11": "1"
        }
        

class OR(LogicGate):
    
    def __init__(self, ID):
        super().__init__(ID, "OR", 2, 1)

        self.truthTable = {
            "00": "0",
            "01": "1",
            "10": "1",
            "11": "1"
        }

class NOT(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "NOT", 1, 1)

        self.truthTable = {
            "0": "1",
            "1": "0"
        }

class XOR(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "XOR", 2, 1)

        self.truthTable = {
            "00": "0",
            "01": "1",
            "10": "1",
            "11": "0"
        }

class NAND(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "NAND", 2, 1)

        self.truthTable = {
            "00": "1",
            "01": "1",
            "10": "1",
            "11": "0"
        }

class NOR(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "NOR", 2, 1)

        self.truthTable = {
            "00": "1",
            "01": "0",
            "10": "0",
            "11": "0"
        }

class HALFADDER(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "HALFADDER", 2, 2)

        self.truthTable = {
            "00": "00",
            "01": "10",
            "10": "10",
            "11": "01"
        }


class FULLADDER(LogicGate):

    def __init__(self, ID):
        super().__init__(ID, "FULLADDER", 3, 2)

        self.truthTable = {
            "000": "00",
            "001": "10",
            "010": "10",
            "011": "01",
            "100": "10",
            "101": "01",
            "110": "01",
            "111": "11"
        }


class Pin:

    def __init__(self, ID, label = ""):
        self.ID = ID

        self.inputConnections = {}
        self.outputConnections = {}
    
        self.value = 0
        self.label = label

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return str(self.label)

    def addConnection(self, myOutIndex, connectee, connecteeInIndex):

        myOutIndex = str(myOutIndex)
        connecteeInIndex = str(connecteeInIndex)

        if myOutIndex not in self.outputConnections:
            self.outputConnections[myOutIndex] = []

        if connecteeInIndex not in connectee.inputConnections:
            connectee.inputConnections[connecteeInIndex] = []

        self.outputConnections[myOutIndex].append(connectee)
        connectee.inputConnections[connecteeInIndex].append(self)


def execute(inputPins, outputPins, verbose=False, maxItterations = 100): 

    gates = []

    if(verbose): 
        print("-------------------------------------------")
        print("INPUTS:")
        for i in inputPins:
            if(verbose): print(" * " + str(i))
        print("OUTPUTS:")
        for o in outputPins:
            print(" * " + str(o))
        print("-------------------------------------------")

    def findGates(passed):
        for gate in passed:
            if gate not in gates and type(gate) is not Pin:
                gates.append(gate)
                if(verbose): print("GATE:", gate.label + " " + str(gate.ID))
                if(verbose): print(gate.outputConnections)
                for i in range(len(gate.outputConnections)):
                    outs = gate.outputConnections[str(i)]
                    if(verbose):  
                        for o in outs:
                            if o is not None and type(gate) is not Pin:
                                print("   - OUT:", o.label + " " + str(o.ID))
                            else:
                                print("   - OUT:", o)
    
                findGates([o for o in outs if o is not None])

    passed = []

    for i in inputPins:
        for k, v in i.outputConnections.items():
            for o in v:
                if o not in passed:
                    passed.append(o)


    findGates(passed)
    if(verbose): print("GATES:", str(gates))

    def passThroughGates(maxIterations = 1000):
    
        queue = []
        i = 0

        if(verbose):print("GATES:")
        for g in gates:
            if(verbose):print(g.displayGate())
            queue.append(g)

        outputs = []

        iter_ = 0
        while len(queue) > 0:

            if iter_ >= maxIterations:
                if(verbose):print("MAX ITERATIONS REACHED")
                return None

            iter_ += 1

            item = queue[0]

            if "-1" not in item.inputs:
                if(verbose):print("[EXECUTING] QUEUE:", item.label + " " + str(item.ID))
                out = item.process()
                if(verbose): print("OUTPUT:", out)
                
                if out != {}:
                    outputs.append(out)

                queue.pop(i)

            else:

                if(verbose):print("[SKIPPING] QUEUE:", item.label + " " + str(item.ID))
                # move to end of queue
                queue.append(queue.pop(i))
        
        return outputs


    def returnInput(i, l):
        return str(decToBin(i, l))

    outputs = {}

    for i in range(2**len(inputPins)):

        if(verbose): print("I:", str(i) + " ------------------------------------------------------------")

        for j in range(len(inputPins)):
            inputPins[j].value = returnInput(i, len(inputPins))[j]
            if(verbose): print("INPUT:", str(inputPins[j]) + ":\t" + inputPins[j].value)

        for g in gates:
            g.inputs = ["-1" for _ in range(g.inputCount)]
            g.outputs = ["-1" for _ in range(g.outputCount)]

        for j in inputPins:
            for k, v in j.outputConnections.items():
                for o in v:
                    o.setInput(j, j.value)
       
        p = passThroughGates(maxItterations)
        inputs = []

        for j in inputPins:
            inputs.append({j.label : j.value})

        outputs[str(inputs)] = p

    return outputs
                        


def compareTruthTables(tt1, tt2):
    score = 0

    for k, v in tt1.items():
        if k in tt2:
            if v == tt2[k]:
                score += 1

    return score / len(tt1)
         

def compactTruthTable(tt):
    newTable = {}
    for k, v in tt.items():
        key_ = ""
        for i in ast.literal_eval(k):
            for key, value in i.items():
                key_ += value
        
        val_ = ""
        for i in v:
            for key, value in i.items():
                val_ += value

        newTable[key_] = val_
        
    return newTable

def displayTruthTable(outputs, group = []):



    print("Truth Table:")

    def binStringToDec(string):

        # check if string contains only 0s and 1s
        if not all(c in "01" for c in string):
            return string
        return int(string, 2)

    if len(group) == 0:
        for i in outputs:
            print(i, ":", outputs[i])

    else:
        
        for k, v in outputs.items():

            groupCopy = copy.deepcopy(group)

            k = ast.literal_eval(str(k))
            v = ast.literal_eval(str(v))

            masterDict = {}

            for i in k:
                for key, value in i.items():
                    masterDict[key] = value

            for i in v:
                for key, value in i.items():
                    masterDict[key] = value

            for i in range(len(groupCopy)):
                for j in range(len(groupCopy[i])):
                    groupCopy[i][j] = masterDict[groupCopy[i][j]]

            for i in range(len(groupCopy)):
                groupCopy[i] = str(binStringToDec("".join(groupCopy[i])))

            print(groupCopy)

            

                    



        

