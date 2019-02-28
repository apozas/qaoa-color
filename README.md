# qaoa-color
Qiskit camp 2019 hackathon: Using QAOA for solving the graph coloring problem

Important files:
- [constrainedqaoa.py](https://github.com/apozas/qaoa-color/blob/master/constrainedqaoa.py): modified QAOA class that allows for setting an arbitrary mixer Hamiltonian
- [arbitrary_mixer_example.ipynb](https://github.com/apozas/qaoa-color/blob/master/arbitrary_mixer_example.ipynb): Example of use of the new class constrainedQAOA
- [state_preparation_and_qaoa.ipynb](https://github.com/apozas/qaoa-color/blob/master/state_preparation_and_qaoa.ipynb): Graph coloring for constrained QAOAs
- [original_mixer_log_qubits.ipynb](https://github.com/apozas/qaoa-color/blob/master/original_mixer_log_qubits.ipynb): Same calculations, but with the original mixer Hamiltonian, allowing a reduction in the number of qubits at the cost of lower precision
- [results](https://github.com/apozas/qaoa-color/tree/master/results): colorings using constrainedQAOAs
- [visualize_binary.ipynb](https://github.com/apozas/qaoa-color/blob/master/visualize_binary.ipynb): visualizations of colorings for binary encodings and original mixers
