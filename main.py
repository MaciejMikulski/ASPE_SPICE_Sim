import numpy as np

from Circuit import *
from Resistor import *
from CurrentSource import *
from VoltageSource import *
from Diode import *

import matplotlib.pyplot as plt
import math

R1 = Resistor(1, [1, 2], 100.0)
IDD1 = CurrentSource(1, [7, 1], 20.0)
VDD1 = VoltageSource(1, [8, 7], 0.1)
D1 = Diode(1, [2, 3], satCurr=10**(-12), emissionCoeff=1.0)
D2 = Diode(2, [3, 4], satCurr=10**(-12), emissionCoeff=1.0)
D3 = Diode(3, [4, 5], satCurr=10**(-12), emissionCoeff=1.0)
D4 = Diode(4, [5, 6], satCurr=10**(-12), emissionCoeff=1.0)
D5 = Diode(5, [6, 7], satCurr=10**(-12), emissionCoeff=1.0)

circ = Circuit()

circ.add_element(R1)
circ.add_element(D1)
circ.add_element(D2)
circ.add_element(D3)
circ.add_element(D4)
circ.add_element(D5)
circ.add_element(IDD1)
# circ.add_element(VDD1)

circ.set_gnd_node(7)
print(circ.op_analisys())
