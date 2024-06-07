from Component import *
import Constants
import math
from Diode import *

class TransistorBJT(Component):

    def __init__(self, id, ports, satCurrC, satCurrE, emissionCoeffC, emissionCoeffE, beta, temp=300.0):
        self._id = id
        self._type = ComponentType.BJT.name
        self._ports = []
        for x in ports:
            self.add_port(x)

        self._Isc = satCurrC
        self._Ise = satCurrE

        fiT = (Constants.k * temp) / Constants.q

        # These alpha parameters are not present in BJT equations in the lectures, but were kept to make the code
        # similar to the Diode class
        self._alphaC = 1.0 / (emissionCoeffC * fiT)
        self._alphaE = 1.0 / (emissionCoeffE * fiT)

        self._alphaF = beta / (1 + beta)

    def get_ports(self):
        return super().get_ports()

    def get_params(self, Ube, Ubc):
        # Calculate collector diode
        Ieqc, Gbc = self._calc_diode(Ubc, self._Isc, self._alphaC)
        # Calculate emitter diode
        Ieqe, Gbe = self._calc_diode(Ube, self._Ise, self._alphaE)

        return Ieqc, Ieqe, Gbc, Gbe, self._alphaF

    def _calc_diode(self, Uf, Is, alpha):
        if Uf < Constants.DIO_LO_THRES:
            Udeff = Constants.DIO_LO_THRES
        elif Uf <= Constants.DIO_HI_THRES:
            Udeff = Uf
        else:
            Udeff = Constants.DIO_HI_THRES

        Gd = alpha * Is * math.exp(alpha * Udeff)
        Id = Is * (math.exp(alpha * Udeff) - 1.0)
        Ieq = Id - Gd * Udeff

        return Ieq, Gd

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Collector saturation current: " + str(self._Isc) + " [A]")
        print("Emitter saturation current: " + str(self._Ise) + " [A]")
        print("Beta: " + str(self._alphaF / (1 - self._alphaF)))
        print("Alpha collector: " + str(self._alphaC) + " [1/V]")
        print("Alpha emitter: " + str(self._alphaE) + " [1/V]")
