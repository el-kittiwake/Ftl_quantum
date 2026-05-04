"""
Exercise 01
    "Write a program that will produce a quantum circuit with two qubits in order
    to obtain this 1/√2 (|00⟩ + |11⟩) state. This demonstrates the principles of
    superposition and quantum entanglement. The program must display the circuit,
    then run it on a quantum simulator with 500 shots and then display the results
    in a plot_histogram."

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
# -------------------------- EXERCISE 01 CODE STARTS HERE --------------------
# ============================================================================

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
                       cirq.measure(qubit0, qubit1, key='m'))
print("Circuit:")
print(circuit)

# Simulate the above circuit 500 times.
reps = 500
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=reps)

# Expected outcomes for this Bell state are |00⟩ (index 0) and |11⟩ (index 3)
expected_indices = {0, 3}

# Create a subplot axes and let cirq draw the histogram (counts) onto it
ax = plt.subplot()
cirq.plot_state_histogram(result, ax)
ax.set_ylabel('Probability')
# Override x-axis labels with ket notation
ax.set_xticklabels(['|00⟩', '|01⟩', '|10⟩', '|11⟩'])
for i, bar in enumerate(ax.patches):
    # Rescale each bar from raw count to probability (count / total shots)
    bar.set_height(bar.get_height() / reps)
    # Blue for expected Bell state outcomes (|00⟩, |11⟩), red for unexpected
    bar.set_color('blue' if i in expected_indices else 'red')
    # Place the probability value as text centred above the bar, display 3 decimal places
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.3f}',
            ha='center', va='bottom')
# Set y-axis ceiling to 0.1 above the tallest bar so labels aren't clipped
ax.set_ylim(0, max(bar.get_height() for bar in ax.patches) + 0.1)
plt.show()
