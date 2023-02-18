import ast
import copy
import ast
from connection import *

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

        self.type_ = "Gate"

        self.inputs = ["-1" for _ in range(inputCount)]
        self.outputs = ["-1" for _ in range(outputCount)]

        

        self.UTD = False

        for i in range(2 ** self.inputCount):
            self.truthTable[str(decToBin(i, self.inputCount))] = "0"

        self.connections = {
            "incomming": [[i, None] for i in range(inputCount)], 
            "outgoing": [[i, None] for i in range(outputCount)]
        }

        self.ancestors = []
        self.descendants = []

    def __str__(self):
        return self.label + "(" + str(self.ID) + ")"

    def __repr__(self):
        return self.label

    def process(self):
        if not self.synced():
            return False

        self.outputs = list(self.truthTable["".join(self.inputs)])
        return True

    def synced(self):
        if any([x == "-1" for x in self.inputs]):
            self.UTD = False
            return False
        
        self.UTD = True
        return True

        
    def getInput(self, indexPin):
        return self.inputs[indexPin]

    def getOutput(self, indexPin):
        return self.outputs[indexPin]

    def setOutput(self, indexPin, value):
        self.outputs[indexPin] = value

    def setInput(self, indexPin, value):
        self.inputs[indexPin] = value

    def reset(self):
        self.inputs = ["-1" for _ in range(self.inputCount)]
        self.outputs = ["-1" for _ in range(self.outputCount)]
        self.UTD = False

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

        self.type_ = "Pin"
        self.UTD = False
    
        self.value = "-1"
        self.label = label

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return str(self.label)

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value     
        
    def process(self):
        if not self.synced():
            return False

        for i in self.outputConnections:
            i.setInput(self.outputConnections[i], self.value)

        return True

    def synced(self):
        if self.value == "-1":
            self.UTD = False
            return False
        
        self.UTD = True
        return True

    def reset(self):
        self.value = "-1"
        self.UTD = False


def execute(gates, inputPins, outputPins, connections): 
    outputTruthTable = {}

    def returnInput(i, l):
        return str(decToBin(i, l))

    

    for i in range(2**len(inputPins)):

        in_ = str(returnInput(i, len(inputPins)))
        outputTruthTable[in_] = "0" * len(outputPins)

        for j in range(len(inputPins)):
            inputPins[j].setValue(in_[j])

        for g in gates:
            g.reset()

        for o in outputPins:
            o.reset()

        connections.reset()

        Q = []
        Q.extend(inputPins)
        Q.extend(gates)
        Q.extend(outputPins)
        Q.append(len(Q))

        while len(Q) > 0:
            
            current = Q.pop(0) 
            if type(current) == int:
                if (len(Q) != current):
                    Q.append(len(Q))
                    continue
                else:
                    break

            SYNC = current.process() 

            if SYNC:
                fill = connections.myConnections(current, False)

                if fill == []:
                    if current in outputPins:
                        index = outputPins.index(current)
                        
                        s_ = ""
                        for i in range(len(outputTruthTable[in_])):
                            if i != int(index):
                                s_ += outputTruthTable[in_][i]
                            else:
                                s_ += str(current.getValue())
                        
                        outputTruthTable[in_] = s_
                    continue
                
                for f in fill:
                    f.pushSignal()   

            else:
                Q.append(current)
                
    return outputTruthTable



def compareTruthTables(tt1, tt2):
    score = 0

    if len(tt1) != len(tt2):
        return -1

    if len(tt1) == 0 or len(tt2) == 0:
        return -1

    for k, v in tt1.items():
        l = len(tt1[k])
        for i in range(l):
            if tt1[k][i] == tt2[k][i]:
                score += 1
        
    return score / (len(tt1) * len(tt1[k]))
         

def compactTruthTable(tt):
    newTable = {}
    for k, v in tt.items():
        key_ = ""
        for i in ast.literal_eval(k):
            for key, value in i.items():
                key_ += value
        
        val_ = ""
        if type(v) is list:
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

            

                    



        

