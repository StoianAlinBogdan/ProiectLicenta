import cmath
from random import random
from qiskit import Aer, QuantumCircuit, transpile

import matplotlib.pyplot as plt

if __name__ == "__main__":
    sim = Aer.get_backend('aer_simulator')
    numbers = []

    for i in range(100000):
        theta = random() * cmath.pi
        phi = random() * 2 * cmath.pi
        qc = QuantumCircuit(1)
        qc.initialize([cmath.cos(theta / 2), cmath.exp(phi * 1j) * cmath.sin(theta/2)])
        qc.measure_all()
        qc = transpile(qc, sim, optimization_level=3)

        result = sim.run(qc, shots=1, memory=True).result()
        memory = result.get_memory()
        for i in range(len(memory)):
            memory[i] = int(memory[i], 2)
        numbers.append(memory[0])
    uniques = list(set(numbers))
    counts = {x: memory.count(x) for x in uniques}
    plt.bar(counts.keys(), counts.values(), width=1)
    plt.show()
    
