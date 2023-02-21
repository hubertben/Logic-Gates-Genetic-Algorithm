
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


def map(x, a, b , c, d, round_ = None):
    if round != None:
        return round((x-a)/(b-a) * (d-c) + c, round_)
    return (x-a)/(b-a) * (d-c) + c

def mapFunc(x, func, a, b, c, d):
    return func(map(x, a, b, c, d))


def newPinSet(inputPinCount, outputPinCount):
    inputPins = [Pin(i, label = "In_" + str(i)) for i in range(inputPinCount)]
    outputPins = [Pin(i, label = "Out_" + str(i)) for i in range(outputPinCount)]
    return inputPins, outputPins


def replicateGates(gates):
    newGates = []
    for gate in gates:
        newGates.append(gate.copyGate())
    return newGates




def buildConnections(truthTable, GATES):
    CONNECTIONS = Connections()
    INPUT_NUM = len(list(truthTable.keys())[0])
    OUTPUT_NUM = len(list(truthTable.values())[0])

    inputPins, outputPins = newPinSet(INPUT_NUM, OUTPUT_NUM)
    
    for gate in GATES:

        gateInputCount = gate.inputCount
        gateOutputCount = gate.outputCount

        for i in range(gateInputCount):
            for pin in inputPins:
                CONNECTIONS.addConnection(pin, 0, gate, i)

        for i in range(gateOutputCount):
            for pin in outputPins:
                CONNECTIONS.addConnection(gate, i, pin, 0)

        for g in GATES:
            if g != gate:
                for i in range(gateOutputCount):
                    for j in range(g.inputCount):
                        CONNECTIONS.addConnection(gate, i, g, j)

    return CONNECTIONS, inputPins, outputPins


def printTop(group, top = 10):
    print("\n\nTop " + str(top) + ":")

    for i in range(top):

        f = group[i]["fitness"]
        f = str(f)
        while len(f) < 5:
            f = f + " "
        c = group[i]["numberOfConnections"]
        c = str(c)
        while len(c) < 5:
            c = c + " "

        w = group[i]["weightedFitness"]
        w = str(w)
        while len(w) < 5:
            w = w + " "

        print("Fitness:", f, "\tConnections:", c, "\tWeighted Fitness:", w)


def generateGroup(truthTable, GATES, CONNECTIONS, inputPins, outputPins, numberOfInstances = 1, displayEveryPercent = 0):
    group = []
    displayRate = numberOfInstances * displayEveryPercent

    for i in range(1, numberOfInstances + 1):

        if displayEveryPercent != 0 and i % displayRate == 0:
            print("Instance:", i, "of", numberOfInstances)
        
        r = random.random()   
        SAMPLE, BITMAP = CONNECTIONS.__sample__(r, returnBitMap = True)

        exc = execute(GATES, inputPins, outputPins, SAMPLE)
        fitness = compareTruthTables(exc, truthTable)

        group.append({
            "fitness": fitness,
            "connections": SAMPLE,
            "numberOfConnections": len(SAMPLE),
            "bitmap": BITMAP,
            "exc": exc,
        })

        CONNECTIONS.reset()

    return group


def addWeightedFitness(group, weight = .85):
    maxConnectionsLength = max([len(c["connections"]) for c in group])
    minConnectionsLength = min([len(c["connections"]) for c in group])

    for c in group:
        c["fitness"] = round(c["fitness"], 3)
        c["connectionLengthScaling"] = 1 - map(c["numberOfConnections"], minConnectionsLength, maxConnectionsLength, 0, 1, 3)
        c["weightedFitness"] = round((weight * c["fitness"]) + ((1 - weight) * c["connectionLengthScaling"]), 3)
        

    group.sort(key = lambda x: x["weightedFitness"], reverse = True)
    return group


def mutate(group, desiredGroupSize, truthTable, GATES, CONNECTIONS, inputPins, outputPins, mutateRate = .1):
    
    newGroup = []
    tempgroup = []

    instanceCount = int(desiredGroupSize / len(group))
    extra = desiredGroupSize - (instanceCount * len(group))

    for g in group:
        for _ in range(instanceCount):
            tempgroup.append(g)
    
    for g in tempgroup:

        bitmap = g["bitmap"]

        for b in range(len(bitmap)):
            if random.random() < mutateRate:
                bitmap[b] = 1 - bitmap[b]

        g["bitmap"] = bitmap

        CONNECTIONS_ = CONNECTIONS.__BitMap__(bitmap)

        exc = execute(GATES, inputPins, outputPins, CONNECTIONS_)
        fitness = compareTruthTables(exc, truthTable)

        newGroup.append({
            "fitness": fitness,
            "connections": CONNECTIONS_,
            "numberOfConnections": len(CONNECTIONS_),
            "bitmap": bitmap,
            "exc": exc,
        })

        CONNECTIONS.reset()

        

    newGroup = addWeightedFitness(newGroup)
    newGroup.sort(key = lambda x: x["weightedFitness"], reverse = True)
    return newGroup


def avgGroupFitness(group):
    return sum([g["fitness"] for g in group]) / len(group)

        
def solve(truthTable, GATES, numberOfInstances = 1, displayEveryPercent = 0):

    startTime = time.time()

    CONNECTIONS, inputPins, outputPins = buildConnections(truthTable, GATES)
    group = generateGroup(truthTable, GATES, CONNECTIONS, inputPins, outputPins, numberOfInstances = numberOfInstances, displayEveryPercent = displayEveryPercent)
    group = addWeightedFitness(group)

    chooseTop = 5

    printTop(group, min(chooseTop, len(group)))
    top = [g for g in group[:chooseTop]]
    print("Average Fitness:", avgGroupFitness(top))
    
    print(len(top))

    newGroup = top

    for i in range(100):
        CONNECTIONS.reset()
        newGroup = mutate(newGroup, numberOfInstances, truthTable, GATES, CONNECTIONS, inputPins, outputPins, mutateRate = .1)
        newGroup = [g for g in newGroup[:chooseTop]]
        print("Average Fitness (" + str(i) + ") :", round(avgGroupFitness(newGroup), 3), "\t Best:", round(newGroup[0]["weightedFitness"], 3))



    printTop(newGroup, min(10, len(newGroup)))

    print("\n\nExecution time:", time.time() - startTime, "seconds")
    return





def easyReadConnections(package):
    connections = []
    print()
    for c in package.fullConnections:
        if(c[2]):
            print(c[1][0][0], ":", c[1][0][1], "\t->\t", c[1][1][0], ":", c[1][1][1])

    return connections