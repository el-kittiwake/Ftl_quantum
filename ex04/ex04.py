"""
Exercise 04: Search algorithm
    The search algorithm, the ultimate goal of this project.
    Your algorithm should search for one or more items that meet a given requirement among
    N unclassified items.
        • On a traditional computer, the complexity of the problem is O(N).
        • On a quantum computer, the complexity is reduced to O(√(N)).
    You will need to have 3 distinct parts:
        • The initialization of states.
        • The Oracle.
        • Diffuser.
    Your algorithm will take a Y number of qubits (minimum 2) and must not require
    any modification to work.
    Similar to the Deutsch-Jozsa algorithm, several Oracles will be provided during the
    evaluation to verify that your algorithm is working properly.

Classical computing could get away with checking once. However to guarantee
finding the target it would have to check every member of N.

Quantum computing rotates the probability distribution toward the target state by
a fixed angle each iteration, requiring only √N rotations to guarantee finding it.
It does this by using superposition to allow for consideration of all states
at the same time. The oracle is designed to steer the search towards the correct
target, so marks the desired state for the diffuser to act on. The diffuser
repeatedly amplifies the probability of the target.

!! If this requires a virtual environment, make sure to activate it first.    !!
!! `source .venv/bin/activate`                                                !!
"""

# ============================================================================
# ------------------------------ IMPORT DEPENDENCIES -------------------------
# ============================================================================

# Allows the script to be run without cirq and matplotlib being installed, will install if needed.
# Allows running of shell commands
import subprocess
# Allows access to system-specific parameters and functions
import sys
# Allows access to maths functions
import math as maths

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
# -------------------------- EXERCISE 04 CODE STARTS HERE --------------------
# ============================================================================

# ============================================================================
# --------------------------------- DEFINITIONS ------------------------------
# ============================================================================

# --------------------------------- RUN FUNCTION -----------------------------
def run_simulation(num_qubits, target_scheme, reps=500):
    """
    Run the quantum search algorithm:
        Initialise the system with a uniform superposition over all states (H gate)
        Perform the following a calculated number of times:
            Apply the desired oracle
            Apply the diffuser
        Measure the resulting quantum state
        Visualise the results as a probability bar chart (subject copy)

    This algorithm is also known as Grover's algorithm.

    Args:
        num_qubits: Number of qubits to use (minimum 2). Search space is 2^num_qubits states.
        target_scheme: List of bitstrings representing the states to search for (e.g. ["101", "011"]).
        reps: Number of times to run the circuit for measurement statistics.
    """

    # Number of iterations
    # Generally (π/4) * √N -  where N = 2^num_qubits
    # However as we are allowing multiple target strings we need to take those into account.
    # This may not be needed, but I don't know how the evaluation will implement the testing.
    N = 2 ** num_qubits
    k = len(target_scheme)
    # Tried round() here first, but led to incorrect results for 2 qubits
    iterations = max(1, maths.floor((maths.pi / 4) * maths.sqrt(N / k)))

    ## Initialisation of states!
    # Similar to Deutsch-Jozsa in a lot of the setup.
    # Create Y number of input qubits using a LineQubit() range
    qubits = cirq.LineQubit.range(num_qubits)
    
    # Create an empty circuit which will be added to later.
    circuit = cirq.Circuit()
    
    # Initial H gate - superposition
    circuit.append(cirq.H.on_each(*qubits))
    
    # Create oracle and diffuser
    for _ in range(iterations):
        circuit.append(build_oracle(qubits, target_scheme))
        circuit.append(build_diffuser(qubits))

    # Add measurements to all qubits in circuit
    circuit.append(cirq.measure(*qubits, key="results"))
    print("Circuit:\n", circuit)

    # Run the simulation. Using the subject required 500 reps.
    simulator = cirq.Simulator()
    raw_results = simulator.run(circuit, repetitions=reps)
    result_measurements = raw_results.measurements["results"]

    # Visualise the results
    # This never stopped being a pain
    # Creates an array of all combinations of 01 bitstrings that fit within num_qubits
    all_states = [format(i, f"0{num_qubits}b") for i in range(2 ** num_qubits)]
    # Creates a counter for each state and defaults it to 0
    counts = {state: 0 for state in all_states}
    # Count all states and fill totals
    for row in result_measurements:
        counts["".join(str(b) for b in row)] += 1
    
    # Calculate probability (count / reps) of states and maximum probability
    probabilities = [counts[s] / reps for s in all_states]
    max_prob = max(probabilities)

    # Plot results as a bar chart
    # figsize in inches (remnant of MATLAB days), scaled to number of qubits
    # Still awkward, but better than fixed size.
    _, ax = plt.subplots(figsize=(max(8, 2 ** num_qubits * 0.5), 5))
    # Bar graph, labels on top of bars, formatted to 2 decimal places
    # Left and right margin to prevent waste of space on larger amounts of qubits
    bars = ax.bar(all_states, probabilities)
    ax.margins(x=0.01)
    ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=8)
    ax.set_ylabel("Probabilities")
    # Upper limit for y axis (max prob + 0.1)
    ax.set_ylim(0, max_prob + 0.1)
    # Rotate x axis labels by 45 degrees for space saving
    ax.tick_params(axis="x", labelrotation=45)
    # Grid lines, on y, 60% opaque, dashed style
    plt.grid(axis='y', alpha=0.6, linestyle='--')
    # tight_layout ensures nothing gets clipped
    plt.tight_layout()
    plt.show()

# --------------------------------- BUILD ORACLE -----------------------------
def build_oracle(qubits, target_scheme):
    """
    Build the oracle circuit.

    For each target bitstring (example: "101")
        1. For every qubit that is '0', apply X (flip to 1)
        2. Apply a multi-controlled Z on last qubit
        3. Apply X again to qubits from step 1

    Args:
        qubits: Qubit array to be operated on.
        target_scheme: List of bitstrings representing the states to search for.

    Returns:
        oracle: The oracle circuit, complete for this current running of the simulation.
    """

    # Create an empty circuit
    oracle = cirq.Circuit()

    # Number of qubits (could be passed as a param, but why bother?)
    num_qubits = len(qubits)

    # 1. X gate on all qubits that are '0'
    # Checking the given target for this information
    for target in target_scheme:
        for i, bit in enumerate(target):
            if bit == "0":
                oracle.append(cirq.X(qubits[i]))

        # 2. Apply a multi-controlled Z on last qubit
        oracle.append(cirq.Z.controlled(num_qubits - 1)(*qubits))

        # 3. Apply X again to qubits from step 1
        # Using the same target as step 1
        for i, bit in enumerate(target):
            if bit == "0":
                oracle.append(cirq.X(qubits[i]))

    return oracle

# --------------------------------- BUILD DIFFUSER -----------------------------
def build_diffuser(qubits):
    """
    Grover diffusion function.
    Performs inversion about the mean, essentially amplifying below average states
        and suppressing above average.

    Method:
        H on all → X on all → controlled-Z → X on all → H on all

    Args:
        qubits: Qubit array to be operated on.

    Returns:
        diffuser: The diffuser circuit. This will "find" the actual target.
    """

    # Create an empty circuit
    diffuser = cirq.Circuit()

    # Number of qubits
    num_qubits = len(qubits)

    diffuser.append(cirq.H.on_each(*qubits))
    diffuser.append(cirq.X.on_each(*qubits))
    diffuser.append(cirq.Z.controlled(num_qubits - 1)(*qubits))
    diffuser.append(cirq.X.on_each(*qubits))
    diffuser.append(cirq.H.on_each(*qubits))

    return diffuser

# ============================================================================
# ----------------------------------- MAIN -----------------------------------
# ============================================================================

"""
Performs input checks for validation and whether to run the default or not.
Tries to return meaningful error messages for validation failure.
Default: 3 qubits, target = 111
"""
if __name__ == "__main__":
    if len(sys.argv) < 3:
        num_qubits = 3
        target_scheme = ["111"]
        run_simulation(num_qubits, target_scheme)
        sys.exit(0)

    if not sys.argv[1].isdigit():
        sys.exit("Error: number of qubits must be a positive integer.")
    num_qubits = int(sys.argv[1])
    if num_qubits < 2:
        sys.exit("Error: number of qubits must be at least 2.")

    target_scheme = sys.argv[2:]
    for target in target_scheme:
        if len(target) != num_qubits:
            sys.exit(f"Error: target '{target}' must be {num_qubits} bits long.")
        if not all(bit in "01" for bit in target):
            sys.exit(f"Error: target '{target}' must only contain 0s and 1s.")

    run_simulation(num_qubits, target_scheme)
