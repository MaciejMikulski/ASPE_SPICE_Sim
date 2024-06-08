from Component import *
import numpy as np

class Capacitor(Component):

    def __init__(self, id, ports, capacitance):
        self._id = id
        self._type = ComponentType.C
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._capacitance = capacitance

    def get_capacitance(self):
        return self._capacitance
    
    def get_impedance(self, freq):
        w = 2.0 * np.pi * freq
        return 1.0 / (1j * w * self._capacitance)
    
    def get_addmitance(self, freq):
        w = 2.0 * np.pi * freq
        return 1j * w * self._capacitance
    
    def get_ports(self):
        return super().get_ports()

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Capacitance: " + str(self._capacitance) + " [Ohm]")
