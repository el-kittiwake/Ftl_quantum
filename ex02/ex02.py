"""
"Exercise 02: Quantum noise
Take the program from exercise 3, and modify it to run your circuit on a real quantum
computer."

Subject for this is strange because the implication is that exercise 2 needs to
be a modification of exercise 3?
In the notes for the exercise it states:
	"Your results between exercise 3 and 4 should be different, even though the
    circuit	is identical. It's up to you to understand why."
Exercise 3 and 4 are totally different algorithms.

It is possible that this exercise is:
	1. Meant to be after the current exercise 3 (Deutsch-Jozsa).
	2. In the right location and we are supposed to do the entanglement exercise
        on actual quantum hardware.
I am assuming 2 and working accordingly.

This exercise will be the real quantum hardware running of exercise 1.
Quantum entanglement.

However, my choice of Cirq as development framework was poor and I could not
get Microsoft Azure (the service I would need to run cirq programs) to work
without paying. So this exercise will be done in Qiskit, IBM's quantum development
framework. IBM offer easy access to free tokens for quantum time. Qiskit is also
a python framework so the porting of ex01 should not be too complicated.

    !!!!  If this requires a virtual environment, make sure to activate it first.
    !!!!  `python3 -m venv .venv`
    !!!!  `source .venv/bin/activate`
    !!!!  `pip install --quiet qiskit qiskit-ibm-runtime qiskit-aer matplotlib cirq`
"""

# ============================================================================
# ------------------------------ IMPORT DEPENDENCIES -------------------------
# ============================================================================

# Allows the script to be run without qiskit and matplotlib being installed, will install if needed.
# Allows running of shell commands
import subprocess
# Allows access to system-specific parameters and functions
import sys
import os

# Supress Qiskit informational messages
import logging
logging.getLogger("qiskit_ibm_runtime").setLevel(logging.ERROR)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("installing matplotlib...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "matplotlib"])
    import matplotlib.pyplot as plt
    print("installed matplotlib.")

# Qiskit imports seem more complicated than cirq.
# I guess this is expected because this appears to be a more mature framework.
try:
    from qiskit import QuantumCircuit
    # Translates to target hardware
    from qiskit.transpiler import generate_preset_pass_manager
except ImportError:
    print("installing qiskit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "qiskit"])
    from qiskit import QuantumCircuit
    from qiskit.transpiler import generate_preset_pass_manager
    print("installed qiskit.")

try:
    # Authentication and connection to IBM hardware
    from qiskit_ibm_runtime import QiskitRuntimeService
    # The actual simulation running component. like: `simulator.run(circuit, repetitions=500)`
    from qiskit_ibm_runtime import SamplerV2
    # Noisy fake backend that mimics a real IBM device - used for level 2 simulation
    # Fez, Marrakesh and Kingston should all be available.
	# Using Fez (156 qubit) as that is what my real runs seem to be using.
    from qiskit_ibm_runtime.fake_provider import FakeFez
except ImportError:
    print("installing qiskit-ibm-runtime...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "qiskit-ibm-runtime"])
    from qiskit_ibm_runtime import QiskitRuntimeService
    from qiskit_ibm_runtime import SamplerV2
    print("installed qiskit-ibm-runtime.")

try:
    # Local simulator
    from qiskit_aer import AerSimulator
except ImportError:
    print("installing qiskit-aer...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "qiskit-aer"])
    from qiskit_aer import AerSimulator
    print("installed qiskit-aer.")

# Envariables for dictating program flow.
# Levels are: local, local with noise, quantum hardware
IBM_API_KEY = os.environ.get("IBM_TOKEN")
IBM_SIM = os.environ.get("IBM_SIMULATE", "true")

# Number of shots to run of the chosen simulation.
# 500 given by subject
reps=500

# ============================================================================
# -------------------------- EXERCISE 02 CODE STARTS HERE --------------------
# ============================================================================

# ============================================================================
# --------------------------------- DEFINITIONS ------------------------------
# ============================================================================

def build_circuit():
    """
    Build the entanglement circuit 1/√2 (|00⟩ + |11⟩).
    Identical for all three levels.

    Returns:
        ent_circuit: The quantum entanglement circuit.
    """
    ent_circuit = QuantumCircuit(2)
    # sx() is the Qiskit equivalent of X**0.5
    ent_circuit.sx(0)
    ent_circuit.cx(0, 1)
    ent_circuit.measure_all()

    print("Circuit diagram for all levels (Ext ASCII):\n")
    print(ent_circuit.draw("text"))

    return ent_circuit


def authenticate():
    """
    Authenticate with IBM Quantum using the IBM_TOKEN environment variable.
    Only needed for level three.

    Returns:
        service: Authenticated QiskitRuntimeService instance.
    """
    service = QiskitRuntimeService(token=IBM_API_KEY)

    return service


def run_local(circuit, reps=reps):
    """
    Level 1: Run circuit on local noiseless simulator.
    Very simple, essentially the Qiskit version of the Cirq code in ex01.
    No need for any "compilation" to specific hardware. This comes later.

    Args:
        circuit: The quantum circuit to run.
        reps: The number of shots to run.
    Returns:
        counts: dict of bitstring outcome counts.
    """
    print("Running local noiseless simulator. IBM_TOKEN not found.\n")
    sampler = SamplerV2(AerSimulator())
    result = sampler.run([circuit], shots=reps).result()
    counts = result[0].data.meas.get_counts()

    print(f"Counts for {reps} shots: {counts}")

    return counts


def run_noisy(circuit, reps=reps):
    """
    Level 2: Run circuit on a fake backend with noise model.
    Using FakeMarrakesh, but FakeFez would also be suitable.
    API key grants me access to these 156 qubit backends: Fez, Marrakesh, Kingston

    Args:
        circuit: The quantum circuit to run.
        reps: The number of shots to run.
    Returns:
        counts: dict of bitstring outcome counts.
    """
    print("Running local noisy fake backend (FakeFez). IBM_SIMULATE set to true.\n")
    fake_backend = FakeFez()
    pm = generate_preset_pass_manager(backend=fake_backend, optimization_level=1)
    transpiled = pm.run(circuit)
    sampler = SamplerV2(fake_backend)
    result = sampler.run([transpiled], shots=reps).result()
    counts = result[0].data.meas.get_counts()

    print(f"Counts for {reps} shots: {counts}")

    return counts


def run_real(circuit, service, reps=reps):
    """
    Level 3: Run circuit on IBM quantum hardware.
        Requires API key and available runtime.
        Free tier is limited to 10 minutes per month.

    Args:
        circuit: The quantum circuit to run.
        service: Authenticated QiskitRuntimeService instance.
        reps: The number of shots to run.
    Returns:
        counts: dict of bitstring outcome counts.
    """
    print("Running on remote quantum hardware.\n")
    
    try:
        backend = service.least_busy(simulator=False, operational=True)
    except Exception as e:
        sys.exit(f"No backend available: {e}")

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    transpiled = pm.run(circuit)
    sampler = SamplerV2(backend)
    result = sampler.run([transpiled], shots=reps).result()
    counts = result[0].data.meas.get_counts()

    print(f"Counts for {reps} shots: {counts}")

    return counts


def visualise(counts):
    """
    Plot measurement results as a probability bar chart.

    Args:
        counts: dict of bitstring outcome counts e.g. {'00': 243, '11': 257}.
    """
    total = sum(counts.values())
    all_states = ['00', '01', '10', '11']
    # Expected Bell state outcomes are |00⟩ (index 0) and |11⟩ (index 3)
    expected_indices = {0, 3}
    probabilities = [counts.get(s, 0) / total for s in all_states]

    # Create subplot axes and draw bars with blue for expected states, red for unexpected
    ax = plt.subplot()
    bars = ax.bar(range(4), probabilities,
                  color=['blue' if i in expected_indices else 'red' for i in range(4)])
    ax.set_ylabel('Probability')
    ax.set_xticks(range(4))
    ax.set_xticklabels(['|00⟩', '|01⟩', '|10⟩', '|11⟩'])
    for bar, prob in zip(bars, probabilities):
        # Place the probability value as text centred above the bar, display 3 decimal places
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{prob:.3f}',
                ha='center', va='bottom')
    # Set y-axis ceiling to 0.1 above the tallest bar so labels aren't clipped
    ax.set_ylim(0, max(probabilities) + 0.1)
    plt.show()


# ============================================================================
# ----------------------------------- MAIN -----------------------------------
# ============================================================================

if __name__ == "__main__":
    circuit = build_circuit()

    if not IBM_API_KEY:
        counts = run_local(circuit, reps)
    elif IBM_SIM.lower() == "true":
        counts = run_noisy(circuit, reps)
    else:
        try:
            service = authenticate()
        except Exception as e:
            sys.exit(f"Authentication failed: {e}")
        counts = run_real(circuit, service, reps)

    visualise(counts)
