import numpy as np

from Circuit import *
from Resistor import *
from CurrentSource import *

R1 = Resistor(1, [1,2], 1000.0)
R2 = Resistor(2, [2,3], 2000.0)
R3 = Resistor(3, [2,3], 3000.0)
IDD1 = CurrentSource(1, [1,3], 0.01)

circ = Circuit()
circ.add_element(R1)
circ.add_element(R2)
circ.add_element(R3)
circ.add_element(IDD1)

print(circ._nodes)



