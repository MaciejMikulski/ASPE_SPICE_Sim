from Component import *

class Resistor(Component):

    def __init__(self, id, ports, resistance):
        self._id = id
        self._type: ComponentType = ComponentType.R.name
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._resistance = resistance

    def get_resistance(self):
        return self._resistance
    
    def get_ports(self):
        return super().get_ports()

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Resistence: " + str(self._resistance) + " [Ohm]")