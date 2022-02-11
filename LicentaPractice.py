#!/usr/bin/env python
# coding: utf-8

# In[11]:


from qiskit import Aer, QuantumCircuit
import matplotlib.pyplot as plt
import pandas as pd
import math
from statsmodels.stats.weightstats import ztest as ztest

get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = [10, 5]


# In[2]:


qc = QuantumCircuit(8)
qc.h(range(8))
qc.measure_all()
qc.draw(output='mpl')


# In[3]:


sim = Aer.get_backend('aer_simulator')
result = sim.run(qc, shots=100000).result()
counts = result.get_counts()
counts


# In[4]:


plt.bar([int(x, 2) for x in counts.keys()], counts.values(), width=1)
plt.show()


# In[5]:


#from qiskit.circuit.library import UniformDistribution
from qiskit_finance.circuit.library import UniformDistribution
qc2 = UniformDistribution(8)
qc2.measure_all()
result2 = sim.run(qc2.decompose(), shots=100000, memory=True).result()
counts2 = result2.get_counts()
plt.bar([int(x, 2) for x in counts2.keys()], counts2.values(), width=1)
plt.show()


# In[6]:


#df1_data = {"number": [numere], "counts": [counts]}
df1_data = {"number": [int(x, 2) for x in counts.keys()], "counts": [x for x in counts.values()]}
df1 = pd.DataFrame.from_dict(df1_data)
df2_data = {"number": [int(x, 2) for x in counts2.keys()], "counts": [x for x in counts2.values()]}
df2 = pd.DataFrame.from_dict(df2_data)
plt.bar(df1['number'], df1['counts'], width=1)
plt.show()
plt.bar(df2['number'], df2['counts'], width=1)
plt.show()


# In[7]:


# asta normal ca nu merge, sunt distributii uniforme, pana la urma - ar merge daca as normaliza count-urile sau ceva
z_table = 1 - 0.9675 # sau -1.96, e two-tailed
#z_calc = (df1['counts'].mean() - df2['counts'].mean()) / (math.sqrt(df1.var()['counts'] / len(df1['counts']) + df2.var()['counts']/ len(df2['counts'])))
df1['mult'] = df1['number'] * df1['counts']
df2['mult'] = df2['number'] * df2['counts']
z_calc = (df1['mult'].mean() - df2['mult'].mean()) / (math.sqrt(df1.var()['mult'] / len(df1['mult']) + df2.var()['mult']/ len(df2['mult'])))
df1


# In[13]:


# si asa s-ar face cu metoda gata implementata, daca ar fi distributie normala
ztest(df1['mult'], df2['mult'], value=0)


# In[ ]:




