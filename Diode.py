from Component import *
import Constants
import math

class Diode(Component):

    def __init__(self, id, ports, satCurr, emissionCoeff, temp=300.0):
        self._id = id
        self._type: ComponentType = ComponentType.DIO.name
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._Is = satCurr
        fiT = (Constants.k * temp) / Constants.q
        self._alpha = 1.0 / (emissionCoeff * fiT)

    def get_ports(self):
        return super().get_ports()

    def getParams(self, Ud):
        # TODO: add linearisation of the diode characteristics for extreme polarisations
        Gd = self._alpha * self._Is * math.exp(self._alpha * Ud)
        Id = self._Is * (math.exp(self._alpha * Ud) - 1.0)
        Ieq = Id - Gd * Ud
        return Gd, Ieq

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Saturation current: " + str(self._Is) + " [A]")
        print("Alpha: " + str(self._alpha) + " [1/V]")
