from Circuit import *
from Resistor import *
from CurrentSource import *
from VoltageSource import *
from Diode import *
from TransistorBJT import *

circ = Circuit()

## Układ z projektu (same rezystory, tranzystor i zasilanie)
E1 = VoltageSource(1, [1, 6], 12.0)
R1 = Resistor(1, [1, 2], 47000.0)
R2 = Resistor(2, [2, 6], 22000.0)
R3 = Resistor(3, [1, 3], 10000.0)
R4 = Resistor(4, [4, 5], 330.0)
R5 = Resistor(5, [5, 6], 4700.0)
Q1 = TransistorBJT(1, [3, 2, 4], 1e-12, 1e-12, 1.0, 1.0, 100.0)

circ.add_element(E1)
circ.add_element(R1)
circ.add_element(R2)
circ.add_element(R3)
circ.add_element(R4)
circ.add_element(R5)
circ.add_element(Q1)

circ.set_gnd_node(6)

circ.op_analisys()
circ.display_OP_analysys_results()
