from enum import Enum


class ComponentType(Enum):
    R = 1
    VDD = 2
    IDD = 3
    DIO = 4
    BJT = 5


class Component:

    def __init__(self, type):
        self._ports = []
        self._type = type

    def get_type(self):
        return self._type

    def add_port(self, nodeNum: int):
        self._ports.append(nodeNum)

    def get_ports(self):
        return self._ports
    