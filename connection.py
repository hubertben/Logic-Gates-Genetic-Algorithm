
from gates import *

class Connections:

    def __init__(self, connections_ = []):
        self.connections = connections_

    def addConnection(self, from_, fPin_, to_, tPin_):
        self.connections.append(Connection(from_, fPin_, to_, tPin_))

    def myConnections(self, object_, all = True):
        if all:
            return [x for x in self.connections if x.from_ == object_ or x.to_ == object_]
        else:
            return [x for x in self.connections if (x.from_ == object_ or x.to_ == object_) and not x.pushed]

    def reset(self):
        for x in self.connections:
            x.reset()

class Connection:

    def __init__(self, from_, fPin_, to_, tPin_):
        self.from_ = from_
        self.fPin_ = fPin_
        self.to_ = to_
        self.tPin_ = tPin_

        self.pushed = False

    def reset(self):
        self.pushed = False

    def pushSignal(self):
        signal = 0
        if self.from_.type_ == "Pin":
            signal = self.from_.getValue()
        else:
            signal = self.from_.getOutput(self.fPin_)

        if self.to_.type_ == "Pin":
            self.to_.setValue(signal)
        else:
            self.to_.setInput(self.tPin_, signal)

        self.pushed = True

    def __str__(self):
        return str(self.from_) + str(" [" + str(self.fPin_) + "]") + " -> " + str(self.to_) + str(" [" + str(self.tPin_) + "]")

    def __repr__(self):
        return str(self.from_) + str(" [" + str(self.fPin_) + "]") + " -> " + str(self.to_) + str(" [" + str(self.tPin_) + "]")

