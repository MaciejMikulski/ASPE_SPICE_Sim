import numpy as np

from Circuit import *
from Resistor import *
from CurrentSource import *
from VoltageSource import *
from Diode import *
from TransistorBJT import *

import matplotlib.pyplot as plt
import math

VDD1 = VoltageSource(1, [1, 3], 9.0)
R1 = Resistor(1, [1, 2], 39000.0)
R2 = Resistor(2, [2, 3], 9100.0)
R3 = Resistor(3, [4, 3], 100.0)
Q1 = TransistorBJT(1, [1, 2, 4], 10**(-12), 10**(-12), 1.0, 1.0, 100)

circ = Circuit()

circ.add_element(R1)
circ.add_element(R2)
circ.add_element(R3)
circ.add_element(VDD1)
circ.add_element(Q1)

circ.set_gnd_node(3)
print(circ.op_analisys())
