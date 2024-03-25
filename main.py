import numpy as np

from Circuit import *
from Resistor import *
from CurrentSource import *
from VoltageSource import *
from Diode import *

R1 = Resistor(1, [1, 2], 1000.0)
R2 = Resistor(2, [2, 3], 2000.0)
R3 = Resistor(3, [2, 3], 3000.0)
IDD1 = CurrentSource(1, [3, 1], 0.01)
VDD1 = VoltageSource(1, [2, 3], 5)
D1 = Diode(1, [1, 2], satCurr=10**(-12), emissionCoeff=1.0)

circ = Circuit()
circ.add_element(R1)
circ.add_element(R2)
circ.add_element(R3)
circ.add_element(IDD1)
circ.add_element(VDD1)

circ.set_gnd_node(3)
circ.construct_matrix()
print(circ.op_analisys())


