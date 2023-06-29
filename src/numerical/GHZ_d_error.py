# from sympy import zeros
import numpy as np
from numpy.linalg import matrix_power
from scipy.linalg import dft
import pandas as pd
d = 2
n = 3

def Dagger(x):
    return np.conjugate(x.T)

def operate(O,rho):
    O_conj = Dagger(O)
    temp = np.matmul(O,rho)
    return np.matmul(temp,O_conj)


basis_mat = np.eye(d)
X = np.zeros((d,d)).astype('complex128')
for i in range (d):
#     print(i)
    X += basis_mat[:,i].reshape(-1,1)*Dagger(basis_mat[:,(i+1)%d])
    
    
    
basis_mat = np.eye(d)
w = np.exp(2j * np.pi / d)
Z = np.zeros((d,d)).astype('complex128')
for i in range (d):
#     print(i)
    Z += w**i * (basis_mat[:,i].reshape(-1,1)*Dagger(basis_mat[:,i]))



def depol_d(rho,d,p):
    out_dens1 = np.zeros((d,d)).astype('complex128')
    for i in range (d):
        for j in range (d):
#             print(i,j)
            temp = operate(matrix_power(X,i),rho)
            temp = operate(matrix_power(Z,j),temp)
            out_dens1 += temp
        
    out_dens1 = (p/(d**2)) * out_dens1
    # out_dens1 = re(out_dens1) + I*(im(out_dens1))
    
    out_dens2 = (1-p) * rho 
    
    return(out_dens1 + out_dens2)

    
def Noisy_GHZ_state(d,n,p):
    I = np.eye(d)
    basis_mat = []
    for i in range (d):
        for j in range (d):
            temp_mat = I[:,i].reshape(-1,1)*Dagger(I[:,j])
#             print('Before noise')
#             print(type(temp_mat))
            temp_mat = depol_d(temp_mat,d,p)
#             print('After Noise')
#             print(type(temp_mat))
            basis_mat.append(temp_mat)
    if (n>1):
        for k in range(d**2):
#             print(type(basis_mat[k]))
            temp_mat1 = np.kron(basis_mat[k],basis_mat[k])
#             print(type(temp_mat1))
            if (n==2):
                basis_mat[k] = temp_mat1
            else:
                for l in range (n-2):
                    temp_mat1 = np.kron(temp_mat1,basis_mat[k])
                    basis_mat[k] = temp_mat1
    return (basis_mat)

mdft = dft(d)
mdft = 1/(np.sqrt(d)) * mdft
# d = 3
fourier_ket = []
for i in range(d):
    fourier_ket.append(mdft[:,i])
basis_f = [i.reshape(-1,1)*Dagger(i) for i in fourier_ket]
# print(basis_f[0])


# n=2
# basis_digits = []

def convert_int_m_ary(n,m,d):
    m_ary = []
    a,b = divmod(n,m)
    m_ary.append(b)
    while a != 0:
        n = a
        a,b = divmod(n,m)
        m_ary.append(b)
    if len(m_ary) < d:
        range_ = d - len(m_ary)
        for i in range(range_):
            m_ary.append(0)
    m_ary.reverse()
    return m_ary
# a = convert_int_m_ary(13,3)


range_ = d**n
meas_list = []
for i in range(range_):
    list_m = convert_int_m_ary(i,d,n)
#     print(list_m)
    if n==1:
        meas_list = basis_f
    elif n==2:
        meas_list.append(np.kron(basis_f[list_m[0]],basis_f[list_m[1]]))
    else:
        temp = np.kron(basis_f[list_m[0]],basis_f[list_m[1]])
        for j in range(n-2):
            temp = np.kron(temp,basis_f[list_m[j+2]])
        meas_list.append(temp)
# print(meas_list[0])

list_prob = np.linspace(0,1,10)
# list_prob = [0.5]
list_error = []
for i in range(len(list_prob)):
    print(f"Prob: {list_prob[i]} ")
    q_state = Noisy_GHZ_state(d,n,list_prob[i])
    sum_ = q_state[0]
    for j in range(len(q_state)-1):
        sum_ += q_state[j+1]
    output_state = (1/d)*sum_
    # print(output_state)
    prob_correct = 0
    for k in range(range_):
#         print(bin(j))
        list_mary = convert_int_m_ary(k,d,n)
        prob = np.matmul(meas_list[k],output_state)
        prob = abs(np.trace(prob).real)
        print(f'{list_mary}, {prob}')
        # prob = np.round(prob,5)
        if sum(list_mary) % d == 0:
            prob_correct += prob
    prob_error = 1 - prob_correct
    list_error.append(prob_error)
        


    

df = pd.DataFrame({'X': list_prob, 'Y': list_error})
print(df)
filename = f"error_d={d}_n={n}.csv"
df.to_csv(filename, index=False)
