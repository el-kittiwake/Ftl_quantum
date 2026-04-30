# Exercise 01
# Write a program that will produce a quantum circuit with two qubits in order to obtain
# this 1/√2 (|00⟩ + |11⟩) state using the principle of superposition and quantum entanglement.
# The program must display the circuit, then run it on a quantum simulator with 500
# shots and then display the results in a plot_histogram.

# If this requires a virtual environment, make sure to activate it first.
# source venv/bin/activate

# Allows the script to be run without cirq being installed, and will install it if needed.
# Allows running of shell commands
import subprocess
# Allows access to system-specific parameters and functions
import sys

# For plotting the results
import matplotlib.pyplot as plt
# Needed to format the y-axis of the plot to show probabilities with two decimal places
from matplotlib.ticker import FuncFormatter

try:
    import cirq
except ImportError:
    print("installing cirq...")
    # Runs the `python3 -m pip install --quiet cirq` command to install cirq
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "cirq"])
    import cirq
    print("installed cirq.")

# Create two qubits at row 0, columns 0 and 1 of a grid.
# Position doesn't actually matter, but horizontally adjacent is easier to read.
qubit0 = cirq.GridQubit(0, 0)
qubit1 = cirq.GridQubit(0, 1)

 # Create a circuit that produces the entangled Bell state 1/√2 (|00⟩ + |11⟩) AKA: |Φ+⟩.
# 1. Apply Hadamard gate (X**0.5) to qubit0 to create superposition
# 2. Apply CNOT gate with qubit0 as control to entangle the two qubits
# 3. Measure both qubits - results should show only |00⟩ or |11⟩ outcomes
# https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_gate
# https://en.wikipedia.org/wiki/Bell_state
circuit = cirq.Circuit(cirq.X(qubit0) ** 0.5, cirq.CNOT(qubit0, qubit1),
                       cirq.measure(qubit0, key='m0'), cirq.measure(qubit1, key='m1'))
print("Circuit:")
print(circuit)

# Simulate the above circuit 500 times.
reps = 500
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=reps)

# Calculate probabilities of all possible 2-qubit states.
# Extract each qubit's results, flatten to 1D array
m0_results = result.measurements['m0'].flatten()
m1_results = result.measurements['m1'].flatten()
# Join each result pair into the combined state.
# Zip pairs m0 and m1 values, convert to strings, and join into state strings ('00', '01', '10', '11')
states = [''.join(map(str, [m0, m1])) for m0, m1 in zip(m0_results, m1_results)]
prob_00 = states.count('00') / reps
prob_01 = states.count('01') / reps
prob_10 = states.count('10') / reps
prob_11 = states.count('11') / reps

# Calculate max probability with padding
maxProb = max(prob_00, prob_01, prob_10, prob_11) + 0.1
# Create a plot showing all four states to demonstrate entanglement correlation
# This is still a pain
plt.figure(figsize=(10, 8))
x_positions = [0, 0.5, 1.0, 1.5]
probabilities = [prob_00, prob_01, prob_10, prob_11]
plt.bar(x_positions, probabilities, color=['blue', 'red', 'red', 'blue'], width=0.4)
plt.ylabel('Probabilities')
# x tick location and labels
plt.xticks(x_positions, ['|00⟩', '|01⟩', '|10⟩', '|11⟩'])
# x limits, add padding to either side
plt.xlim([-0.3, 1.8])
plt.ylim([0, maxProb])
# Grid lines, on y, 60% opaque, dashed style
plt.grid(axis='y', alpha=0.6, linestyle='--')
# gca () get current axes, yaxis set major formatter to a lambda function that formats the y values to two decimal places
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2f}'.format(y)))
plt.show()
