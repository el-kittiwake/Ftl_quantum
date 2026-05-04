"""
Exercise 00: Superposition
    "Write a program that will produce a quantum circuit with a single qubit to
    obtain this 1/√2 (|0⟩ + |1⟩) state. This demonstrates the principle of quantum
    superposition. The program should display a visual of the circuit, then run
    it on a quantum simulator with 500 shots and then display the results in a bar plot."

|0⟩ = (1 0) and |1⟩ = (0 1) but in column form. 
So the state 1/√2 (|0⟩ + |1⟩) is represented as 1/√2 (1 0) + 1/√2 (0 1) = (1/√2 1/√2) in column form.

    !!!!  If this requires a virtual environment, make sure to activate it first.
    !!!!  `python3 -m venv .venv`
    !!!!  `source .venv/bin/activate`
    !!!!  `pip install --quiet matplotlib cirq`
"""

# ============================================================================
# ------------------------------ IMPORT DEPENDENCIES ---------------------------
# ============================================================================

# Allows the script to be run without cirq being installed, and will install it if needed.
# Allows running of shell commands
import subprocess
# Allows access to system-specific parameters and functions
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("installing matplotlib...")
    # Runs the `python3 -m pip install --quiet matplotlib` command to install matplotlib
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "matplotlib"])
    import matplotlib.pyplot as plt
    print("installed matplotlib.")

try:
    import cirq
except ImportError:
    print("installing cirq...")
    # Runs the `python3 -m pip install --quiet cirq` command to install cirq
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "cirq"])
    import cirq
    print("installed cirq.")

# ============================================================================
# -------------------------- EXERCISE 00 CODE STARTS HERE --------------------
# ============================================================================

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

# Create a subplot axes and let cirq draw the histogram (counts) onto it
ax = plt.subplot()
cirq.plot_state_histogram(result, ax)
ax.set_ylabel('Probability')
for bar in ax.patches:
    # Rescale each bar from raw count to probability (count / total shots)
    bar.set_height(bar.get_height() / reps)
    # Place the probability value as text centred above the bar, display 3 decimal places
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.3f}',
            ha='center', va='bottom')
# Set y-axis ceiling to 0.1 above the tallest bar so labels aren't clipped
ax.set_ylim(0, max(bar.get_height() for bar in ax.patches) + 0.1)
plt.show()
