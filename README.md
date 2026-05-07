# Ftl_quantum

Subject version 2

"This project is an introduction to quantum programming. It will challenge you to create different quantum programs, and run them on a real quantum computer."

I attempted to do this work mostly in Cirq, by Google. However, if I had researched better I would have realised that getting ex02 to work using the systems available is a nightmare. It took me many attempts over a couple of hours to fail and give up.

So, for the sake of completing this in a reasonable time I did ex02 in IBM Qiskit. The process for setting up an account, getting a free API key and running software was completed in less than an hour.

The evaluation sheet also gives you the code changes required as qiskit snippets. This along with differences in how cirq and qiskit work make it a bad idea to use any other framework than qiskit for these exercises.

## Usage

```bash
# Set up the virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate

# Run an exercise
make ex00
make ex01
make ex02   # requires IBM_TOKEN in a .env file
make ex03
make ex04
make bonus

# Clean the virtual environment
make clean
```

ex02 requires a `.env` file in the project root with your IBM Quantum API token:

```sh
IBM_TOKEN=your_token_here
IBM_SIMULATE=true   # false to run on real hardware
```

ex04 takes optional parameters to specify the number of qubits and one or more target states:

```bash
.venv/bin/python3 ex04/ex04.py <num_qubits> <target>
```

- `num_qubits` - number of qubits (minimum 2). The search space is 2^num_qubits states.
- `target` - bitstring of length num_qubits representing the state to search for.

```bash
# Default: 3 qubits, target = 111
make ex04

# 3 qubits, search for 101
.venv/bin/python3 ex04/ex04.py 3 101

# 4 qubits, search for 1010
.venv/bin/python3 ex04/ex04.py 4 1010
```

Note: the algorithm degrades when the number of targets is >= N/2 (where N = 2^num_qubits).

## Contents

ex00: Create a superposition of a single qubit.

ex01: Entangle a pair of qubits.

ex02: Run the entanglement circuit (ex01) on real/simulated IBM quantum hardware using Qiskit. Observe and discuss the concept of quantum noise.

ex03: Implement and test the Deutsch-Jozsa algorithm.

ex04: Implement and test the quantum search algorithm.

bonus1: Implement and test the quantum teleportation concept.

## Qiskit/Cirq adaptation

The evaluation sheet provides oracle code as Qiskit snippets. The table below maps the Qiskit gates used in the eval oracles to their Cirq equivalents.

| Qiskit | Cirq | Notes |
| --- | --- | --- |
| `circuit.h(q)` | `cirq.H(qubits[q])` | Hadamard |
| `circuit.x(q)` | `cirq.X(qubits[q])` | Pauli-X / bit flip |
| `circuit.cx(control, target)` | `cirq.CNOT(qubits[control], qubits[target])` | CNOT |
| `circuit.cz(q0, q1)` | `cirq.CZ(qubits[q0], qubits[q1])` | Controlled-Z |
| `circuit.ccx(c0, c1, target)` | `cirq.CCNOT(qubits[c0], qubits[c1], qubits[target])` | Toffoli |
| `circuit.ch(control, target)` | `cirq.H.controlled()(qubits[control], qubits[target])` | Controlled-H |
| `circuit.ry(theta, q)` | `cirq.ry(rads=theta)(qubits[q])` | Y-rotation |

Qiskit uses little-endian bit ordering (qubit 0 is the rightmost bit in a result string). Cirq uses big-endian (qubit 0 is leftmost). So a result of `"01"` in Qiskit and `"10"` in Cirq represent the same state.
