from Component import *

class VoltageSource(Component):

    def __init__(self, id, ports, voltage):
        self._id = id
        self._type = ComponentType.VDD.name
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._voltage = voltage

    def get_voltage(self):
        return self._voltage
    
    def get_ports(self):
        return super().get_ports()

    def get_id(self):
        return self._id

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Voltage: " + str(self._voltage) + " [V]")