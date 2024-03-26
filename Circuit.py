import numpy as np
from Component import *

class Circuit:

    def __init__(self):
        self._elements = []
        self._nodes = []
        self._rightSideVect = np.empty(0)
        self._conductanceMatrix = np.empty(0)
        self._gndNode = 0
        print(self._conductanceMatrix.size)

    def add_element(self, element: Component):
        self._elements.append(element)
        tmpPorts = element.get_ports()
        for port in tmpPorts:
            if port not in self._nodes:
                self._nodes.append(port)
        
    def construct_matrix(self, prevVoltVect):
        node_num = len(self._nodes)
        self._conductanceMatrix = np.zeros((node_num, node_num))
        self._rightSideVect = np.zeros((node_num, 1))

        for component in self._elements:
            comp_type = component.get_type()
            if comp_type == ComponentType.R.name:
                rPorts = component.get_ports()
                conductance = 1.0 / component.get_resistance()
                pNodeId = self._nodes.index(rPorts[0])
                nNodeId = self._nodes.index(rPorts[1])
                self._conductanceMatrix[pNodeId, pNodeId] += conductance
                self._conductanceMatrix[pNodeId, nNodeId] -= conductance
                self._conductanceMatrix[nNodeId, pNodeId] -= conductance
                self._conductanceMatrix[nNodeId, nNodeId] += conductance
                
            elif comp_type == ComponentType.IDD.name:
                iddPorts = component.get_ports()
                current = component.get_current()
                pNodeId = self._nodes.index(iddPorts[0])
                nNodeId = self._nodes.index(iddPorts[1])
                self._rightSideVect[pNodeId, 0] -= current
                self._rightSideVect[nNodeId, 0] += current

            elif comp_type == ComponentType.VDD.name:
                vddPorts = component.get_ports()
                voltage = component.get_voltage()
                pNodeId = self._nodes.index(vddPorts[0])
                nNodeId = self._nodes.index(vddPorts[1])

                tmpCol = np.zeros((node_num, 1))
                tmpRow = np.zeros((1, node_num+1))
                tmpEl = np.zeros((1,1))

                tmpCol[pNodeId, 0] += 1
                tmpCol[nNodeId, 0] -= 1
                tmpRow[0, pNodeId] += 1
                tmpRow[0, nNodeId] -= 1
                tmpEl[0, 0] = voltage

                self._conductanceMatrix = np.append(self._conductanceMatrix, tmpCol, axis=1)
                self._conductanceMatrix = np.append(self._conductanceMatrix, tmpRow, axis=0)
                self._rightSideVect = np.append(self._rightSideVect, tmpEl, axis=0)

            elif comp_type == ComponentType.VDD.name:
                dioPorts = component.get_ports()
                aNodeId = self._nodes.index(dioPorts[0])
                kNodeId = self._nodes.index(dioPorts[1])
                Ud = prevVoltVect[aNodeId] - prevVoltVect[kNodeId]

                Gd, Ieq, Id = component.get_params(Ud)

                self._conductanceMatrix[aNodeId, aNodeId] += Gd
                self._conductanceMatrix[aNodeId, kNodeId] -= Gd
                self._conductanceMatrix[kNodeId, aNodeId] -= Gd
                self._conductanceMatrix[kNodeId, kNodeId] += Gd

                self._rightSideVect[aNodeId, 0] -= Ieq
                self._rightSideVect[kNodeId, 0] += Ieq

            else:
                pass

        # delete ground node from conductance matrix
        gndNodeIndex = self._nodes.index(self._gndNode)
        self._conductanceMatrix = np.delete(self._conductanceMatrix, gndNodeIndex, 0)
        self._conductanceMatrix = np.delete(self._conductanceMatrix, gndNodeIndex, 1)
        # delete ground node from right side vector
        self._rightSideVect = np.delete(self._rightSideVect, gndNodeIndex, 0)

    def set_gnd_node(self, id):
        if id in self._nodes:
            self._gndNode = id
        else:
            raise Exception("Specified nonexistent node as GND.")

    def op_analisys(self):
        return np.linalg.solve(self._conductanceMatrix, self._rightSideVect)

    def tran_analisys(self):
        pass

    
