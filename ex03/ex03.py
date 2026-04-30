"""
Exercise 03: Deutsch-Jozsa Algorithm
You have to recreate the Deutsch-Jozsa algorithm, it should work with a total number of 3 qubits.
When applying your algorithm, your circuit should be able to determine whether the
Oracle is Constant or Balanced, based on the measurement of your Qubits.
• Your Qubits must be 1 if the Oracle is Balanced.
• Your Qubits must be 0 if the Oracle is Constant.

https://en.wikipedia.org/wiki/Deutsch%E2%80%93Jozsa_algorithm

If this requires a virtual environment, make sure to activate it first.
`source .venv/bin/activate`

Apparently Python desires snake_case for variable and function names,
so I'll reluctantly follow that convention here.

Just learned about docstrings, now the time is ripe to overdo them!
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
    from matplotlib.ticker import FuncFormatter
except ImportError:
    print("installing matplotlib...")
    # Runs the `python3 -m pip install --quiet matplotlib` command to install matplotlib
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "matplotlib"])
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    print("installed matplotlib.")

try:
    import cirq
except ImportError:
    print("installing cirq...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "cirq"])
    import cirq
    print("installed cirq.")

# =============================================================================
# -------------------------- EXERCISE 03 CODE STARTS HERE ----------------------
# =============================================================================

# ============================================================================
# --------------------------------- DECLARATIONS -------------------------------
# ============================================================================

simulator = cirq.Simulator()
CONSTANT_THRESHOLD = 0.9
BALANCED_THRESHOLD = 0.1

# ============================================================================
# --------------------------------- DEFINITIONS --------------------------------
# ============================================================================

def oracle_func(input_qubits, output_qubit, constant=False):
    """
    Oracles.
    I think this is what will be changed to test different constant and balanced functions.
    Initially:
        The constant oracle does nothing, leaving the output qubit unchanged.
        The balanced oracle applies CNOT gates from each input qubit to the output qubit.
        
    Args:
        input_qubits: List of input qubits
        output_qubit: Auxiliary/output qubit
        constant: If True, create constant oracle; else balanced oracle 
    """
    if constant:
        # Oracle for a constant function
        return cirq.Circuit()
    else:
        # Oracle for a balanced function
        return cirq.Circuit(cirq.CNOT(q, output_qubit) for q in input_qubits)

def run_test(oracle_func, expected_constant, reps=500):
    """
    Runs the test with the given oracle function and expected type
    Builds the circuit, simulates it, and calculates the probability of measuring |000⟩.
    Prints whether the results match the expected outcome based on the oracle type.
    
    Args:
        oracle_func: The oracle function to test
        expected_constant: Whether we expect a constant oracle
        reps: Number of circuit repetitions (default: 500)
    """
    circuit = cirq.Circuit()
    circuit.append(initial_gates)
    circuit.append(output_gates)
    circuit.append(oracle_func(input_qubits, output_qubit, constant=expected_constant))
    circuit.append(final_gates)
    circuit.append(measure_gates)

    print(f"\nTesting {'CONSTANT' if expected_constant else 'BALANCED'} Oracle:")
    print(circuit)

    result = simulator.run(circuit, repetitions=reps)
    results = result.measurements['result']
    states = [''.join(map(str, measurement)) for measurement in results]
    all_zeros = states.count('000')
    prob_zeros = all_zeros / reps

    print(f"Measured |000⟩: {all_zeros}/{reps} ({prob_zeros:.2%})")
    if expected_constant:
        print(f"Conclusion: {'✓ CONSTANT' if prob_zeros > CONSTANT_THRESHOLD else '✗ INCORRECT'}")
    else:
        print(f"Measured other states: {reps - all_zeros}/{reps} ({1 - prob_zeros:.2%})")
        print(f"Conclusion: {'✓ BALANCED' if prob_zeros < BALANCED_THRESHOLD else '✗ INCORRECT'}")

    return prob_zeros

def plotResults(probZeros, expected_constant):
    """
    Plots the results for either the constant or balanced oracle.
    Shows the probability of measuring |000⟩ vs other states
    
    Args:
        probZeros: Probability of measuring |000⟩
        expected_constant: If True, plot constant oracle results
    """
    # Define configuration based on oracle type
    config = {
        True: {
            'subplot': 1,
            'title': 'Constant Oracle Results',
            'color': ['blue', 'lightblue'],
            'labels': ['|000⟩\n(Expected)', 'Other States']
        },
        False: {
            'subplot': 2,
            'title': 'Balanced Oracle Results',
            'color': ['red', 'lightcoral'],
            'labels': ['|000⟩\n(Unexpected)', 'Other States\n(Expected)']
        }
    }
    cfg = config[expected_constant]
    
    plt.subplot(1, 2, cfg['subplot'])
    x_positions = [0, 0.5]
    plt.bar(x_positions, [probZeros, 1 - probZeros], color=cfg['color'], width=0.4)
    plt.ylabel('Probability')
    plt.title(cfg['title'])
    plt.xticks(x_positions, cfg['labels'])
    plt.xlim([-0.3, 0.8])
    plt.ylim([0, 1.1])
    plt.grid(axis='y', alpha=0.6, linestyle='--')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2f}'.format(y)))

# ============================================================================
# ----------------------------------- SETUP ------------------------------------
# ============================================================================

# Create 3 input qubits at row 0, columns 0-2 of a grid.
# Could probably use LineQubit, but grid seems more intuitive.
input_qubits = [cirq.GridQubit(0, i) for i in range(3)]
# Create 1 output qubit at row 1, column 0 of the grid.
# This qubit will not be measured, but is required for the algorithm. (CNOT)
output_qubit = cirq.GridQubit(1, 0)

# Define initial gates: Put input qubits into superposition
# This creates all possible input combinations in superposition
initial_gates = [cirq.H(q) for q in input_qubits]

# Define output qubit preparation: |1⟩ state in superposition (1/√2(|0⟩ - |1⟩))
# This is needed for the phase kickback to work
output_gates = [cirq.X(output_qubit), cirq.H(output_qubit)]

# Define final gates: Apply Hadamard again to input qubits
# This is where quantum interference happens - distinguishes constant from balanced
final_gates = [cirq.H(q) for q in input_qubits]

# Define measurement
measure_gates = cirq.measure(*input_qubits, key='result')

# ============================================================================
# TEST 1: Circuit with CONSTANT ORACLE
# ============================================================================
print("\n" + "="*60)
print("TESTING CONSTANT ORACLE")
print("="*60)

prob_zeros_const = run_test(oracle_func, expected_constant=True)

# ============================================================================
# TEST 2: Circuit with BALANCED ORACLE
# ============================================================================
print("\n" + "="*60)
print("TESTING BALANCED ORACLE")
print("="*60)

prob_zeros_bal = run_test(oracle_func, expected_constant=False)

# ============================================================================
# VISUALIZATION: Compare both oracles
# ============================================================================
plt.figure(figsize=(14, 6))
plt.suptitle('Deutsch-Jozsa Algorithm: Oracle Classification', fontsize=14)
plotResults(prob_zeros_const, expected_constant=True)
plotResults(prob_zeros_bal, expected_constant=False)
plt.tight_layout()
plt.show()
