from Component import *
import numpy as np

class IntegratingRule(Enum):
    INERP = 1
    TRAPEZ = 2

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

    def get_params(self, ud, id, stepLen, method=IntegratingRule.INERP):
        """
        This method calculates companion model parametes for capacitor using given
        integrating method.

        Parameters
        ----------
        ud : float
            Voltage drop between positive and negative terminal of the capacitor in previous step.
        id : float
            Current flowing through capacitor in previous step.
        stepLen : float
            Length of simulation timestep in seconds.
        method : constant
            Type of integrating method represented by IntegratingRule enum.
        Returns
        Gc - conductance, Ieq - current of model's internal current cource.
        ----------
        """
        Gc = 0.0
        Ieq = 0.0
        if method == IntegratingRule.INERP:
            Gc = self._capacitance / stepLen
            Ieq = -Gc * ud
        elif method == IntegratingRule.TRAPEZ:
            Gc = 2.0 * self._capacitance / stepLen
            Ieq = -(-Gc * ud + id)
        return Gc, Ieq

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Capacitance: " + str(self._capacitance) + " [Ohm]")
