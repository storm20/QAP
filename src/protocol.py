from netsquid.protocols import NodeProtocol, Signals ,LocalProtocol       
import netsquid as ns
from netsquid.protocols import NodeProtocol,Signals
from program import InitStateProgram,CorrectionProgram,BSM,Hadamard_Measure,Final_correction
import random
import numpy as np
# import global_var
import pandas as pd
class GHZ_Source(NodeProtocol):
    def __init__(self, node,name, num_nodes,list_length,sr):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.sr = sr

    def run(self):
#         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
#         print(self.num_nodes)
        qubit_number = 4 
#Init phase

        #Program to initialize the qubits in the memory, input param: number of qubits
        qubit_init_program = InitStateProgram(num_qubits=qubit_number)
#         print(self.name)
        send_recv_program = CorrectionProgram(num_qubits=qubit_number)
        measure_hadamard_program = Hadamard_Measure(num_qubits=qubit_number)
        final_correction_program = Final_correction(num_qubits=qubit_number)
        #Indicator variable for case of Initial sending (without waitting port message)
        Initial_send = True
        #Get all port on this node
        #Variable to store classical and quantum ports
        list_port = [k for k in self.node.ports.keys()]
#         print(list_port)
        list_classic = []
        list_quantum = []
        first_party = False      
        #Put classical ports in list_classic and quantum ports in list_quantum
#         print(list_port)
        for i in range(len(list_port)):
            if (list_port[i][0] == 'c'):
                list_classic.append(list_port[i])
            else:
                list_quantum.append(list_port[i])
#         print(list_classic[-1])
#         print(list_quantum)
#         print(list_classic)
        
        for i in range(len(list_quantum)):
            if ((list_quantum[i][1]) == 'o'):
                port_qo = list_quantum[i] #Quantum Input Port
            if ((list_quantum[i][1]) == 'i'):
                port_qi = list_quantum[i] #Quantum Output Port
#         print(self.node.name[1])
        node_num = int(self.node.name.replace('P','')) # Current Node Number    

        #Initialize loop count for number of state that has been distributed
        k = 0
        #Initialize count for list length
        x = 0
        
        
# Program Start    
        #Exec init program(create qubits in memory and apply Hadamard gate)
#         self.node.qmemory.execute_program(qubit_init_program)
        #Loop For Program
        while True:
#             print(f"Index of program: {k}")
            print("Node 1 Start")

            # If sender is also the first node
            # Initialize Qubits
            print("Node 1 preparing qubits")
            self.node.qmemory.execute_program(qubit_init_program)
#             print(self.node.qmemory.peek(positions=0))
#             yield(self.node.qmemory.execute_program(qubit_init_program))
            yield self.await_program(self.node.qmemory)
            print("Node 1 Qubit initialized")
            
            if self.sr == 1:
                #Perform CNOT
                self.node.qmemory.execute_program(send_recv_program,node_num=1,sr=self.sr,value=0)
                yield self.await_program(self.node.qmemory)
                
            #Send 2nd qubit to Next node
            qubit1 = self.node.qmemory.pop(positions=1)
            print(qubit1)
            self.node.ports[port_qo].tx_output(qubit1)
            print("Node 1 send to Node 2")
            
            #Await last party message, indicating relay is complete
            print("Node 1 waitting for last relay message")
            yield self.await_port_input(self.node.ports[list_classic[-1]])
            

            #Perform hadamard measurement
            self.node.qmemory.execute_program(measure_hadamard_program,mem_pos=0)
            yield self.await_program(self.node.qmemory)
            print("Node 1 Hadamard Measurement")

            #Broadcast measurement results
            for i in range(self.num_nodes-1):
                self.node.ports[list_classic[i]].tx_output(measure_hadamard_program.output["H"][0])
            yield self.await_port_input(self.node.ports[list_classic[-1]])
            print("Node 1 broadcast measurement results")
            message = self.node.ports[list_port[list_classic[-1]]].rx_input().items[0]
            
            #If first party is sender
            if sr == 1:
                # Perform correction
                if message == measure_hadamard_program.output["H"][0]:
                    self.node.qmemory.execute_program(final_correction_program,value=0)
                else:
                    self.node.qmemory.execute_program(final_correction_program,value=1)
                yield self.await_program(self.node.qmemory)
                

                

class Node(NodeProtocol):
    def __init__(self, node,name, num_nodes,list_length,sr):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.sr = sr

    def run(self):
    #         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
    #         print(self.num_nodes) 
        qubit_number = 4 
    #Init phase
        #Program to initialize the qubits in the memory, input param: number of qubits
        qubit_init_program = InitStateProgram(num_qubits=qubit_number)
    #         print(self.name)
        send_recv_program = CorrectionProgram(num_qubits=qubit_number)
        measure_hadamard_program = Hadamard_Measure(num_qubits=qubit_number)
        final_correction_program = Final_correction(num_qubits=qubit_number)
        bsm_measurement_program = BSM(num_qubits=qubit_number)

        #Get all port on this node
        #Variable to store classical and quantum ports
        list_port = [k for k in self.node.ports.keys()]
#         print(list_port)
        list_classic = []
        list_quantum = []
        first_party = False      
        #Put classical ports in list_classic and quantum ports in list_quantum
    #         print(list_port)
        for i in range(len(list_port)):
            if (list_port[i][0] == 'c'):
                list_classic.append(list_port[i])
            else:
                list_quantum.append(list_port[i])
    #         print(list_classic[-1])
#         print(list_quantum)
#         print(list_classic)

        for i in range(len(list_quantum)):
            if ((list_quantum[i][1]) == 'o'):
                port_qo = list_quantum[i] #Quantum Input Port
            if ((list_quantum[i][1]) == 'i'):
                port_qi = list_quantum[i] #Quantum Output Port
    #         print(self.node.name[1])
        node_num = int(self.node.name.replace('P','')) # Current Node Number    

        #Initialize loop count for number of state that has been distributed
        k = 0
        #Initialize count for list length
        x = 0

    # Program Start    
        #Exec init program(create qubits in memory and apply Hadamard gate)
#         self.node.qmemory.execute_program(qubit_init_program)
        #Loop For Program
        while True:
            
            print(f"node {node_num} init qubits")
            self.node.qmemory.execute_program(qubit_init_program)
            yield self.await_program(self.node.qmemory)
            print(f"node {node_num} waitting from node {node_num-1}")
            #Wait for quantum state input in quantum port
#             print(self.node.ports[port_qi].input_queue)
            yield self.await_port_input(self.node.ports[port_qi])
            print(self.node.ports[port_qi].input_queue)
            print(self.node.qmemory.peek(positions=3))
            
            #If node is sender or receiver
            print(f"Node {node_num} BSM")
            yield self.node.qmemory.execute_program(bsm_measurement_program)
            print("Finished BSM")
#             output = bsm_measurement_program.output["M"]
#             print(output)
            #Perform BSM, Correction, and CNOT If last node is sender
            if self.sr == 1:
                print(f"Node {node_num} Correction and CNOT")
                yield self.node.qmemory.execute_program(send_recv_program,node_num=node_num,sr=1,value=bsm_measurement_program.output["M"][0])
            else:
                print(f"Node {node_num} Correction")
                yield self.node.qmemory.execute_program(send_recv_program,node_num=node_num,sr=0,value=bsm_measurement_program.output["M"][0])

            
            #Send the qubit to the next 
            print(f"node {node_num} send qubit to node {node_num+1}")
            qubit1 = self.node.qmemory.pop(positions=1)
            self.node.ports[port_qo].tx_output(qubit1)
            
            print(f"node {node_num} waitting for finished relay")
           #Wait for broadcast result from last node 
            yield self.await_port_input(self.node.ports[list_classic[-1]])
            message = self.node.ports[list_port[list_classic[-1]]].rx_input().items[0]
            
            print(f"node {node_num} waitting hadamard measurement results from node 4")
            yield self.await_port_input(self.node.ports[list_classic[-1]])
            message1 = self.node.ports[list_port[list_classic[-1]]].rx_input().items[0]
            
            print(f"node {node_num} wait for hadamard measurement results from node 1")
            #Wait for broadcast result from last first node 
            yield self.await_port_input(self.node.ports[list_classic[0]])
            message2 = self.node.ports[list_port[list_classic[0]]].rx_input().items[0]
            
            if self.sr == 1:
                
                if message1 == message2:
                    print(f"node {node_num} apply correction")
                    yield self.node.qmemory.execute_program(final_correction_program,value=0)
                else:
                    yield self.node.qmemory.execute_program(final_correction_program,value=1)
#                 yield self.await_program(self.node.qmemory)
 

                    

