
from network import *
from gates import *
from solve import *

'''

Below are a sample of test cases
in which the software that manges the
logic gates and the network is tested.

'''


# XOR Gate from AND and NOT gates

'''
P1 = Pin(1, label = "Input Pin 1")
P2 = Pin(2, label = "Input Pin 2")
P3 = Pin(3, label = "Output Pin 1")

A1 = AND(1)
N1 = NOT(1)

P1.addConnection(0, A1, 0)
P2.addConnection(0, A1, 1)

A1.addConnection(0, N1, 0)

N1.addConnection(0, P3, 0)

INPUTS = [P1, P2]
OUTPUTS = [P3]

execution = execute(INPUTS, OUTPUTS, False)

displayTruthTable(execution)
'''


# Half Adder from XOR and AND gates

'''
P1 = Pin(1, label = "A")
P2 = Pin(2, label = "B")
P3 = Pin(3, label = "S")
P4 = Pin(4, label = "C")

A1 = AND(1)
X1 = XOR(1)

P1.addConnection(0, A1, 0)
P2.addConnection(0, A1, 1)

P1.addConnection(0, X1, 0)
P2.addConnection(0, X1, 1)

X1.addConnection(0, P3, 0)
A1.addConnection(0, P4, 0)

INPUTS = [P1, P2]
OUTPUTS = [P3, P4]

output = execute(INPUTS, OUTPUTS, False)
displayTruthTable(output, group=[["A"], ["B"], ["C", "S"]])
'''

'''

# Full Adder from AND, XOR, and OR gates


P1 = Pin(1, label = "A")
P2 = Pin(2, label = "B")
P3 = Pin(3, label = "C(in)")

P4 = Pin(4, label = "S")
P5 = Pin(5, label = "C(out)")

A1 = AND(1)
A2 = AND(2)

X1 = XOR(1)
X2 = XOR(2)

O1 = OR(1)

P1.addConnection(0, X1, 0)
P2.addConnection(0, X1, 1)

P1.addConnection(0, A2, 0)
P2.addConnection(0, A2, 1)

X1.addConnection(0, X2, 0)
P3.addConnection(0, X2, 1)

X1.addConnection(0, A1, 0)
P3.addConnection(0, A1, 1)

A1.addConnection(0, O1, 0)
A2.addConnection(0, O1, 1)

X2.addConnection(0, P4, 0)

O1.addConnection(0, P5, 0)

INPUTS = [P1, P2, P3]
OUTPUTS = [P4, P5]

outputs = execute(INPUTS, OUTPUTS, False)
displayTruthTable(outputs, group=[["A"], ["B"], ["C(in)"], ["C(out)", "S"]])
'''


'''

# 4-bit Adder from Full Adder


P1 = Pin(1, label = "A8")
P2 = Pin(2, label = "A4")
P3 = Pin(3, label = "A2")
P4 = Pin(4, label = "A1")

P5 = Pin(5, label = "B8")
P6 = Pin(6, label = "B4")
P7 = Pin(7, label = "B2")
P8 = Pin(8, label = "B1")

P9 = Pin(9, label = "C1")

P10 = Pin(10, label = "S8")
P11 = Pin(11, label = "S4")
P12 = Pin(12, label = "S2")
P13 = Pin(13, label = "S1")

P14 = Pin(14, label = "C2")


FA1 = FULLADDER(1)
FA2 = FULLADDER(2)
FA3 = FULLADDER(3)
FA4 = FULLADDER(4)


P1.addConnection(0, FA4, 0)
P2.addConnection(0, FA3, 0)
P3.addConnection(0, FA2, 0)
P4.addConnection(0, FA1, 0)

P5.addConnection(0, FA4, 1)
P6.addConnection(0, FA3, 1)
P7.addConnection(0, FA2, 1)
P8.addConnection(0, FA1, 1)

P9.addConnection(0, FA1, 2)


FA1.addConnection(0, P13, 0)
FA1.addConnection(1, FA2, 2)

FA2.addConnection(0, P12, 1)
FA2.addConnection(1, FA3, 2)

FA3.addConnection(0, P11, 1)
FA3.addConnection(1, FA4, 2)

FA4.addConnection(0, P10, 1)
FA4.addConnection(1, P14, 0)


INPUTS = [P1, P2, P3, P4, P5, P6, P7, P8, P9]
OUTPUTS = [P10, P11, P12, P13, P14]

outputs = execute(INPUTS, OUTPUTS, False)
displayTruthTable(outputs, group = [["A8", "A4", "A2", "A1"], ["B8", "B4", "B2", "B1"], ["C1"], ["C2", "S8", "S4", "S2", "S1"]])

'''