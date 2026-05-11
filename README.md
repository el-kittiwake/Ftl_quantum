# Ftl_quantum

Subject version 2

"This project is an introduction to quantum programming. It will challenge you to create different quantum programs, and run them on a real quantum computer."

I attempted to do this work in Cirq, by Google. However, if I had researched better I would have realised that getting ex02 to work using the systems available is a nightmare. It took me many attempts over a couple of hours to fail and give up.

So, for the sake of completing this in a reasonable time I did ex02 in IBM Qiskit. The process for setting up an account, getting a free API key and running software was completed in less than an hour.

The evaluation sheet also gives you the code changes required as qiskit snippets. This along with differences in how cirq and qiskit work make it a bad idea to use any other framework than qiskit for these exercises.

For details regarding adapting between different frameworks please see the [Qiskit/Cirq adaptation](#qiskitcirq-adaptation) section below.

## Usage

```bash
# Run an exercise
# Virtual environment will be set up if needed
make ex00
make ex01
make ex02   # requires IBM_TOKEN in a .env file
make ex03
make ex04
make bonus

# Clean the virtual environment
make clean
```

**ex02** requires a `.env` file in the project root, contents below:

```
IBM_TOKEN=your_token_here
IBM_SIMULATE=true   # false to run on real hardware
```

- If IBM_TOKEN is not present then a local noiseless simulation will run.
- If IBM_TOKEN is present and IBM_SIMULATE is true, then a local noisy simulation (using the FakeFez simulator) will run.
- If IBM_TOKEN is present and IBM_SIMULATE is false, then the circuit will run on an IBM quantum machine (usually Fez, a Heron r2 based machine with 156 qubits).


**ex04** takes optional parameters to specify the number of qubits and target states:

```bash
.venv/bin/python3 ex04/ex04.py <num_qubits> <targets>
```

- `num_qubits` - number of qubits (minimum 2). The search space is 2^num_qubits states.
- `targets` - bitstrings of length num_qubits representing the states to search for.

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

The subject consists of 5 mandatory exercises and the chance to implement bonus algorithms.

### Exercise 0

Create a superposition of a single qubit. Given in bra-ket notation: 1/√2 (|0⟩ + |1⟩)

Superposition is the situation where the value of a qubit is in a state between 0 and 1 and thus can be considered to be in both states at the same time.

Once measured, the qubit will rest at its final state of 0 or 1. Until then, it has a 50% probability of being either value.

This is the phenomenon on which the Schrödinger's cat thought experiment is based.

###### Bra-ket notation

This quantum arrangement has the bra-ket notation: 1/√2 (|0⟩ + |1⟩)

Essentially meaning: "This qubit has a 50% chance of being measured as 0, and a 50% chance of being measured as 1, and both possibilities have the same phase."

- 1/√2: Amplitude of each outcome. Actual probability: (1/√2)² = 1/2 = 50%.
- |0⟩ and |1⟩: Possible measurement outcomes. | ⟩ essentially means "quantum state of".
- +: Both outcomes have the same phase, they'll interfere constructively.


### Exercise 1

Entangle a pair of qubits. Given in bra-ket notation: 1/√2 (|00⟩ + |11⟩)

When two qubits are connected in some way (CNOT gates are used in these exercises) they cannot be measured independently. The act of measuring one, will cause the connected qubit to read the same value. Regardless of the distance between them.

This is the phenomenon at the heart of the difficulty of marrying classical and quantum paradigms. What Einstein called "spooky action at a distance".


### Exercise 2

Run the entanglement circuit (ex01) on real/simulated IBM quantum hardware using Qiskit. Observe and discuss the concept of quantum noise.

###### Sources of noise

1. Decoherence: Qubits deteriorate over time due to environmental interference, i.e. heat, vibration and EMI effects.
2. Gate errors: Real gates don't work as precisely as simulated gates, this causes some errors which accumulate as the qubits pass through the circuit.
3. Measurement error: As with gates, measurements aren't perfectly precise.
4. Crosstalk: Physical qubits on real hardware are close to each other. This can lead to leakage and one qubit disturbing its neighbour.

###### IBM architecture

As of completing this project, free allowance quantum work is done on IBM Heron r2 architecture. On the machines: ibm_kingston, ibm_fez or ibm_marrakesh (the latter two have noisy simulator models available).

Each run of this exercise on quantum hardware takes about 2 seconds. This is taken from the monthly free allowance of 10 minutes of compute time.

These machines consist of 156 qubits of the transmon type. Two superconducting metal pads separated by a thin insulator (Josephson junction acting as an inductor) in parallel with a capacitor. The qubits (ergo the quantum chip) need to be chilled down to the tens of millikelvin in order to function.

The qubits are operated on by microwave pulses. State change happens when a microwave pulse of a specific phase, amplitude and length is applied. The qubit can be read by a resonating microwave that changes frequency depending on the energy state of the qubit.

### Exercise 3

This is where it starts to get more complicated.

Implement and test the Deutsch-Jozsa algorithm. The first algorithm that performs its task faster than a classical computer can. It is somewhat similar to a classical "black box" problem, but using quantum ideas.

###### Analogy

We have a sealed envelope inside which is written a mystery function. We know the function is one of two types:
- constant (always returns the same value regardless of input)
- balanced (returns 0 for exactly half of all possible inputs and 1 for the other half)
We are not allowed to open the envelope to check. We can only post inputs into a machine, and read what comes out.

A classical computer has to check inputs individually, and may need to try up to half of all combinations before it can be sure what kind it is. The quantum version checks all possible inputs simultaneously in a single query (in our case 3 bits). The result is always `000` if the function is constant, or `111` if it is balanced. A definitive classification from a single query, with no ambiguity.

###### Program

We create our input qubits (3 in our case) and the output qubit. The input qubits are the inputs we post into the machine in our analogy. The output qubit is only used to facilitate the algorithm and is never measured.

These qubits are put into superposition. The initial qubits go from `|0⟩` to superposition with a single Hadamard gate. Together all three represent all possible 3 bit combinations from `000` to `111`. The output qubit is operated on by an X gate followed by a Hadamard gate. This results in a state of `|−⟩`, a superposition state where each possible value can have different phases.

The oracle is now applied. CNOT (controlled not/X) gates are applied to the output qubit with the input qubits as control. If desired, we can apply X gates before and after the CNOT gate on any chosen input qubit.

Because the output qubit is in the `|−⟩` state, something unusual happens when a CNOT fires. Instead of flipping the output qubit, the effect bounces back and flips the phase of the input qubit that triggered it. This is known as *phase kickback*. It always occurs for any CNOT whose input qubit causes the function to return 1. This is the key to the determination of whether the function is constant or balanced.

- constant: the phases are all the same — either none are flipped (f=0) or all are flipped uniformly (f=1)
- balanced: exactly half the input qubits' phases are flipped, the other half are not

Finally, all input qubits pass through one more Hadamard gate. The Hadamard gate is its own inverse, so this action essentially undoes the superposition. The phase state of each qubit determines what it collapses to:

- constant: all phases are uniform (all the same, whether all flipped or none flipped). Uniform phases interfere constructively and the qubits collapse back to `|0⟩`. Measuring gives `000`.
- balanced: half the phases are flipped, half are not. The opposing phases cancel each other out (destructive interference) and the qubits are forced to `|1⟩`. Measuring gives `111`.

All that is left to do is measure the input qubits and visualise or otherwise display the result.


### Exercise 4

Implement and test the quantum search algorithm. Which is also known as Grover's algorithm.

This algorithm was published a couple of years after Deutsch-Jozsa and is provably the optimal quantum search algorithm. It works by repeatedly amplifying the probability of the target state whilst suppressing all others, until only the desired one dominates.

###### Analogy

We have a row of spinning tops, each one a separate target "value". At the beginning, every top is spinning with a gentle wobble, equally likely to fall in any direction. No target is favoured.

The oracle's purpose is to essentially nudge the target top causing it to lean in a single direction. The difference in lean is so slight as to be almost immeasurable.

The diffuser now comes into play and looks at the average lean across all tops and amplifies it. The top that was nudged earlier gets pushed to lean further and the others get nudged to wobble less. Each oracle and diffuser iteration results in the target top wobbling a little more noticeably while the rest straighten up a little more.

After a certain number of cycles (roughly √N), the target top is leaning heavily in one direction while every other top is nearly perfectly upright. When you finally let them fall (measure), the target falls in its direction while the others just fall over.

###### Program

We create our qubits and put them through a Hadamard gate. This puts them into superposition. With the default three qubits, each state has an equal probability of 12.5%.

We build the oracle next. The oracle can be any circuit that flips a desired target's state to the negative while leaving others untouched. The default oracle uses an X gate to flip any bits that are 0 in the target to 1, then flips the phase of all qubits using a Z gate before finally undoing those X flips. This marks the target state. The target's amplitude is now negative and the mean amplitude is slightly below the original uniform value.

The workhorse of the algorithm is the diffuser. Simply put, it reflects amplitudes around the mean. Amplitudes above the mean get reduced slightly, and the target's negative amplitude gets reflected to a large positive value. With each iteration of oracle + diffuser the target's amplitude increases while all others decrease. After all iterations have finished, the target(s) has almost all of the probability.

The number of iterations is an important factor. It is generally given as (π/4)√N where N is the number of states. With multiple targets this becomes (π/4)√(N/k), where k is the number of targets.

The final step is to measure. Doing so collapses the superpositions and reveals the correct answer. Doing multiple runs should result in a chart with the correct answer having an almost 100% share of the "winning" results.


### Bonus

I chose to implement quantum teleportation. This transfers the quantum state of one qubit to another without physically moving it. Einstein's "spooky action at a distance" put to practical use.

Traditionally demonstrated using two theoretical people, Alice and Bob. Alice has a message qubit she wants to send. Bob has a receiving qubit. They share a pre-entangled pair of qubits.

###### Program

Three qubits are created. Q0 is the message qubit we are trying to transfer. Q1 is Alice's half of the entangled pair. Q2 is Bob's half, which will receive the transferred message qubit's state.

The message qubit Q0 is prepared in the state to be sent: `|0⟩`, `|1⟩`, or `|+⟩`.

Alice first entangles Q1 and Q2 into a Bell state by sending them through a Hadamard gate followed by a CNOT. She then entangles her message qubit Q0 with Q1 with another CNOT, followed by a Hadamard gate on Q0. This results in all three qubits being entangled. She measures Q0 and Q1, producing two classical bits. The act of measuring destroys Q0's quantum state because a quantum state cannot be copied.

Alice sends the two classical bits to Bob by whatever means she has available to her. Nothing has travelled faster than light. The bits act as a guide to what was read during measurement.

Bob puts his Q2 qubit through gates based on those classical bits. If Alice's Q1 measured 1, Bob puts Q2 through an X gate. If Alice's Q0 measured 1, Bob puts it through a Z gate. These actions undo the disturbance caused by Alice's entanglement and measurement, resulting in Q2 taking the exact state Q0 started in.

Measuring Q2 across multiple runs confirms it matches the original message state.


## Qiskit/Cirq adaptation

The evaluation sheet provides oracle code that must be used to test the work done. This code is provided as Qiskit snippets. The table below maps the Qiskit gates used in the eval oracles to their Cirq equivalents.

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
