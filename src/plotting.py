import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df1 = pd.read_csv('data_depol_n=10.csv')
df = pd.read_csv('data_depol_n=4.csv')
df2 = pd.read_csv('data_depol_n=15.csv')

# df = pd.read_csv('bps_data_n=4.csv')
# df1 = pd.read_csv('bps_data_n=10.csv')
# df2 = pd.read_csv('bps_data_n=15.csv')
# print(df)

plt.figure(figsize=(8, 6))  
# ax = df.plot(x='X', y='Y', kind='line', title='Error Probability of classical QAP')
plt.plot(df['X'], df['Y'], label=f'n=4')
plt.plot(df1['X'], df1['Y'], label=f'n=10')
plt.plot(df2['X'], df2['Y'], label=f'n=15')

plt.xlabel('Noise parameter') 
plt.ylabel('Error Probability', color = 'black') 
plt.legend()




# plt.plot(df['Distance'], df['Bps'], '-o',label=f'n=4')
# plt.plot(df1['Distance'], df1['Bps'], '-x',label=f'n=10')
# plt.plot(df2['Distance'], df2['Bps'], label=f'n=15')

# plt.xlabel('Distance (meter)') 
# plt.ylabel('Bit per sec (BPS)', color = 'black') 
# plt.legend()


# ax.set_title('4 Nodes Protocol Throughput')
# Display the plot
plt.show()



# ax1.plot(probs, data_error,'*-', color='blue',label='Qudit Protocol 8 nodes')