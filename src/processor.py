import numpy as np
import netsquid as ns
import netsquid.components.instructions as instr
from netsquid.components.qprocessor import QuantumProcessor
from netsquid.components.qprocessor import PhysicalInstruction
from netsquid.qubits.qubitapi import *
from netsquid.util.constrainedmap import ValueConstraint

# from my_operator import *

from netsquid.components.models.qerrormodels import QuantumErrorModel


# class DepolarNoiseGlobalModel(QuantumErrorModel):
#     """Model for applying depolarizing noise to qubit(s) on a quantum component.

#     Parameters
#     ----------
#    probability: probability that noise will be applied (p)
#     """

#     def __init__(self, depolar_rate, **kwargs):
#         super().__init__(**kwargs)
        
#         def depolar_rate_constraint(value):
#                 if  not 0 <= value <= 1:
#                     return False
#                 elif value < 0:
#                     return False
#                 return True
#         self.add_property('depolar_rate', depolar_rate,
#                             value_type=(int, float),
#                             value_constraints=ValueConstraint(depolar_rate_constraint))
#     @property
#     def depolar_rate(self):
#         """float: probability that a qubit will depolarize with time. If
#         :attr:`~netsquid.components.models.qerrormodels.DepolarNoiseModel.time_independent`
#         is False, then this is the exponential depolarizing rate per unit time [Hz].
#         If True, it is a probability."""
#         return self.properties['depolar_rate']

#     @depolar_rate.setter
#     def depolar_rate(self, value):
#         self.properties['depolar_rate'] = value

#     def error_operation(self, qubits,**kwargs):
#         """Error operation to apply to qubits.

#         Parameters
#         ----------
#         qubits : tuple of :obj:`~netsquid.qubits.qubit.Qubit`
#             Qubits to apply noise to.
        

#         """
#         num_qubits = len(qubits)
#         max_mix_state = (np.eye(2**num_qubits)/2**num_qubits)
#         output_state = self.depolar_rate*(max_mix_state) + (1-self.depolar_rate)*reduced_dm(qubits)
#         # print(output_state)
#         assign_qstate(qubits,output_state)






def create_processor(num_parties,prob):
    num_qubits = num_parties
#     print(f"Processor number of qubit: {num_qubits}")
#     top = list(range(0,num_qubits))
#     tuple_top = tuple(top)
#     print(f"list of topology{top}")
#     print(f"tuple of topology{tuple_top}")
    # print(prob)
    # Model = DepolarNoiseGlobalModel(depolar_rate = prob)
    # We'll give both Alice and Bob the same kind of processor
    physical_instructions = [
        PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
        PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_CNOT, duration = 1, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE_BELL, duration=7, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE_X, duration=7, parallel=True)
    ]
    processor = QuantumProcessor("quantum_processor", num_positions=num_qubits,phys_instructions=physical_instructions)
    # processor = QuantumProcessor("quantum_processor", num_positions=num_qubits,mem_noise_models=Model,phys_instructions=physical_instructions)
    return processor



