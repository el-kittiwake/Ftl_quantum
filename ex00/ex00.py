# Exercise 00
# Write a program that will produce a quantum circuit with a single qubit to obtain this
# 1/√2 (|0⟩ + |1⟩) state using the principle of quantum superposition.
# The program should display a visual of the circuit, then run it on a quantum simulator
# with 500 shots and then display the results in a plot_histogram

# |0⟩ = (1 0) and |1⟩ = (0 1) but in column form. 
# So the state 1/√2 (|0⟩ + |1⟩) is represented as 1/√2 (1 0) + 1/√2 (0 1) = (1/√2 1/√2) in column form.

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

# Create a single qubit at row 0, column 0 of a grid.
qubit = cirq.GridQubit(0, 0)

# Create a circuit that applies a square root of NOT gate, then measures the qubit.
# This is the same as a Hadamard gate, which creates a superposition of the two possible outcomes.
# https://en.wikipedia.org/wiki/Quantum_logic_gate#Hadamard_gate
# https://en.wikipedia.org/wiki/Schr%C3%B6dinger%27s_cat
circuit = cirq.Circuit(cirq.X(qubit) ** 0.5, cirq.measure(qubit, key='m'))
print("Circuit:")
print(circuit)

# Simulate the above circuit 500 times.
reps = 500
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=reps)

# Calculate probabilities of measuring 1s and 0s.
resStr = str(result)
ones = resStr.count('1')
zeros = resStr.count('0')
probOnes = ones / reps
probZeros = zeros / reps

# Create a plot of the probabilities
# This is a pain
plt.figure(figsize=(10, 8))
plt.bar([0, 0.5], [probZeros, probOnes], color=['blue', 'blue'], width=0.4)
plt.ylabel('Probabilities')
# x tick location and labels
plt.xticks([0, 0.5], ['0', '1'])
# x limits, addes padding to either side
plt.xlim([-0.3, 0.8])
# max probability, add 0.1 for padding
maxProb = max(probZeros, probOnes) + 0.1
plt.ylim([0, maxProb])
# Grid lines, on y, 60% opaque, dashed style
plt.grid(axis='y', alpha=0.6, linestyle='--')
# gca () get current axes, yaxis set major formatter to a lambda function that formats the y values to two decimal places
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2f}'.format(y)))
plt.show()
