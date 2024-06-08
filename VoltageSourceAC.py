from Component import *
import math
import numpy as np

class VoltageSourceAC(Component):

    def __init__(self, id, ports, dcOffset, amplitude, freq):
        self._id = id
        self._type = ComponentType.VAC
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._dcOffset = dcOffset
        self._amplitude = amplitude
        self._frequency = freq

    def get_voltage(self):
        return self._dcOffset

    def get_voltage_ac(self, t):
        x = 2.0 * np.pi * self._frequency * t
        return self._dcOffset + self._amplitude * math.sin(x)

    def get_ports(self):
        return super().get_ports()

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("DC offset: " + str(self._dcOffset) + " [V]")
        print("Amplitude: " + str(self._amplitude) + " [V]")
        print("Frequency: " + str(self._frequency) + " [Hz]")
