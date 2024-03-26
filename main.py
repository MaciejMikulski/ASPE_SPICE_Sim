import numpy as np

from Circuit import *
from Resistor import *
from CurrentSource import *
from VoltageSource import *
from Diode import *

import matplotlib.pyplot as plt
import math

R1 = Resistor(1, [1, 4], 100.0)
R2 = Resistor(2, [2, 4], 200.0)
R3 = Resistor(3, [2, 4], 300.0)
R4 = Resistor(4, [3, 4], 50.0)
R5 = Resistor(5, [1, 5], 100.0)
IDD1 = CurrentSource(1, [4, 1], 0.2)
VDD1 = VoltageSource(1, [5, 3], 0.1)
D1 = Diode(1, [1, 2], satCurr=10**(-12), emissionCoeff=1.0)

circ = Circuit()

circ.add_element(R1)
circ.add_element(R2)
circ.add_element(R3)
circ.add_element(R4)
circ.add_element(R5)
circ.add_element(IDD1)
circ.add_element(VDD1)
circ.add_element(D1)

circ.set_gnd_node(4)
print(circ.op_analisys())
