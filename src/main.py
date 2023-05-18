import netsquid as ns
import numpy as np
import argparse
import numpy as np
import global_var
import pandas as pd
import matplotlib.pyplot as plt

from netsquid.nodes import Node
from netsquid.nodes import Network
from netsquid.protocols import LocalProtocol


from processor import create_processor
from connections import ClassicalBiConnection,QuantumConnection
from protocol import CSP,Users,IS


from tqdm import tqdm
from time import sleep
import csv  




def setup_protocol(network,nodes_num,list_length):
    
    # print("=====================Setup Protocol=====================")
    
    protocol = LocalProtocol(nodes=network.nodes)
    nodes = []
    i = 1
    # print("Get all nodes from network")
    while i<=(nodes_num):
        nodes.append(network.get_node("P"+str(i)))
        i = i+1
    # print(nodes)

    
    subprotocol = CSP(node=nodes[0],name=f"CSP{nodes[0].name}",num_nodes=nodes_num,list_length=list_length)
    # print(f"Add protocol {subprotocol.name} to node : { nodes[0].name}")
    protocol.add_subprotocol(subprotocol)
    

    i=1
    while i<= (nodes_num-2):
        subprotocol = Users(node=nodes[i], name=f"Node{nodes[i].name}",num_nodes=nodes_num,list_length=list_length,sr=2)
        protocol.add_subprotocol(subprotocol)
        # print(f"Add protocol {subprotocol.name} to node : { nodes[i].name}")
        i = i+1
    
    subprotocol = IS(node=nodes[nodes_num-1],name=f"IS{nodes[nodes_num-1].name}",num_nodes=nodes_num,list_length=list_length)
    protocol.add_subprotocol(subprotocol)
    # print(f"Add protocol {subprotocol.name} to node : { nodes[nodes_num-1].name}")
    # print("=====================End Setup Protocol=====================")
    return protocol



def network_setup(num_nodes,prob,node_distance=4e-3):
    # print("=====================Network Setup=====================")
    nodes =[]
    # print("Create Processors Nodes")
    i = 1
    while i<=(num_nodes):
        # print(f"Create node {i}")
        nodes.append(Node(name = f"P{i}",qmemory = create_processor(num_nodes,prob)))
        i= i+1
    
    # Create a network
    network = Network("QAP Network")
    network.add_nodes(nodes)
    # print(network)
    # print(nodes)
    # print("Nodes completed")
    
    # print("Create classical connections")
    i = 1
    while i< (num_nodes):
        node = nodes[0]
        node_next = nodes[i]
        j = 1
        c_conn = ClassicalBiConnection(name =f"c_conn{1}{1+i}", length = node_distance)
        network.add_connection(node,node_next, connection= c_conn, label="classical", 
        port_name_node1 = f"cio_node_port{1}{i+1}", port_name_node2 = f"cio_node_port{1+i}{1}")
        # print(f"Connecting {node.name} and {node_next.name}")
        i = i+1
    # print("Classical Conn Completed")


    # print("Create quantum connections")
    i =1
    while i<(num_nodes):
#         print(i)
        node = nodes[0]
        node_next = nodes[i]
#         q_conn = QuantumConnection(name=f"qconn_{i}{i+1}", length=node_distance,prob=prob)
        q_conn = QuantumConnection(name=f"qconn_{i}{i+1}", length=node_distance,prob=prob)
        network.add_connection(node, node_next, connection=q_conn, label="quantum", port_name_node1 = f"qo_node_port{1}{i+1}", port_name_node2=f"qin_node_port{i+1}{1}")
        # print(f"Connecting {node.name} and {node_next.name}")
        i= i+1
    # print("Quantum Conn Completed")

    i = 1
    # print("Set input port for quantum memory")
    while i<(num_nodes):
        # print(f"{nodes[i].name} forward input port")
        nodes[i].ports[f"qin_node_port{i+1}{1}"].forward_input(nodes[i].qmemory.ports['qin'])
        i = i+1
    # print("=====================End Network Setup=====================")
    
    return network



def main(args):
    probs = np.linspace(0, 0.5, num=20) # error parameter probability 
    # probs = [0.1]

    nodes_num = args.node_num
    list_length = args.list_length
    average = args.num_exp
    # M = args.M
    # N = args.N
    
    # header = ['Index','Rounds','Uop','Vop','H','Meas']
    # file_name = 'QBA_' + 'node' +str(nodes_num)+'_' + 'list'+ str(list_length) + '_'+'exp'+  str(average) +'_'+ 'M'+  str(M) +'_'+ 'N'  + str(N)+'.csv' 
    # file_name = 'QBA_' + 'node' +str(nodes_num)+'_' + 'list'+ str(list_length) + '_'+'exp'+  str(average) +'.csv' 
    # data = [m,global_var.sum,Uop,Vop,H,Meas]
    # f = open('data/'+file_name, 'a', encoding='UTF8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(header)
    # f.close()

    global_var.resize(list_length)

    # round_sum = 0
    x=0
    data_error = []
    while x < len(probs):

        network = network_setup(nodes_num,probs[x],node_distance=4)
        protocol = setup_protocol(network,nodes_num,list_length)
        # print(f"Parameter lambda1: {p1}")
        # print(f"Parameter lambda2: {p2}")
        # print("===================== Simulation Starts =====================")
        
        # for m in tqdm(range(0, average), desc ="Progress:"):
        for m in range(0,average):
            # global_var.sum = 0
            ns.sim_reset()
            protocol.reset()
            stats = ns.sim_run()
            
            # print(ns.sim_time(ns.SECOND))
            # print(stats.data)
            # print(stats.summary())
            # print(global_var.data)
            
            c = 0
            i = 0
            while i < int(len(global_var.data)/2):
                a = global_var.data[i][0] ^ global_var.data[i][1]
                b = global_var.data[i+1][0] ^ global_var.data[i+1][1]
                c = c + (a or b)
                i = i+2
            # print(c)
            z = (c/list_length*2)
            print(f'noise prob: {probs[x]} error: {z}')
            data_error.append(z)
            # name = list(stats.data.keys())[5] # get the quantum operation data from dictionary
            
            # for i in range (len(stats.data[name])):
            #     if i ==0:
            #         Uop = stats.data[name][i][1] # data is in tuple form, 0 index for its name, 1 index for its value
            #     if i==1:
            #         H = stats.data[name][i][1]
            #     if i==2:
            #         Vop = stats.data[name][i][1]
            #     if i ==3:
            #         Meas = stats.data[name][i][1]
            # round_sum = round_sum + global_var.sum
            # data = [m,global_var.sum,Uop,Vop,H,Meas]
            
            
            
            # f = open('data/'+file_name, 'a', encoding='UTF8', newline='')
            # writer = csv.writer(f)
            # writer.writerow(data)
            # f.close()
            
            # sleep(1)
            
            # Uncomment for debugging purposes: 
            # print("Global list: ")
            # print(global_var.global_list)
            
            # print("Global basis: ") # Show basis value recorded by each node
            # print(global_var.global_basis)
            
            # print("Global basis sum: ") # Show basis sum recorded by each node
            # print(global_var.global_basis_sum)
            
            # print(f"Percentage of Correct List: {round(percentage_correct,3)}%")
            # error_array[x][0] = probs[x]
            # error_array[x][1] = error_sum/average
            
        x = x+1
    df = pd.DataFrame({'X': probs, 'Y': data_error})
    filename = "data_depol_n=10.csv"
    df.to_csv(filename, index=False)

    
    
    # avrg_round = round_sum/(average*list_length)
    # print(f"total round: {round_sum} average round/list: {avrg_round} probability: {1/avrg_round}")
    
    # print("Global list: ")
    # print(arr_result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--node_num', type=int,default=15,help='Number of nodes for the protocol, must be power of 2 (e.g 2,4,8,...)')
    parser.add_argument('--list_length', type=int,default=2500,help='Number of length of a list in a single experiment')
    parser.add_argument('--num_exp', type=int,default=1,help='Number of experiments to be done')
    # parser.add_argument('--M', type=int,default=50,help='Number of M cycles, in order of tenth increment')
    # parser.add_argument('--N', type=int,default=2500,help='Number of N cycles, in order of hundredth increment')
    args = parser.parse_args()
    main(args)

