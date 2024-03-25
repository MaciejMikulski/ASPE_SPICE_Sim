from Component import *


class Diode(Component):

    def __init__(self, id, ports, satCurr, emissionCoeff):
        self._id = id
        self._type: ComponentType = ComponentType.DIO.name
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._Is = satCurr
        self._alpha = 1.0 / (emissionCoeff * 0.025)

    def get_ports(self):
        return super().get_ports()

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Saturation current: " + str(self._Is) + " [A]")
        print("Alpha: " + str(self._alpha) + " [1/V]")
