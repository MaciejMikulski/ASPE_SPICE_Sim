import numpy as np
from Component import *

class Circuit:

    def __init__(self):
        self._elements = []
        self._nodes = []
        self._resultVect = np.empty(0)
        self._rightSideVect = np.empty(0)
        self._conductanceMatrix = np.empty(0)
        self._gndNode = 0
        self._firsIteration = True

    def add_element(self, element: Component):
        self._elements.append(element)
        tmpPorts = element.get_ports()
        for port in tmpPorts:
            if port not in self._nodes:
                self._nodes.append(port)
        
    def construct_matrix(self):
        node_num = len(self._nodes)
        self._conductanceMatrix = np.zeros((node_num, node_num))
        self._rightSideVect = np.zeros((node_num, 1))
        if self._firsIteration:
            self._resultVect = np.zeros((node_num, 1))
            self._firsIteration = False

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
                tmpEl[0, 0] = 0.0
                self._resultVect = np.append(self._resultVect, tmpEl, axis=0)

            elif comp_type == ComponentType.DIO.name:
                dioPorts = component.get_ports()
                aNodeId = self._nodes.index(dioPorts[0])
                kNodeId = self._nodes.index(dioPorts[1])
                Ud = self._resultVect[aNodeId] - self._resultVect[kNodeId]

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
        self.construct_matrix() # Dummy matrix construction to get final length of voltage vect


        for i in range(0, 20):
            _prevVoltageVect = self._resultVect

            self.construct_matrix()

            self._resultVect = np.linalg.solve(self._conductanceMatrix, self._rightSideVect)
            self._resultVect = self._append_gnd_node(self._resultVect)
            diff = np.absolute(np.subtract(_prevVoltageVect, self._resultVect))
            if np.amax(diff) < 0.001:
                print("Ended in " + str(i) + " iteration")
                break

        return self._resultVect

    def tran_analisys(self):
        pass

    def _append_gnd_node(self, voltVect):
        rowNum = len(self._resultVect) + 1 # Add one node - GND
        gndVoltVect = _voltageVectGND = np.zeros((rowNum, 1))
        gndIndex = self._nodes.index(self._gndNode)

        for i in range(0, rowNum):
            if i < gndIndex:
                gndVoltVect[i, 0] = voltVect[i, 0]
            elif i == gndIndex:
                gndVoltVect[i, 0] = 0.0
            else:
                gndVoltVect[i, 0] = voltVect[i-1, 0]

        return gndVoltVect
