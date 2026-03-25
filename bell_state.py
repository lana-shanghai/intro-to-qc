from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2) # two qubits

# Add a Hadamard gate to qubit 0
qc.h(0)

# Perform a controlled-X gate on qubit 1, controlled by qubit 0
# TODO

print(qc.draw())

qc_meas = qc.copy()
qc_meas.measure_all()
counts = AerSimulator().run(qc_meas, shots=1024).result().get_counts()

print(counts)

