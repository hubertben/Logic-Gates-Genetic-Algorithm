
from network import *
from gates import *
from solve import *

'''

Below are a sample of test cases
in which the software that manges the
logic gates and the network is tested.

'''


# P_in_1 = Pin(1, label = "PIN I1")
# P_in_2 = Pin(2, label = "PIN I2")
# P_Out = Pin(3, label = "PIN O1")

# A = AND(1)
# N = NOT(1)

# C = Connections([
#     Connection(P_in_1, 0, A, 0),
#     Connection(P_in_2, 0, A, 1),
#     Connection(A, 0, N, 0),
#     Connection(N, 0, P_Out, 0)
# ])

# GATES = [A, N]
# INPUTS = [P_in_1, P_in_2]
# OUTPUTS = [P_Out]
# CONNECTIONS = C

# exc = execute(GATES, INPUTS, OUTPUTS, CONNECTIONS)



# Build XOR from AND, OR, and NOT gates

# P1 = Pin(1, label = "Input Pin 1")
# P2 = Pin(2, label = "Input Pin 2")
# P3 = Pin(3, label = "Output Pin 1")

# NAND = NAND(1)
# AND = AND(1)
# OR = OR(1)

# connections = [
#     Connection(P1, 0, NAND, 0),
#     Connection(P2, 0, NAND, 1),
#     Connection(P1, 0, OR, 1),
#     Connection(P2, 0, OR, 0),
#     Connection(NAND, 0, AND, 0),
#     Connection(OR, 0, AND, 1),
#     Connection(AND, 0, P3, 0)
# ]

# GATES = [NAND, AND, OR]
# INPUTS = [P1, P2]
# OUTPUTS = [P3]
# CONNECTIONS = Connections(connections)

# exc = execute(GATES, INPUTS, OUTPUTS, CONNECTIONS)
# print(exc)







# Half Adder from XOR and AND gates


# P1 = Pin(1, label = "A")
# P2 = Pin(2, label = "B")
# P3 = Pin(3, label = "S")
# P4 = Pin(4, label = "C")

# A1 = AND(1)
# X1 = XOR(1)

# C = Connections([
#     Connection(P1, 0, A1, 0),
#     Connection(P2, 0, A1, 1),
#     Connection(P1, 0, X1, 0),
#     Connection(P2, 0, X1, 1),
#     Connection(X1, 0, P3, 0),
#     Connection(A1, 0, P4, 0)
# ])

# GATES = [A1, X1]
# INPUTS = [P1, P2]
# OUTPUTS = [P4, P3]
# CONNECTIONS = C

# output = execute(GATES, INPUTS, OUTPUTS, CONNECTIONS)
# displayTruthTable(output)






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


C = Connections([
    Connection(P1, 0, X1, 0),
    Connection(P2, 0, X1, 1),
    Connection(P1, 0, A2, 0),
    Connection(P2, 0, A2, 1),
    Connection(X1, 0, X2, 0),
    Connection(P3, 0, X2, 1),
    Connection(X1, 0, A1, 0),
    Connection(P3, 0, A1, 1),
    Connection(A1, 0, O1, 0),
    Connection(A2, 0, O1, 1),
    Connection(X2, 0, P4, 0),
    Connection(O1, 0, P5, 0)
])

GATES = [A1, A2, X1, X2, O1]
INPUTS = [P1, P2, P3]
OUTPUTS = [P5, P4]
CONNECTIONS = C

outputs = execute(GATES, INPUTS, OUTPUTS, CONNECTIONS)
displayTruthTable(outputs)



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










'''

Solver Examples

'''


# Nand

'''
truthTable = {
                "00": "1",
                "01": "1",
                "10": "1",
                "11": "0"
            }


AND_ = AND(1)
NOT_ = NOT(1)


gates = [AND_, NOT_]

solve(truthTable, gates, 100)
'''


# XOR

'''
truthTable = {
                "00": "0",
                "01": "1",
                "10": "1",
                "11": "0"
            }


AND_1 = AND(1)
AND_2 = AND(2)
NOT_1 = NOT(1)
OR_ = OR(1)



gates = [AND_1, AND_2, OR_, NOT_1]

solve(truthTable, gates, 10000, .05)
'''


# Half Adder


# truthTable = {
#                 "00": "0",
#                 "01": "0",
#                 "10": "0",
#                 "11": "1",
#             }


# AND_1 = AND(1)
# AND_2 = AND(2)

# XOR_1 = XOR(1)
# XOR_2 = XOR(2)

# OR_1 = OR(1)


# gates = [AND_1, AND_2, XOR_1, XOR_2, OR_1]

# solve(truthTable, gates, 5000, .1)









