"""
Bonus: Quantum Teleportation
    AKA. The ballad of Alice and Bob.

Transfers the state of one qubit (Q0) to another (Q2) without physically moving it.
Alice and Bob share a pre-entangled pair of qubits (Q1, Q2). Alice entangles the
message qubit Q0 with her half of the pair, then measures Q0 and Q1, producing two
classical bits. She sends these to Bob, who applies correction gates to Q2 based on
those bits. Q2 then holds exactly the original state of Q0.

Q0 is destroyed by measurement in the process — consistent with the no-cloning theorem.
No information travels faster than light: the classical bits must be sent conventionally.

    !!!!  If this requires a virtual environment, make sure to activate it first.
    !!!!  `python3 -m venv .venv`
    !!!!  `source .venv/bin/activate`
    !!!!  `pip install --quiet matplotlib cirq`
"""

# ============================================================================
# ------------------------------ IMPORT DEPENDENCIES -------------------------
# ============================================================================

# Allows the script to be run without cirq and matplotlib being installed, will install if needed.
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
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "cirq"])
    import cirq
    print("installed cirq.")

# ============================================================================
# -------------------------- BONUS 01 CODE STARTS HERE ----------------------
# ============================================================================

# ============================================================================
# --------------------------------- DEFINITIONS ------------------------------
# ============================================================================

# Number of shots to run
reps=500

def alice(qubits):
    """
    Entangles Q1/Q2 into a Bell state.
    Entangles Q0 with Q1.
    Measures Q0 and Q1.
    Return the circuit fragment.
    """
    circuit = cirq.Circuit()

    # Entangle Q1 controlling Q2.
    # CNOT(control, target)
    circuit.append(cirq.H(qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))

    # Entangle Q0 controlling Q1
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))

    # Apply H() to Q0
    circuit.append(cirq.H(qubits[0]))

    # Measure Q0 and Q1
    # measure(qubit0, qubit1, qubit2 ...  key for later reference in classical control)
    circuit.append(cirq.measure(qubits[0], key='m0'))
    circuit.append(cirq.measure(qubits[1], key='m1'))

    return circuit


def bob(qubits):
    """
    Applies the classically controlled X and Z corrections to Q2 based on Alice's measurement results.
    Return the circuit fragment.
    """
    circuit = cirq.Circuit()

    # Apply classical control to Bob's qubit.
    # Z if Q0 = 1 and X if Q1 = 1
    circuit.append(cirq.X(qubits[2]).with_classical_controls('m1'))
    circuit.append(cirq.Z(qubits[2]).with_classical_controls('m0'))

    return circuit


def prepare_message(qubits, state):
    """
    Applies gates to Q0 to create the state being teleported. States: |0⟩, |1⟩, |+⟩
    Return the circuit fragment.
    """
    circuit = cirq.Circuit()

    if state == '1':
        circuit.append(cirq.X(qubits[0]))
    elif state == '+':
        circuit.append(cirq.H(qubits[0]))
    
    return circuit


EXPECTED = {'0': 0.0, '1': 1.0, '+': 0.5}

def visualise(ax, idx, measured_prob, state_label):
    """
    Draw one group of two bars (expected vs measured) at position idx on ax.
    Call once per state inside the loop, then plt.show() after.

    Args:
        ax: matplotlib axes to draw on
        idx: x position of this group (0, 1, 2)
        measured_prob: measured probability of Q2 = 1
        state_label: state string ('0', '1', '+') for expected lookup
    """
    width = 0.35
    expected_prob = EXPECTED[state_label]

    ax.bar(idx - width / 2, expected_prob, width, color='blue',
           label='Expected' if idx == 0 else '')
    ax.bar(idx + width / 2, measured_prob, width, color='orange',
           label='Measured' if idx == 0 else '')

    # Label both bars with their values
    ax.text(idx - width / 2, expected_prob, f'{expected_prob:.3f}',
            ha='center', va='bottom', fontsize=8)
    ax.text(idx + width / 2, measured_prob, f'{measured_prob:.3f}',
            ha='center', va='bottom', fontsize=8)


# ============================================================================
# ----------------------------------- MAIN -----------------------------------
# ============================================================================

if __name__ == "__main__":
    # Create 3 qubits. Traditionally Alice and Bob are used to demonstrate this.
    # Q0: message
    # Q1: alice's qubit
    # Q2: bob's qubit
    qubits = cirq.LineQubit.range(3)

    _, ax = plt.subplots(figsize=(8, 5))
    ax.set_ylabel('Probability of measuring |1⟩')
    ax.set_title('Quantum Teleportation: Expected vs Measured')
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['|0⟩', '|1⟩', '|+⟩'])
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', alpha=0.6, linestyle='--')

    simulator = cirq.Simulator()

    print("\n" + "=" * 50)
    print(f"{'State':<8} {'Expected':>10} {'Measured':>10} {'Result':>10}")
    print("=" * 50)

    for idx, state in enumerate(('0', '1', '+')):
        circuit = cirq.Circuit()
        circuit += prepare_message(qubits, state)
        circuit += alice(qubits)
        circuit += bob(qubits)
        circuit.append(cirq.measure(qubits[2], key='result'))

        print(f"\nCircuit for |{state}⟩:\n", circuit)

        raw_results = simulator.run(circuit, repetitions=reps)
        count_ones = sum(int(row[0]) for row in raw_results.measurements['result'])
        measured_prob = count_ones / reps
        expected_prob = EXPECTED[state]

        status = '✓' if abs(measured_prob - expected_prob) < 0.1 else '✗'
        print(f"|{state}⟩     {expected_prob:>10.3f} {measured_prob:>10.3f} {status:>10}")

        visualise(ax, idx, measured_prob, state)

    print("=" * 50)
    ax.legend()
    plt.tight_layout()
    plt.show()
