# Copied and modified from qiskit_aqua.algorithms.adaptive.qaoa.qaoa.py
# and qiskit_aqua.algorithms.adaptive.qaoa.varform.py
# =============================================================================

import logging

from qiskit_aqua.algorithms import QuantumAlgorithm
from qiskit_aqua import AquaError, PluggableType, get_pluggable_class
from qiskit_aqua.algorithms.adaptive import VQE
from qiskit_aqua.algorithms.adaptive.qaoa.varform import QAOAVarForm

logger = logging.getLogger(__name__)


class constrainedQAOA(VQE):
    """
    The Quantum Approximate Optimization Algorithm.

    See https://arxiv.org/abs/1411.4028
    """

    CONFIGURATION = {
        'name': 'QAOA.Variational',
        'description': 'Quantum Approximate Optimization Algorithm',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'qaoa_schema',
            'type': 'object',
            'properties': {
                'operator_mode': {
                    'type': 'string',
                    'default': 'matrix',
                    'oneOf': [
                        {'enum': ['matrix', 'paulis', 'grouped_paulis']}
                    ]
                },
                'p': {
                    'type': 'integer',
                    'default': 1,
                    'minimum': 1
                },
                'initial_point': {
                    'type': ['array', 'null'],
                    "items": {
                        "type": "number"
                    },
                    'default': None
                },
                'batch_mode': {
                    'type': 'boolean',
                    'default': False
                }
            },
            'additionalProperties': False
        },
        'problems': ['ising'],
        'depends': ['optimizer'],
        'defaults': {
            'optimizer': {
                'name': 'COBYLA'
            },
        }
    }

    def __init__(self, cost, optimizer, mixer, p=1, initial_state=None, operator_mode='matrix', initial_point=None,
                 batch_mode=False, aux_operators=None):
        """
        Args:
            operator (Operator): Qubit operator
            operator_mode (str): operator mode, used for eval of operator
            p (int) : the integer parameter p as specified in https://arxiv.org/abs/1411.4028
            optimizer (Optimizer) : the classical optimization algorithm.
            initial_point (numpy.ndarray) : optimizer initial point.
        """
        self.validate(locals())
        var_form = constrainedQAOAVarForm(cost, p, mixer, initial_state)
        super().__init__(cost, var_form, optimizer,
                         operator_mode=operator_mode, initial_point=initial_point)

    @classmethod
    def init_params(cls, params, algo_input):
        """
        Initialize via parameters dictionary and algorithm input instance

        Args:
            params (dict): parameters dictionary
            algo_input (EnergyInput): EnergyInput instance
        """
        if algo_input is None:
            raise AquaError("EnergyInput instance is required.")

        operator = algo_input.qubit_op

        qaoa_params = params.get(QuantumAlgorithm.SECTION_KEY_ALGORITHM)
        operator_mode = qaoa_params.get('operator_mode')
        p = qaoa_params.get('p')
        initial_point = qaoa_params.get('initial_point')
        batch_mode = qaoa_params.get('batch_mode')

        # Set up optimizer
        opt_params = params.get(QuantumAlgorithm.SECTION_KEY_OPTIMIZER)
        optimizer = get_pluggable_class(PluggableType.OPTIMIZER,
                                        opt_params['name']).init_params(opt_params)

        return cls(operator, optimizer, p=p, operator_mode=operator_mode,
                   initial_point=initial_point, batch_mode=batch_mode,
                   aux_operators=algo_input.aux_ops)

class constrainedQAOAVarForm(QAOAVarForm):
    def __init__(self, cost_operator, p, mixer_operator=None, initial_state=None):
        super().__init__(cost_operator, p, initial_state)

        if mixer_operator is None:
            v = np.zeros(self._cost_operator.num_qubits)
            ws = np.eye(self._cost_operator.num_qubits)
            self._mixer_operator = reduce(
                lambda x, y: x + y,
                [
                    Operator([[1, Pauli(v, ws[i, :])]])
                    for i in range(self._cost_operator.num_qubits)
                ]
            )
        else:
            self._mixer_operator = mixer_operator
          
    def construct_circuit(self, angles):
        if not len(angles) == self.num_parameters:
            raise ValueError('Incorrect number of angles: expecting {}, but {} given.'.format(
                self.num_parameters, len(angles)
            ))
        circuit = QuantumCircuit()
        if self._initial_state:
            circuit += self._initial_state
        if len(circuit.qregs) == 0:
            q = QuantumRegister(self._cost_operator.num_qubits, name='q')
            circuit.add_register(q)
        elif len(circuit.qregs) == 1:
            q = circuit.qregs[0]
        else:
            raise NotImplementedError
        circuit.u2(0, np.pi, q)
        for idx in range(self._p):
            beta, gamma = angles[idx], angles[idx + self._p]
            circuit += self._cost_operator.evolve(None, gamma, 'circuit', 1, quantum_registers=q)
            circuit += self._mixer_operator.evolve(None, beta, 'circuit', 1, quantum_registers=q)
        return circuit    
      
