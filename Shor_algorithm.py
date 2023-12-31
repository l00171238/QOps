import numpy as np
from qiskit import QuantumCircuit, transpile, assemble, Aer, execute
from math import gcd
import time
from qiskit.visualization import plot_histogram
from qiskit import IBMQ
import os

IBM_TOKEN = os.environ["IBM_TOKEN"]

IBMQ.save_account(IBM_TOKEN)
IBMQ.load_account()

# Define the quantum part of Shor's algorithm
def qpe_amod15(a):
    n_count = 8
    qc = QuantumCircuit(4 + n_count, n_count)

    for q in range(n_count):
        qc.h(q)  # Initialize counting qubits in state |+
    qc.x(3 + n_count)  # And auxiliary register in state |1>
    for q in range(n_count):
        qc.append(c_amod15(a, 2 ** q),
                  [q] + [i + n_count for i in range(4)])
    qc.append(qft_dagger(n_count), range(n_count))  # Do inverse-QFT
    qc.measure(range(n_count), range(n_count))

    # Simulate Results
    aer_sim = Aer.get_backend('aer_simulator')
    # Setting memory=True below allows us to see a list of each sequential reading
    # for each experiment.
    # Setting shots=1 gives us the most accurate possible result by only measuring
    # each state once, but it takes longer.
    # Setting memory=False gives us a faster result that's slightly less accurate.
    # But it looks like we get the right answer in one try!


    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc, shots=1)
    result = aer_sim.run(qobj, memory=True).result()
    readings = result.get_memory()
    print("Register Reading: " + readings[0])
    print(readings)

    # Print and display the circuit
    print("Quantum Circuit:")
    print(qc.draw(output='text'))

    time.sleep(5)
    # Return the number of times the reading is '0000'
    print("Shor's algorithm guess: " + str(int(readings[0], 2)))
    return int(readings[0], 2)

    # Get the measurement results
    results = qpe_amod15(a).result()

    # Plot the histogram
    plot_histogram(results.get_counts())


provider = IBMQ.get_provider('ibm-q')
backend = provider.get_backend('ibmq_qasm_simulator')  # Choose a backend


# Define the Quantum Fourier Transform
def qft_dagger(n):
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc


# Create controlled-U gate
def c_amod15(a, power):
    U = QuantumCircuit(4)
    for iteration in range(power):
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
        for q in range(4):
            U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U


# Now, let's run the algorithm
N = 100  # The number to be factored
a =10 # The "a" in a^x mod N
factor_found = False

print("Running Shor's algorithm for N =", N)

while not factor_found:
    print("Attempt with a =", a)
    # Compute the greatest common divisor of a^x - 1 and N
    gcd_candidate = gcd(a, N)

    if gcd_candidate > 1:
        print("Found a non-trivial factor:", gcd_candidate)
        factor_found = True
        break

    measured = qpe_amod15(a)  # Apply the quantum part of the algorithm
    # Attempt to find a non-trivial factor using the measured result
    guesses = []
    for guess in range(1, N):
        if pow(a, guess, N) == measured:
            guesses.append(guess)
    if len(guesses) > 0:
        print("Guesses:", guesses)
        factor_found = True
    else:
        print("No guesses found, trying a different 'a'")
        a = np.random.randint(2, N)

def test_correct_factoring():
    """
    Test that the Shor's algorithm can correctly factor the input number.
    """

    # Generate a random input number
    N = np.random.randint(100, 1000)

    # Find the factors of N
    factors = list(factors(N))

    # Run Shor's algorithm on N
    measured = qpe_amod15(a)

    # Check that the measured value is one of the factors of N
    assert measured in factors



print("Quantum Circuit:")
circuit = qpe_amod15(a)  # Use the original qpe_amod15(a) function

