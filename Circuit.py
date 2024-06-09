import numpy as np
from Component import *
import Constants

class AnalysisType(Enum):
    OP = 1
    TRAN = 2

class Circuit:

    def __init__(self):
        self._elements = []  # List of elements present in the circuit
        self._nodes = []     # List of nodes present in the circuit
        self._resultVect = np.empty(0)
        self._rightSideVect = np.empty(0)
        self._conductanceMatrix = np.empty(0)
        self._gndNode = 0
        self._firsIteration = True

        self._opAnalysisResult = np.empty(0)
        self._opAnalysisStatus = OPAnalysisStatus()

        self._tranSimulationTime = 0.0
        self._tranStepLength = 0.0
        self._tranInitialOPResult = np.empty(0)
        self._tranInitialOPCurrent = np.empty(0)
        self._tranAnalysisResult = np.empty(0)
        self._tranAnalysisTimescale = np.empty(0)
        self._tranAnalysisStatus = TRANAnalysisStatus()

    def add_element(self, element: Component):
        """
        Adds component to the circuit. It appends it to the element list and adding its nodes 
        to node list if they are not present already.
        
        Parameters:
            (Component) element: Component to be added to the circuit.
        Returns:
            None
        """
        self._elements.append(element)
        tmpPorts = element.get_ports()
        for port in tmpPorts:
            if port not in self._nodes:
                self._nodes.append(port)

    def set_gnd_node(self, id):
        """
        This function assigns the ID of the ground node in the circuit.
        
        Parameters:
            (int) GND node ID - must be already present in the circuit.
        Returns:
            None
        """
         
        if id in self._nodes:
            self._gndNode = id
        else:
            raise Exception("Specified nonexistent node as GND.")

    def op_analysis(self):
        returnStatus = False
        iterationNumber = 0
        # Dummy matrix construction to get final length of voltage vector - some elements rows.
        self._firsIteration = True
        self._construct_matrix() 
        exceededIterationNumber = True
        for i in range(0, Constants.OP_IRER_NUM):
            prevVoltageVect = self._resultVect
            prevCurrVect = self._rightSideVect

            # Create matrix for this step and perform calculations
            self._construct_matrix()
            self._resultVect = np.linalg.solve(self._conductanceMatrix, self._rightSideVect)
            self._resultVect = self._append_gnd_node(self._resultVect)

            # Check calculation end conditions
            voltCheck = self._check_voltage_break_condition(self._resultVect, prevVoltageVect)
            currCheck = self._check_current_break_condition(self._rightSideVect, prevCurrVect)
            if (voltCheck and currCheck):
                exceededIterationNumber = False
                iterationNumber = i
                returnStatus = True # Simulation completed succesfully
                break
        if(exceededIterationNumber):
            iterationNumber = Constants.OP_ITER_NUM
            print("Exceeded iteration number.")
        # Save calculation result and status
        self._opAnalysisResult = self._resultVect
        self._opAnalysisStatus.set_status(returnStatus, voltCheck, currCheck, iterationNumber)

        return returnStatus

    def tran_analysis(self, startT, stopT, step):
        tranReturnStatus = False
        # First perform OP analisys to get initial operating point of the circuit
        opAnlReturnStat = self.op_analysis()
        # If OP analysis failed, exit function with error
        if opAnlReturnStat == False:
           return tranReturnStatus
        # Store results of the OP analysis
        tranInitialOPResult = self._opAnalysisResult
        tranInitialOPCurrent = self._rightSideVect

        # Perform tran analisys
        # Get timescale and number of steps from given parameters
        stepsNumber = (int)((stopT - startT) / step)
        self._tranAnalysisTimescale = np.linspace(startT, stopT, stepsNumber)
        self._tranStepLength = step

        # List for results of circuit analisys in all time steps
        # After all operations it will be converted to 2D numpy array
        tranResults = []

        # Calculate every step from the timescale
        for i in range(stepsNumber):
            print("Timestep ", i)
            # Dummy matrix construction to get final length of voltage vector - some elements rows.
            self._firsIteration = True
            self._construct_matrix(AnalysisType.TRAN) 
            # Status variables of varius checks in the calculations
            exceededIterationNumber = True
            voltCheck = False
            currCheck = False
            for j in range(0, Constants.OP_IRER_NUM):
                # In first iteration use results from previous analysis
                if j == 0:
                    prevVoltageVect = tranInitialOPResult
                    self._resultVect = tranInitialOPResult
                    prevCurrVect = tranInitialOPCurrent
                else:
                    prevVoltageVect = self._resultVect
                    prevCurrVect = self._rightSideVect

                # Create matrix for this step and perform calculations
                self._construct_matrix(AnalysisType.TRAN)
                self._resultVect = np.linalg.solve(self._conductanceMatrix, self._rightSideVect)
                self._resultVect = self._append_gnd_node(self._resultVect)

                # Check calculation end conditions
                voltCheck = self._check_voltage_break_condition(self._resultVect, prevVoltageVect)
                currCheck = self._check_current_break_condition(self._rightSideVect, prevCurrVect)
                if (voltCheck and currCheck):
                    exceededIterationNumber = False
                    iterationNumber = j
                    break
            if(exceededIterationNumber):
                iterationNumber = Constants.OP_IRER_NUM
                print("TRAN exceeded iteration number at time: ", self._tranSimulationTime)
                self._tranAnalysisStatus.set_fail_time(self._tranSimulationTime)
                self._tranAnalysisStatus.set_return_status(tranReturnStatus)
                return tranReturnStatus

            # Save status of this timestep
            self._tranAnalysisStatus.append_status(voltCheck, currCheck, iterationNumber)
            # Add result of this time step to result list
            tranResults.append(self._resultVect)

            # Store those vectors, so they can serve as starting point in next time step
            tranInitialOPResult = self._resultVect
            tranInitialOPCurrent = self._rightSideVect

            self._tranSimulationTime += self._tranStepLength

        # Save all output data of the TRAN simulation
        tranResults = np.array(tranResults)
        print(tranResults.shape)
        np.savetxt("tranWyniki.txt", tranResults[:,:,0])
        self._tranAnalysisResult = tranResults

        # Save status of the simulation and exit
        tranReturnStatus = True
        self._tranAnalysisStatus.set_return_status(tranReturnStatus)
        return tranReturnStatus

    def display_op_analysis_results(self):
        # Generate labels for all elements of result vector
        labels = []
        # Add schematic node names ...
        for node in self._nodes:
            labels.append("V" + str(node))
        # ... and name of currents going through voltage sources
        for element in self._elements:
            type = element.get_type()
            if type == ComponentType.VDD or type == ComponentType.VAC:
                id = element.get_id()
                labels.append("IE" + str(id)) 

        # Sort labels and reorder respective values
        values = self._resultVect.T
        values = values.tolist()[0]
        labels, values = (list(t) for t in zip(*sorted(zip(labels, values))))

        # Print OP analisys status report
        self._opAnalysisStatus.print()
        print("OP analysis results:")
        for label, value in zip(labels, values):
            print(label, ": ", value)

    ############################ PRIVATE HELPER FUNCTIONS ############################

    def _construct_matrix(self, analysisType: AnalysisType = AnalysisType.OP):
        """
        This function constructs conductance matrix, right side vector and result vector based on component list.
        
        Parameters
        ----------
        analisysType : AnalisysType
            Chooses which type of circuit analisys is being performed. Default is OP.
        Returns:
        ----------
                None
        """
        node_num = len(self._nodes)
        self._conductanceMatrix = np.zeros((node_num, node_num))
        self._rightSideVect = np.zeros((node_num, 1))
        # Initialise result vector with zeros in first iteration. In all others it holds result
        # of previous iterations.
        if self._firsIteration:
            self._resultVect = np.zeros((node_num, 1))
            self._firsIteration = False

        for component in self._elements:
            comp_type = component.get_type()
            if comp_type == ComponentType.R:
                self._matrix_add_resistor(component)
                
            elif comp_type == ComponentType.IDD:
                self._matrix_add_curr_source(component)

            elif comp_type == ComponentType.VDD or comp_type == ComponentType.VAC:
                self._matrix_add_volt_source(component, analysisType, comp_type)

            elif comp_type == ComponentType.DIO:
                self._matrix_add_diode(component)

            elif comp_type == ComponentType.BJT:
                self._matrix_add_BJT(component)

            elif comp_type == ComponentType.C:
                # Capacitor in OP analisys is a break in the curcuit, don't add it.
                if analysisType != AnalysisType.OP:
                    self._matrix_add_capacitor(component, self._tranStepLength)

            else:
                pass

        # delete ground node from conductance matrix
        gndNodeIndex = self._nodes.index(self._gndNode)
        self._conductanceMatrix = np.delete(self._conductanceMatrix, gndNodeIndex, 0)
        self._conductanceMatrix = np.delete(self._conductanceMatrix, gndNodeIndex, 1)
        # delete ground node from right side vector
        self._rightSideVect = np.delete(self._rightSideVect, gndNodeIndex, 0)

    def _check_voltage_break_condition(self, currVoltVect, prevVoltVect):
        voltDiff = np.absolute(np.subtract(currVoltVect, prevVoltVect))
        voltAbs = np.absolute(currVoltVect)
        prevVoltAbs = np.absolute(prevVoltVect)
        return np.all(voltDiff < np.maximum(voltAbs, prevVoltAbs) * Constants.RELTOL + Constants.VNTOL)

    def _check_current_break_condition(self, currCurrVect, prevCurrVect):
        currDiff = np.absolute(np.subtract(currCurrVect, prevCurrVect))
        currAbs = np.absolute(currCurrVect)
        prevCurrAbs = np.absolute(prevCurrVect)
        return np.all(currDiff < np.maximum(currAbs, prevCurrAbs) * Constants.RELTOL + Constants.ABSTOL)

    def _append_gnd_node(self, voltVect):
        """
        Helper function. GND node is removed from the matrix and vectors before calculations.
        However it is needed after calculations eg. for displaying. 

        Parameters:
            voltVect: Result vector to which GND node will be appended.
        
        Returns:
            Result vector with appended GND node.
        """
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
    
    #################################  COMPONENT ADD  #################################
    # Below are helper functions. They contain all the logic needed to add respective component 
    # to the matrix and vectors used in calculations. They were created to shorten the body 
    # of the construct_matrix() method and make it clearer.

    def _matrix_add_resistor(self, component):
        rPorts = component.get_ports()
        conductance = 1.0 / component.get_resistance()
        pNodeId = self._nodes.index(rPorts[0])
        nNodeId = self._nodes.index(rPorts[1])
        self._conductanceMatrix[pNodeId, pNodeId] += conductance
        self._conductanceMatrix[pNodeId, nNodeId] -= conductance
        self._conductanceMatrix[nNodeId, pNodeId] -= conductance
        self._conductanceMatrix[nNodeId, nNodeId] += conductance

    def _matrix_add_curr_source(self, component):
        iddPorts = component.get_ports()
        current = component.get_current()
        pNodeId = self._nodes.index(iddPorts[0])
        nNodeId = self._nodes.index(iddPorts[1])
        self._rightSideVect[pNodeId, 0] -= current
        self._rightSideVect[nNodeId, 0] += current

    def _matrix_add_volt_source(self, component, analysisType, sourceType):
        vddPorts = component.get_ports()
        pNodeId = self._nodes.index(vddPorts[0])
        nNodeId = self._nodes.index(vddPorts[1])

        # Get proper voltage value depending on voltage cource type and analisys type
        if sourceType == ComponentType.VDD or analysisType == AnalysisType.OP:
            voltage = component.get_voltage()
        else:
            voltage = component.get_voltage_ac(self._tranSimulationTime)

        # get the size of the conductance matrix
        cond_matrix_shape = self._conductanceMatrix.shape

        # and create temporary vectors, that will be appended to it
        # after this operation the matrix will be higher and wider by 1 element
        tmpCol = np.zeros((cond_matrix_shape[0], 1))
        tmpRow = np.zeros((1, cond_matrix_shape[0]+1))
        tmpEl = np.zeros((1,1))

        # Construct voltage source stamp
        tmpCol[pNodeId, 0] += 1
        tmpCol[nNodeId, 0] -= 1
        tmpRow[0, pNodeId] += 1
        tmpRow[0, nNodeId] -= 1
        tmpEl[0, 0] = voltage

        # Append new column and row to the conductance matrix
        self._conductanceMatrix = np.append(self._conductanceMatrix, tmpCol, axis=1)
        self._conductanceMatrix = np.append(self._conductanceMatrix, tmpRow, axis=0)
        # Append new element containing voltage to right side vector
        self._rightSideVect = np.append(self._rightSideVect, tmpEl, axis=0)
        # Append new element to the result vector. Set its initial value to 0.0 V
        tmpEl[0, 0] = 0.0
        self._resultVect = np.append(self._resultVect, tmpEl, axis=0)

    def _matrix_add_diode(self, component):
        dioPorts = component.get_ports()
        aNodeId = self._nodes.index(dioPorts[0])
        kNodeId = self._nodes.index(dioPorts[1])
        Ud = self._resultVect[aNodeId] - self._resultVect[kNodeId]

        Gd, Ieq = component.get_params(Ud)

        self._conductanceMatrix[aNodeId, aNodeId] += Gd
        self._conductanceMatrix[aNodeId, kNodeId] -= Gd
        self._conductanceMatrix[kNodeId, aNodeId] -= Gd
        self._conductanceMatrix[kNodeId, kNodeId] += Gd

        self._rightSideVect[aNodeId, 0] -= Ieq
        self._rightSideVect[kNodeId, 0] += Ieq

    def _matrix_add_BJT(self, component):
        bjtPorts = component.get_ports()
        cNodeId = self._nodes.index(bjtPorts[0])
        bNodeId = self._nodes.index(bjtPorts[1])
        eNodeId = self._nodes.index(bjtPorts[2])

        Ube = self._resultVect[bNodeId] - self._resultVect[eNodeId]
        Ubc = self._resultVect[bNodeId] - self._resultVect[cNodeId]

        Ieqc, Ieqe, Gbc, Gbe, alphaF = component.get_params(Ube, Ubc)

        self._conductanceMatrix[cNodeId, cNodeId] += Gbc
        self._conductanceMatrix[cNodeId, bNodeId] += alphaF * Gbe - Gbc
        self._conductanceMatrix[cNodeId, eNodeId] -= alphaF * Gbe
        self._conductanceMatrix[bNodeId, cNodeId] += (alphaF - 1.0) * Gbc
        self._conductanceMatrix[bNodeId, bNodeId] += (1.0 - alphaF) * (Gbc + Gbe)
        self._conductanceMatrix[bNodeId, eNodeId] += (alphaF - 1.0) * Gbe
        self._conductanceMatrix[eNodeId, cNodeId] -= alphaF * Gbc
        self._conductanceMatrix[eNodeId, bNodeId] += alphaF * Gbc - Gbe
        self._conductanceMatrix[eNodeId, eNodeId] += Gbe

        self._rightSideVect[cNodeId, 0] += Ieqc - alphaF * Ieqe
        self._rightSideVect[bNodeId, 0] -= (1.0 - alphaF) * (Ieqc + Ieqe)
        self._rightSideVect[eNodeId, 0] += Ieqe - alphaF * Ieqc

    def _matrix_add_capacitor(self, component, stepLen):
        capPorts = component.get_ports()
        pNodeId = self._nodes.index(capPorts[0])
        nNodeId = self._nodes.index(capPorts[1])
        Ud = self._resultVect[pNodeId] - self._resultVect[nNodeId]

        Gc, Ieq = component.get_params(Ud, stepLen)

        self._conductanceMatrix[pNodeId, pNodeId] += Gc
        self._conductanceMatrix[pNodeId, nNodeId] -= Gc
        self._conductanceMatrix[nNodeId, pNodeId] -= Gc
        self._conductanceMatrix[nNodeId, nNodeId] += Gc

        self._rightSideVect[pNodeId, 0] -= Ieq
        self._rightSideVect[nNodeId, 0] += Ieq

################################ HELPER CLASSES ################################

class OPAnalysisStatus():

    def __init__(self, exitStatus=False, voltCond=False, currCond=False, iter=0):
        """
        Class containing data about the OP analysis result

        Parameters
        ----------
        exitStatus : bool
            Exit status of the analysis. False - failed, True - succes
        voltCond : bool
            Status of the voltage condition. False - not met, True - met
        currCond : bool
            Status of the current condition. False - not met, True - met
        iter : int
            Number of iterations performed to get the result.
        """
        self._exitStatus = exitStatus
        self._voltageCondition = voltCond
        self._currentCondition = currCond
        self._iterationNumber = iter

    def get_status(self):
        return self._exitStatus, self._voltageCondition, self._currentCondition, self._iterationNumber
    
    def set_status(self, exitStatus=False, voltCond=False, currCond=False, iter=0):
        self._exitStatus = exitStatus
        self._voltageCondition = voltCond
        self._currentCondition = currCond
        self._iterationNumber = iter

    def print(self):
        if self._exitStatus:
            print("OP analisys was completed succesfully in ", self._iterationNumber, " iterations.")
            if self._voltageCondition:
                print("Voltage condition was met.")
            else:
                print("Voltage condition was not met.")
            if self._currentCondition:
                print("Current condition was met.")
            else:
                print("Current condition was not met.")
        else:
            print("OP analisys exceeded iteration number")
        
class TRANAnalysisStatus():
    
    def __init__(self):
        self._returnStatus = False
        self._failTime = 0.0
        self._timeStepsNumber = 0
        self._voltageCondition = []
        self._currentCondition = []
        self._iterationNumber = []

    def get_status(self):
        return self._returnStatus, self._failTime, self._timeSteps, self._voltageCondition, self._currentCondition, self._iterationNumber
    
    def append_status(self, voltCond=False, currCond=False, iter=0):
        self._voltageCondition.append(voltCond)
        self._currentCondition.append(currCond)
        self._iterationNumber.append(iter)

    def set_return_status(self, retStat):
        self._returnStatus = retStat

    def set_fail_time(self, time):
        self._failTime = time

    def set_time_steps_number(self, num):
        self._timeStepsNumber = num

    def print(self):
        if self._returnStatus:
            print("TRAN analysis was completed succesfully")
            print("Average number of iterations: ", (int)(np.average(self._iterationNumber)))
            print("Minimum number of iterations: ", np.min(self._iterationNumber))
            print("Maximum number of iterations: ", np.max(self._iterationNumber))
        else:
            print("TRAN analisys failed")
