from math import gcd
from fractions import Fraction

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator


N = 15  # Number to factor
a = 2   # Randomly chosen base coprime to N

# Bail out early if a shares a factor with N (gives a factor for free)
if gcd(a, N) != 1:
    print("Trivial factor:", gcd(a, N))
    raise SystemExit


def c_amod15(a, power):  # Build controlled-U gate for a^power mod 15
    # Only a handful of bases have hardcoded modular-mult circuits here
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("This toy circuit only supports selected a values for N=15")

    U = QuantumCircuit(4)  # 4-qubit register holds the work value mod 15

    for _ in range(power):  # Repeat the base operation 'power' times
        if a in [2, 13]:    # Multiply by 2/13: cyclic shift of qubits
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:     # Multiply by 7/8: reverse-direction shift
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [4, 11]:    # Multiply by 4/11: swap qubit pairs
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:        # These bases need a bit flip on every qubit
            for q in range(4):      # Apply X to each of the 4 qubits
                U.x(q)

    gate = U.to_gate()                  # Convert the circuit into a single gate
    gate.name = f"{a}^{power} mod 15"   # Label it for readability in diagrams
    return gate.control()               # Add a control qubit -> controlled-U


n_count = 8  # Number of counting (phase-estimation) qubits

qc = QuantumCircuit(n_count + 4, n_count)  # Counting qubits + 4 work qubits + n_count classical bits

for q in range(n_count):  # Put all counting qubits into superposition
    qc.h(q)

qc.x(n_count)  # Initialize the work register to |1>

for q in range(n_count):  # Apply controlled-U^(2^q) for each counting qubit
    qc.append(c_amod15(a, 2 ** q), [q] + list(range(n_count, n_count + 4)))

qc.append(QFT(n_count, inverse=True).to_gate(), range(n_count))  # Inverse QFT to extract the phase

qc.measure(range(n_count), range(n_count))  # Measure counting qubits into classical bits

backend = AerSimulator()                          # Local Aer state-vector simulator
compiled = transpile(qc, backend)                 # Optimize circuit for the backend
result = backend.run(compiled, shots=2048).result()  # Run 2048 shots
counts = result.get_counts()                      # Histogram of measured bitstrings

print("Counts:")
print(counts)

print("\nCandidate periods:")
# Inspect the 10 most frequent measurement outcomes
for measured, freq in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    decimal = int(measured, 2)          # Bitstring -> integer
    phase = decimal / (2 ** n_count)    # Estimated phase = s/r
    frac = Fraction(phase).limit_denominator(N)  # Continued-fraction approx of the phase
    r = frac.denominator                # Candidate period r
    print(measured, "freq=", freq, "phase=", phase, "r=", r)

    if r % 2 == 0:                      # Period must be even to recover factors
        x = pow(a, r // 2, N)           # Compute a^(r/2) mod N
        f1 = gcd(x - 1, N)              # Try gcd(x-1, N)
        f2 = gcd(x + 1, N)              # Try gcd(x+1, N)
        if f1 not in [1, N] and f2 not in [1, N]:  # Accept only non-trivial factors
            print("Factors:", f1, f2)
            break                       # Stop once a valid factorization is found