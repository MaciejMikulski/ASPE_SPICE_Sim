import numpy as np
from Component import *

class Circuit:

    def __init__(self):
        self._elements = []
        self._nodes = []
        self._right_side_vect = np.empty(0)
        self._conductance_matrix = np.empty(0)
        self._gnd_node = 0
        print(self._conductance_matrix.size)

    def add_element(self, element: Component):
        self._elements.append(element)
        tmp_ports = element.get_ports()
        for port in tmp_ports:
            if port not in self._nodes:
                self._nodes.append(port)
        
    def construct_matrix(self):
        node_num = len(self._nodes)
        self._conductance_matrix = np.zeros((node_num, node_num))
        self._right_side_vect = np.zeros((node_num, 1))

        for component in self._elements_arr:
            comp_type = component.get_type()
            if comp_type == ComponentType.R.name:
                r_ports = component.get_ports()
                conductance = 1.0 / component.get_resistance()
                p_node_id = self._nodes.index(r_ports[0])
                n_node_id = self._nodes.index(r_ports[1])
                self._conductance_matrix[p_node_id, p_node_id] += conductance
                self._conductance_matrix[p_node_id, n_node_id] -= conductance
                self._conductance_matrix[n_node_id, p_node_id] -= conductance
                self._conductance_matrix[n_node_id, n_node_id] += conductance
                
            elif comp_type == ComponentType.IDD.name:
                idd_ports = component.get_ports()
                current = component.get_current()
                p_node_id = self._nodes.index(idd_ports[0])
                n_node_id = self._nodes.index(idd_ports[1])
                self._right_side_vect[p_node_id, 0] -= current
                self._right_side_vect[n_node_id, 0] += current

            elif comp_type == ComponentType.VDD.name:
                #add voltage source stamp to matrix
                pass
            else:
                pass
        print(self._conductance_matrix)
        print(self._right_side_vect)
        #delete ground node from conductance matrix
        gnd_node_index = self._nodes.index(self._gnd_node)
        self._conductance_matrix = np.delete(self._conductance_matrix, gnd_node_index, 0)
        self._conductance_matrix = np.delete(self._conductance_matrix, gnd_node_index, 1)
        #delete ground node from right side vector
        self._right_side_vect = np.delete(self._right_side_vect, gnd_node_index, 0)
        print(self._conductance_matrix)
        print(self._right_side_vect)


    def set_gnd_node(self, id):
        if id in self._nodes:
            self._gnd_node = id
        else:
            raise Exception("Specified nonexistent node as GND.")


    def op_analisys(self):
        return np.linalg.solve(self._conductance_matrix, self._right_side_vect)

    def tran_analisys(self):
        pass

    
