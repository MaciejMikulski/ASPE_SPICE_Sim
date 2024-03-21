import numpy as np
from Component import *

class Circuit:

    def __init__(self):
        self._elements = []
        self._nodes = []
        self._conductance_matrix = np.empty(0)
        print(self._conductance_matrix.size)

    def add_element(self, element: Component):
        self._elements.append(element)
        tmp_ports = element.get_ports()
        for port in tmp_ports:
            if port not in self._nodes:
                self._nodes.append(port)
                #add row and column to conductance matrix
        
        #check for component type and add its stamp to conductance matrix

        

    
