#!/usr/bin/env python
# coding: utf-8

# In[65]:


# useful additional packages 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import time
from pprint import pprint

# importing Qiskit
from qiskit import Aer, IBMQ
from qiskit.providers.ibmq import least_busy 
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.tools.visualization import plot_histogram


# In[72]:


"Choice of the backend"
# using local qasm simulator
backend = Aer.get_backend('qasm_simulator')  

# using IBMQ qasm simulator 
# backend = IBMQ.get_backend('ibmq_qasm_simulator')
# using real device
# backend = least_busy(IBMQ.backends(simulator=False))

flag_qx2 = True
if backend.name() == 'ibmqx4':
        flag_qx2 = False
        
print("Your choice for the backend is: ", backend, "flag_qx2 is: ", flag_qx2)


# In[73]:


# Here, two useful routine
# Define a F_gate
def G_gate(circ, p, q , i, j) :
    theta = np.arctan(np.sqrt(p/(1-p)))
    circ.ry(theta,q[j])       
    circ.cx(q[i],q[j])
    circ.ry(-theta,q[j])
    #circ.cx(q[i],q[j])
    circ.barrier(q[i])
# Define the cxrv gate which uses reverse CNOT instead of CNOT
def  cxrv(circ,q,i,j) :
    circ.h(q[i])
    circ.h(q[j])
    circ.cx(q[j],q[i])
    circ.h(q[i])
    circ.h(q[j])
    circ.barrier(q[i],q[j])


# In[78]:


# 3-qubit W state
n = 8
q = QuantumRegister(n) 
c = ClassicalRegister(n)

W_states = QuantumCircuit(q,c) 

W_states.x(q[n-1]) #start is |100>


# In[79]:


for i in range(1,n) : 
    p=1/(n+1-i)
    print(n-i, n-i-1, p)
    print(p/(1-p))
    print(np.arctan(np.sqrt(p/(1-p)))*180/3.14)
    G_gate(W_states, p, q, n-i, n-i-1)
    W_states.cx(q[n-i-1], q[n-i])


# In[80]:


for i in range(n) :
    W_states.measure(q[i] , c[i]) 

shots = 10000
time_exp = time.strftime('%d/%m/%Y %H:%M:%S')
print('start W state 3-qubit on', backend, "N=", shots,time_exp)
result = execute(W_states, backend=backend, shots=shots)
time_exp = time.strftime('%d/%m/%Y %H:%M:%S')
print('end   W state 3-qubit on', backend, "N=", shots,time_exp)
W_states.draw(output="mpl")
plot_histogram(result.result().get_counts(W_states))


# In[81]:





# In[ ]:




