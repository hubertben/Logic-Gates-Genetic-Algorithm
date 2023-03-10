
from gates import *
import copy
import random

class Connections:

    def __init__(self, connections_ = []):
        self.connections = connections_

    def addConnection(self, from_, fPin_, to_, tPin_):
        self.connections.append(Connection(from_, fPin_, to_, tPin_))

    def myConnections(self, object_, all = True):
        if all:
            return [x for x in self.connections if x.from_ == object_ or x.to_ == object_]
        else:
            return [x for x in self.connections if (x.from_ == object_ or x.to_ == object_) and not x.active]

    def reset(self):
        for x in self.connections:
            x.reset()

    def __len__(self):
        return len(self.connections)

    def __str__(self):
        print("\nConnections: ")
        for x in self.connections:
            print(x)
        return ""
    
    def __repr__(self):
        print("\nConnections: ")
        for x in self.connections:
            print(x)
        return ""
    
    def swapItem(self, index):
        i = self.connections[index]
        i.active = not i.active

    
    def _deepcopy_(self):
        L = []
        for x in self.connections:
            L.append(x._deepcopy_())
        return Connections(L)
    
    def __sample__(self, percent = 0.1, returnBitMap = False):

        if percent > 1:
            S = random.sample(self.connections, int(percent))
        else:
            S = random.sample(self.connections, int(len(self.connections) * percent))

        if returnBitMap:
            self.BITMAP = [0] * len(self.connections)
            
            for i in range(len(self.connections)):
                if self.connections[i] in S:
                    self.BITMAP[i] = 1
            
            return Connections(S), self.BITMAP

        return Connections(S)

    def __iter__(self):
        return iter(self.connections)
    
    def __clear__(self):
        self.connections = []

    def __BitMap__(self, bitmap):
        L = []
        for i in range(len(bitmap)):
            if bitmap[i] == 1:
                L.append(self.connections[i])
        return Connections(L)

class Connection:

    def __init__(self, from_, fPin_, to_, tPin_):
        self.from_ = from_
        self.fPin_ = fPin_
        self.to_ = to_
        self.tPin_ = tPin_

        self.signal = 0
        self.active = False

    def reset(self):
        self.active = False
        self.signal = 0

    def pushSignal(self):
        self.signal = 0
        if self.from_.type_ == "Pin":
            self.signal = self.from_.getValue()
        else:
            self.signal = self.from_.getOutput(self.fPin_)

        if self.to_.type_ == "Pin":
            self.to_.setValue(self.signal)
        else:
            self.to_.setInput(self.tPin_, self.signal)

        self.active = True

    def __str__(self):
        return str(self.from_) + str(" [" + str(self.fPin_) + "]") + "\t->\t" + str(self.to_) + str(" [" + str(self.tPin_) + "]" + "\t> " + str(self.signal))

    def __repr__(self):
        return str(self.from_) + str(" [" + str(self.fPin_) + "]") + " -> " + str(self.to_) + str(" [" + str(self.tPin_) + "]" + "\t> " + str(self.signal))
