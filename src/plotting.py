import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df1 = pd.read_csv('data_depol_n=10.csv')
df = pd.read_csv('data_depol_n=4.csv')
# print(df)

plt.figure(figsize=(8, 6))  
# ax = df.plot(x='X', y='Y', kind='line', title='Error Probability of classical QAP')
plt.plot(df['X'], df['Y'], label=f'n=4')
plt.plot(df1['X'], df1['Y'], label=f'n=10')

plt.xlabel('Noise parameter') 
plt.ylabel('Error Probability', color = 'black') 
plt.legend()


# ax.set_title('4 Nodes Protocol Throughput')
# Display the plot
plt.show()



# ax1.plot(probs, data_error,'*-', color='blue',label='Qudit Protocol 8 nodes')