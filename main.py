from Circuit import *
from Resistor import *
from CurrentSource import *
from VoltageSource import *
from Diode import *
from TransistorBJT import *
from Capacitor import *
from VoltageSourceAC import *
import matplotlib.pyplot as plt
import numpy as np

circ = Circuit()

## Układ z projektu (same rezystory, tranzystor i zasilanie)
E1 = VoltageSource(1, [1, 6], 12.0)
E2 = VoltageSourceAC(2, [7, 6], 0.0, 0.5, 5000.0)
R1 = Resistor(1, [1, 2], 47000.0)
R2 = Resistor(2, [2, 6], 22000.0)
R3 = Resistor(3, [1, 3], 10000.0)
R4 = Resistor(4, [4, 5], 330.0)
R5 = Resistor(5, [5, 6], 4700.0)
RL = Resistor(6, [8, 6], 22000.0)
C1 = Capacitor(1, [7, 2], 10e-6)
C2 = Capacitor(2, [3, 8], 10e-6)
C3 = Capacitor(3, [5, 6], 22e-6)
Q1 = TransistorBJT(1, [3, 2, 4], 1e-12, 1e-12, 1.0, 1.0, 100.0)
circ.add_element(E1)
circ.add_element(E2)
circ.add_element(R1)
circ.add_element(R2)
circ.add_element(R3)
circ.add_element(R4)
circ.add_element(R5)
circ.add_element(RL)
circ.add_element(C1)
circ.add_element(C2)
circ.add_element(C3)
circ.add_element(Q1)

circ.set_gnd_node(6)

# Analiza TRAN, 10 okresów sygnału wejściowego
#circ.tran_analysis(0.0, 0.002, 0.00001)
#circ._tranAnalysisStatus.print()

# Analiza OP
circ.op_analysis()
circ.display_op_analysis_results()
print(circ._nodes)

## Wykreślenie wyników analizy TRAN
#data = np.loadtxt("tranWyniki.txt")
#Vout = data[:, 7]
#Vin = data[:, 2]
#xaxis = np.linspace(0.0, 0.002, 200)
#plt.figure()
#plt.plot(xaxis, Vout, "r-")
#plt.title("Napięcie wyjściowe układu")
#plt.xlabel("Czas symulacji [s]")
#plt.ylabel("Napięcie [V]")
#plt.grid(linestyle=':')
#plt.figure()
#plt.plot(xaxis, Vin, "r-")
#plt.title("Napięcie wejściowe układu")
#plt.xlabel("Czas symulacji [s]")
#plt.ylabel("Napięcie [V]")
#plt.grid(linestyle=':')
#plt.show()
