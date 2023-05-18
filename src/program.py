from netsquid.components.qprogram import QuantumProgram
# from my_operator import *
from netsquid.qubits.operators import Operator
import netsquid.components.instructions as instr

from netsquid.components.qprogram import QuantumProgram

class InitStateProgram(QuantumProgram):
    # default_num_qubits = 4
# Program to initialize quantum state
# Initialized quantum state are: 0-> First qubit of Phi+, 1-> Second qubit of Phi-, 2-> Ancillary 0 state, 3-> empty(to receive q state)
    def program(self):
#         self.num_qubits = int(np.log2(self.num_qubits))
        qubits = self.get_qubit_indices()
#         print(qubits)
#         print("Init qubits 0")
        self.apply(instr.INSTR_INIT, qubits) # Initialize all memory into 0 state
#         print("Apply Hadamard")
        self.apply(instr.INSTR_H,qubits[0])# apply Hadamard 
        for i in range(self.num_qubits-1):
            self.apply(instr.INSTR_CNOT, [qubits[0], qubits[i+1]])# Apply CNOT 
#         print("Finish Init Program")
        yield self.run()
        
                
class Encode_Op(QuantumProgram):
#Program to apply hadamard measurement for P1 and Pn(last party)
    def program(self):
        qubits = self.get_qubit_indices(1)
        self.apply(instr.INSTR_X,qubits[0])
        yield self.run()
        
        
class Hadamard_Op(QuantumProgram):
#Program to apply hadamard measurement for P1 and Pn(last party)
    def program(self):
        # print("TEST")
        qubits = self.get_qubit_indices(1)
        self.apply(instr.INSTR_H,qubits[0])
        yield self.run()
        
# class Hadamard_Op1(QuantumProgram):
# #Program to apply hadamard measurement for P1 and Pn(last party)
#     def program(self,mempos):
#         qubits = self.get_qubit_indices(1)
#         # print(qubits)
#         self.apply(instr.INSTR_H,qubits)
#         yield self.run()
        
class Measure_Z(QuantumProgram):
#Program to apply final correction for sender only, input argument: value 0 if both result same, 1 if both result differ
    def program(self):
        qubits = self.get_qubit_indices(1)
        self.apply(instr.INSTR_MEASURE,0,output_key="m")
        yield self.run()
