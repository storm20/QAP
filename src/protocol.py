from netsquid.protocols import NodeProtocol, Signals ,LocalProtocol       
import netsquid as ns
from netsquid.protocols import NodeProtocol,Signals
from program import InitStateProgram,Encode_Op,Hadamard_Op,Measure_Z
import random
import numpy as np
import global_var
import pandas as pd
from netsquid.qubits.qubitapi import *

class CSP(NodeProtocol):
    def __init__(self, node,name, num_nodes,list_length,prob):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.prob = prob

    def run(self):
#         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
        # print(self.num_nodes)
        qubit_number = self.num_nodes 
#Init phase

        #Program to initialize the qubits in the memory, input param: number of qubits
        qubit_init_program = InitStateProgram(num_qubits=qubit_number)
        hadamard_program = Hadamard_Op()
        # hadamard_program = Hadamard_Op1()
        measurement_program = Measure_Z()
        
#         print(self.name)
        
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
        
        # for i in range(len(list_quantum)):
        #     if ((list_quantum[i][1]) == 'o'):
        #         port_qo = list_quantum[i] #Quantum Input Port
        #     if ((list_quantum[i][1]) == 'i'):
        #         port_qi = list_quantum[i] #Quantum Output Port
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
            # print("CSP Start")
            # If sender is also the first node
            # Initialize Qubits
            # print("CSP preparing qubits")
            self.node.qmemory.execute_program(qubit_init_program)
#             print(self.node.qmemory.peek(positions=0))
#             yield(self.node.qmemory.execute_program(qubit_init_program))
            yield self.await_program(self.node.qmemory)
            # print("CSP Qubit initialized")

                
            #Send all qubits to all nodes
            # print(list_quantum)
            
            # Global noise apply, comment if not used
            # max_mix_state = (np.eye(2**qubit_number)/2**qubit_number)
            # position = list(np.arange(0,qubit_number))
            # qubit_temp = self.node.qmemory.pop(positions=position)
            # # print(reduced_dm(qubit_temp))
            # output_state = self.prob*(max_mix_state) + (1-self.prob)*reduced_dm(qubit_temp)
            # assign_qstate(qubit_temp,output_state)
            # self.node.qmemory.put(qubit_temp,position)
            
            
            for i in range (len(list_quantum)):
                qubit = self.node.qmemory.pop(positions=i+1)
                # print(qubit)
                self.node.ports[list_quantum[i]].tx_output(qubit)
                # print(f"CSP send to Node {list_quantum[i][-1]}")
            

            #Perform hadamard 
            # print("TEST HADAMARD")
            # print(self.node.qmemory.pop(positions=0))
            # print(self.node.qmemory.mem_positions)
            yield self.node.qmemory.execute_program(hadamard_program)
            # yield self.await_program(self.node.qmemory)
            # print("CSP Hadamard Apply")
            
            
            

            #Measure
            yield self.node.qmemory.execute_program(measurement_program)
            # meas = np.ndarray(shape=(qubit_number,1))
            meas, = measurement_program.output['m']
            # print(meas)
            #Receive measurement results and calculate mod
            sum = meas
            for i in range(self.num_nodes-2):
                # print(f"CSP awaits from {list_classic[i]}")
                if len(self.node.ports[list_classic[i]].input_queue) == 0:
                    yield self.await_port_input(self.node.ports[list_classic[i]])
                    message = self.node.ports[list_classic[i]].rx_input().items[0]
                else:
                    message = (self.node.ports[list_classic[i]].input_queue[0][1].items[0])
                # print(self.node.ports)
                
                # print("MESSAGE")
                # print(message)
                sum = sum + message
            sum = sum % 2
            # print("CSP calculate message modulo")
            # Send to IS
            self.node.ports[list_classic[-1]].tx_output(sum)
            # print("CSP send measurement results to IS")  

class Users(NodeProtocol):
    def __init__(self, node,name, num_nodes,list_length,sr):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.sr = sr

    def run(self):
    #         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
    #         print(self.num_nodes) 
        # qubit_number = 4 
    #Init phase
        #Program to initialize the qubits in the memory, input param: number of qubits

    #         print(self.name)
        hadamard_program = Hadamard_Op()
        measurement_program = Measure_Z()
        encode_program = Encode_Op()

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
        sender = False
        if self.sr == node_num:
            sender = True
    # Program Start    
        #Exec init program(create qubits in memory and apply Hadamard gate)
#         self.node.qmemory.execute_program(qubit_init_program)
        #Loop For Program
        while True:

            # print(f"node {node_num} waitting from node {node_num-1}")
            #Wait for quantum state input in quantum port
#             print(self.node.ports[port_qi].input_queue)
            yield self.await_port_input(self.node.ports[port_qi])
            # print(self.node.ports[port_qi].input_queue)
            # print(self.node.qmemory.peek(positions=3))
            
            
            
            #Perform hadamard 
            self.node.qmemory.execute_program(hadamard_program)
            yield self.await_program(self.node.qmemory)
            # print(f"Node {node_num} Hadamard Apply")
            
            if sender:
                # print(f"Node {node_num} Encode")
                if x % 2 == 0:
                    pub_data = np.random.binomial(1,0.5)
                if (pub_data == 1):
                    yield self.node.qmemory.execute_program(encode_program)
                # print(f"Published data: {pub_data}")
                global_var.modify(pub_data,x,0)
                x = x+1
            #Measure
            yield self.node.qmemory.execute_program(measurement_program)
            # meas = np.ndarray(shape=(qubit_number,1))
            meas, = measurement_program.output['m']

            #Send measurement results to CSP
            self.node.ports[list_classic[0]].tx_output(meas)
            if (x > self.list_length-1):
                # print(f"Node {node_num} list distribution ended at: {ns.sim_time(ns.MILLISECOND )} ms")
                self.stop()
          

class IS(NodeProtocol):
    def __init__(self, node,name, num_nodes,list_length):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length


    def run(self):
    #         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
    #         print(self.num_nodes) 
    #Init phase
        #Program to initialize the qubits in the memory, input param: number of qubits
        hadamard_program = Hadamard_Op()
        measurement_program = Measure_Z()

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
            
            # print(f"IS waitting from node 1")
            #Wait for quantum state input in quantum port
#             print(self.node.ports[port_qi].input_queue)
            yield self.await_port_input(self.node.ports[port_qi])
            # print(self.node.ports[port_qi].input_queue)
            # print(self.node.qmemory.peek(positions=3))
            
            #Perform hadamard 
            self.node.qmemory.execute_program(hadamard_program)
            yield self.await_program(self.node.qmemory)
            # print(f"IS Hadamard Apply")

            #Measure
            yield self.node.qmemory.execute_program(measurement_program)
            # meas = np.ndarray(shape=(qubit_number,1))
            meas, = measurement_program.output['m']
            # print(f"IS Measure")
            
            #Await from CSP
            yield self.await_port_input(self.node.ports[list_classic[0]])
            message = self.node.ports[list_classic[0]].rx_input().items[0]
            results = (message + meas) % 2
            # print(f"IS Published Data")
            # print(results)
            global_var.modify(results,x,1)
            x = x+1
 

                    

              

