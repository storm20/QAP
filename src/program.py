from netsquid.components.qprogram import QuantumProgram
# from my_operator import *
from netsquid.qubits.operators import Operator
import netsquid.components.instructions as instr

from netsquid.components.qprogram import QuantumProgram

class InitStateProgram(QuantumProgram):
    default_num_qubits = 4
# Program to initialize quantum state
# Initialized quantum state are: 0-> First qubit of Phi+, 1-> Second qubit of Phi-, 2-> Ancillary 0 state, 3-> empty(to receive q state)
    def program(self):
#         self.num_qubits = int(np.log2(self.num_qubits))
        qubits = self.get_qubit_indices()
#         print(qubits)
#         print("Init qubits 0")
        self.apply(instr.INSTR_INIT, [qubits[0],qubits[1],qubits[2]]) # Initialize all memory into 0 state
#         print("Apply Hadamard")
        self.apply(instr.INSTR_H,qubits[1])# apply Hadamard into q2
#         for i in range(self.num_qubits):
#             if i % 2 != 0:
#                 self.apply(instr.INSTR_H, qubits[i])
#                 print(f"Node 1 apply hadamard to pos {i}")
#         print(qubits)
#         print("Apply CNOT")
        self.apply(instr.INSTR_CNOT, [qubits[1], qubits[0]])# Apply CNOT to turn q1 and q2 into Phi+ state
#         print("Finish Init Program")
        yield self.run()
        
class CorrectionProgram(QuantumProgram):
#Program to apply BSM and CNOT for sender and receiver only
    def program(self,node_num,sr,value):
        qubits = self.get_qubit_indices()
        if node_num != 1:
            print("Program apply Correction")
            if value == 1:
                self.apply(instr.INSTR_X,qubits[1])
            elif value == 2:
                self.apply(instr.INSTR_X,qubits[1])
                self.apply(instr.INSTR_Z,qubits[1])
            elif value == 3:
                self.apply(instr.INSTR_Z,qubits[1])
#             yield self.run()
            if sr == 1:
                print("Program apply CNOT")
                self.apply(instr.INSTR_CNOT,[qubits[1],qubits[2]])
            yield self.run()
        elif node_num == 1 and sr==1:
            print("Program apply CNOT only")
            self.apply(instr.INSTR_CNOT,[qubits[1],qubits[2]])
            yield self.run()
        
class BSM(QuantumProgram):
#Program to apply BSM and its correction for non sender and receiver
    def program(self):
        print("Program BSM")
        qubits = self.get_qubit_indices()
        self.apply(instr.INSTR_MEASURE_BELL,[qubits[0],qubits[3]],output_key="M")
        yield self.run()
        
        
# class BSM(QuantumProgram):
# #     default_num_qubits = 4  
#     def program(self):
#         qubits = self.get_qubit_indices()
#         print(qubits)
#         print("Apply CNOT")
#         self.apply(instr.INSTR_CNOT, [qubits[0], qubits[3]])
#         print("Apply H gate")
#         self.apply(instr.INSTR_H, qubits[0])
#         print("Measure first qubit")
#         self.apply(instr.INSTR_MEASURE, qubits[0], output_key="M1")
#         print("Measure second qubit")
#         self.apply(instr.INSTR_MEASURE, qubits[3], output_key="M2")
#         yield self.run()
class Hadamard_Measure(QuantumProgram):
#Program to apply hadamard measurement for P1 and Pn(last party)
    def program(self,mem_pos):
        qubits = self.get_qubit_indices()
        self.apply(instr.INSTR_MEASURE_X,mem_pos,output_key = "H")
        yield self.run()
        
class Final_correction(QuantumProgram):
#Program to apply final correction for sender only, input argument: value 0 if both result same, 1 if both result differ
    def program(self,value):
        qubits = self.get_qubit_indices()
        if value == 1:
            self.apply(instr.INSTR_Z,[qubits[2]])
            yield self.run()
