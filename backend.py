from qiskit import IBMQ

IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
backends = provider.backends()

print("Available Backends:")
for backend in backends:
    print(backend.name())