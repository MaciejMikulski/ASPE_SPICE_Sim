from Component import *
import Constants
import math


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

        tmpaLo, tmpbLo, tmpaHi, tmpbHi = self._calculate_linear_coeffs()
        self._aLo = tmpaLo
        self._bLo = tmpbLo
        self._aHi = tmpaHi
        self._bHi = tmpbHi

    def get_ports(self):
        return super().get_ports()

    def get_params(self, Ube, Ubc):

        # Calculate collector diode
        GdC, Idc = self._calc_diode(Ubc, self._Isc, self._alphaC)
        # Calculate emitter diode
        GdE, Ide = self._calc_diode(Ube, self._Ise, self._alphaE)

        Ic = self._alphaF * Ide - Idc
        Ie = self._alphaF * Idc - Ide
        Ib = -Ic - Ie

        return Ic, Ib, Ie

    def _calculate_linear_coeffs(self):
        """Calculate coeffitients of linear functions for approximating Id"""
        GdLo, ILo, IdLo = self.get_params(Constants.DIO_LO_THRES)
        GdHi, IHi, IdHi = self.get_params(Constants.DIO_HI_THRES)

        aLo = GdLo
        aHi = GdHi
        bLo = IdLo - GdLo * Constants.DIO_LO_THRES
        bHi = IdHi - GdHi * Constants.DIO_HI_THRES

        return aLo, bLo, aHi, bHi

    def _calc_diode(self, Uf, Is, alpha):
        if Uf < Constants.DIO_LO_THRES:
            Gd = self._aLo
            Id = self._aLo * Uf + self._bLo
        elif Uf <= Constants.DIO_HI_THRES:
            Gd = alpha * Is * math.exp(alpha * Uf)
            Id = Is * (math.exp(alpha * Uf) - 1.0)
        else:
            Gd = self._aHi
            Id = self._aHi * Uf + self._bHi

        return Gd, Id

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Collector saturation current: " + str(self._Isc) + " [A]")
        print("Emitter saturation current: " + str(self._Ise) + " [A]")
        print("Beta: " + str(self._alphaF / (1 - self._alphaF)))
        print("Alpha collector: " + str(self._alphaC) + " [1/V]")
        print("Alpha emitter: " + str(self._alphaE) + " [1/V]")
