import netsquid as ns
import netsquid.components.instructions as instr
from netsquid.components.qprocessor import QuantumProcessor
from netsquid.components.qprocessor import PhysicalInstruction
# from my_operator import *
from netsquid.qubits.operators import Operator

def create_processor(num_parties,prob):
    num_qubits = num_parties
#     print(f"Processor number of qubit: {num_qubits}")
#     top = list(range(0,num_qubits))
#     tuple_top = tuple(top)
#     print(f"list of topology{top}")
#     print(f"tuple of topology{tuple_top}")

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
    return processor