import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df1 = pd.read_csv('data_depol_n=10.csv')
df = pd.read_csv('data_depol_n=10_nocombined_100.csv')
# df = pd.read_csv('data_depol_n=4.csv')
df2 = pd.read_csv('data_depol_n=15.csv')

# df = pd.read_csv('bps_data_n=5.csv')
# df1 = pd.read_csv('bps_data_n=10.csv')
# df2 = pd.read_csv('bps_data_n=15.csv')
# print(df)

plt.figure(figsize=(8, 6))  
# ax = df.plot(x='X', y='Y', kind='line', title='Error Probability of classical QAP')
plt.plot(df['X'], df['Y'], label=f'n=15')
# plt.plot(df1['X'], df1['Y'], label=f'n=10')
# plt.plot(df2['X'], df2['Y'], label=f'n=15')
plt.yscale('log')

def error_prob(n,p):
    # return pow(2,n-1) * (pow((p/4 + (1-p/2)/2),n) - pow(((1-p)/2),n))
    return 0.5 - pow((1-p) , n)/2

# prob = error_prob(10,1)  
prob_data = np.linspace(0,1,100)  
data = []
for i in range(100):
    data.append(error_prob(10,prob_data[i]))
# print(prob)
plt.plot(prob_data, data, label=f'theory')
ymax, ymin = plt.ylim()
# print(ymin)
# print(ymax)
plt.xlabel('Noise parameter') 
plt.ylabel('Error Probability', color = 'black') 
plt.legend()

dict = {'prob': prob_data, 'error': data}  
       
df = pd.DataFrame(dict) 
    
# saving the dataframe 
df.to_csv('data_depol_n=10_theory.csv') 



# plt.plot(df['Distance'], df['Bps'], '-o',label=f'n=5')
# plt.plot(df1['Distance'], df1['Bps'], '-x',label=f'n=10')
# plt.plot(df2['Distance'], df2['Bps'], label=f'n=15')

# plt.xlabel('Distance (meter)') 
# plt.ylabel('Bit per sec (BPS)', color = 'black') 
# plt.legend()


# ax.set_title('4 Nodes Protocol Throughput')
# Display the plot
plt.show()



# ax1.plot(probs, data_error,'*-', color='blue',label='Qudit Protocol 8 nodes')