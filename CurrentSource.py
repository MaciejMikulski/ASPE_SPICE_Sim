from Component import *

class CurrentSource(Component):

    def __init__(self, id, ports, current):
        self._id = id
        self._type = ComponentType.IDD
        self._ports = []
        for x in ports:
            self.add_port(x)
        self._current = current

    def get_current(self):
        return self._current
    
    def get_ports(self):
        return super().get_ports()

    def print(self):
        print("Type: " + str(self._type) + str(self._id))
        print("Ports: " + str(self._ports))
        print("Current: " + str(self._current) + " [A]")