import numpy as np
# Global variable to store experiment data for data collection or debugging purposes
# import main

# Initialize global variable
data = np.full((1,2),999, dtype='i')


# global_basis = np.full((1,1),999, dtype='i')
# global_basis_sum = np.full((1,1),999, dtype='i')
# sum = 0 # value to save round number

# Function to resize global variable
def resize(k):
    global data
    # global global_basis
    # global global_basis_sum
    data = np.resize(data,(k,2))
    # global_basis = np.resize(global_basis,(m,n))
    # global_basis_sum = np.resize(global_basis_sum,(m,n))

# Function to modify the global array value

# def modify_sum():
#     global sum
#     sum = sum+1


# def modify_sum_var(n):
#     global sum
#     sum = n
    
def modify(value,i,j):
    # print("From global_var function:")
    global data
    data[i][j] = value

