import qiskit as q
import numpy as np


# define the input number
n = 15

# creating quantum circuit

circuit = q.QuantumCircuit(n)

# add Hadamard gates to first n qubits

for i in range(n):
    circuit.h(i)

# add controlled U-gate first n-1 qubits
for i in range(n -1):
    circuit.cx(i, i + 1)

# add measurement gate
for i in range(n):
    circuit.measure(i, i)


# Run the circuit on the quantum computer
# run the circuit 1024 for initial trail, increase or decrease depending on results

backend = q.IBMQ.get_backend('ibmq_babbage')
job = q.execute(circuit, backend, shots=1024)

# store result

results = job.result()
counts = results.get_counts()

# determine the factor of input number

for key, value in counts.iteams():
    if value > 0:
        factor = [int(key[0]), int(key[1])]
        break


# test for shor's algorithm

def test_shor(n):
  circuit = create_shor_circuit(n)
  results = execute_circuit(circuit)
  factors = determine_factors(results)
  assert factors == factor(n)
