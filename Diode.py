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
        tmpaLo, tmpbLo, tmpaHi, tmpbHi = self._calculate_linear_coeffs()
        self._aLo = tmpaLo
        self._bLo = tmpbLo
        self._aHi = tmpaHi
        self._bHi = tmpbHi

    def get_ports(self):
        return super().get_ports()

    def get_params(self, Ud):
        # TODO: add linearisation of the diode characteristics for extreme polarisations
        if Ud < Constants.DIO_LO_THRES:
            Gd = self._aLo
            Id = self._aLo * Ud + self._bLo
        elif Ud <= Constants.DIO_HI_THRES:
            Gd = self._alpha * self._Is * math.exp(self._alpha * Ud)
            Id = self._Is * (math.exp(self._alpha * Ud) - 1.0)
        else:
            Gd = self._aHi
            Id = self._aHi * Ud + self._bHi

        Ieq = Id - Gd * Ud
        return Gd, Ieq, Id

    def _calculate_linear_coeffs(self):
        """Calculate coeffitients of linear functions for approximating Id"""
        GdLo, ILo, IdLo = self.get_params(Constants.DIO_LO_THRES)
        GdHi, IHi, IdHi = self.get_params(Constants.DIO_HI_THRES)

        aLo = GdLo
        aHi = GdHi
        bLo = IdLo - GdLo * Constants.DIO_LO_THRES
        bHi = IdHi - GdHi * Constants.DIO_HI_THRES

        return aLo, bLo, aHi, bHi

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Saturation current: " + str(self._Is) + " [A]")
        print("Alpha: " + str(self._alpha) + " [1/V]")
