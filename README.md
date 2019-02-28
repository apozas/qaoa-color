# qaoa-color
Qiskit camp 2019 hackathon: Using QAOA for solving the graph coloring problem

Important files:
- constrainedqaoa.py: modified QAOA class that allows for setting an arbitrary mixer Hamiltonian
- arbitrary_mixer_example.ipynb: Example of use of the new class constrainedQAOA
- state_preparation_and_qaoa.ipynb: Graph coloring for constrained QAOAs
- original_mixer_log_qubits.ipynb: Same calculations, but with the original mixer Hamiltonian, allowing a reduction in the number of qubits at the cost of lower precision
- results: colorings using constrainedQAOAs
- visualize_binary.ipynb: visualizations of colorings for binary encodings and original mixers
