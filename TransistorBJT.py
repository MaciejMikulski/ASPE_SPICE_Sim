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

        # Calculate linearisation parameters for emitter and collector diodes
        tmpaLo, tmpbLo, tmpaHi, tmpbHi = self._calculate_linear_coeffs(self._alphaC, self._Isc)
        self._aLoC = tmpaLo
        self._bLoC = tmpbLo
        self._aHiC = tmpaHi
        self._bHiC = tmpbHi
        tmpaLo, tmpbLo, tmpaHi, tmpbHi = self._calculate_linear_coeffs(self._alphaE, self._Ise)
        self._aLoE = tmpaLo
        self._bLoE = tmpbLo
        self._aHiE = tmpaHi
        self._bHiE = tmpbHi

    def get_ports(self):
        return super().get_ports()

    def get_params(self, Ube, Ubc):

        # Calculate collector diode
        Idc = self._calc_diode(Ubc, self._Isc, self._alphaC, self._aLoC, self._bLoC, self._aHiC, self._bHiC)
        # Calculate emitter diode
        Ide = self._calc_diode(Ube, self._Ise, self._alphaE, self._aLoE, self._bLoE, self._aHiE, self._bHiE)

        Ic = self._alphaF * Ide - Idc
        Ie = self._alphaF * Idc - Ide
        Ib = -Ic - Ie

        return Ic, Ib, Ie

    def _calculate_linear_coeffs(self, alpha, Is):
        """Calculate coeffitients of linear functions for approximating Id"""
        GdLo = alpha * Is * math.exp(alpha * Constants.DIO_LO_THRES)
        IdLo = Is * (math.exp(alpha * Constants.DIO_LO_THRES) - 1.0)

        GdHi = alpha * Is * math.exp(alpha * Constants.DIO_HI_THRES)
        IdHi = Is * (math.exp(alpha * Constants.DIO_HI_THRES) - 1.0)

        aLo = GdLo
        aHi = GdHi
        bLo = IdLo - GdLo * Constants.DIO_LO_THRES
        bHi = IdHi - GdHi * Constants.DIO_HI_THRES

        return aLo, bLo, aHi, bHi

    def _calc_diode(self, Uf, Is, alpha, aLo, bLo, aHi, bHi):
        if Uf < Constants.DIO_LO_THRES:
            Id = aLo * Uf + bLo
        elif Uf <= Constants.DIO_HI_THRES:
            Id = Is * (math.exp(alpha * Uf) - 1.0)
        else:
            Id = aHi * Uf + bHi

        return Id

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Collector saturation current: " + str(self._Isc) + " [A]")
        print("Emitter saturation current: " + str(self._Ise) + " [A]")
        print("Beta: " + str(self._alphaF / (1 - self._alphaF)))
        print("Alpha collector: " + str(self._alphaC) + " [1/V]")
        print("Alpha emitter: " + str(self._alphaE) + " [1/V]")
