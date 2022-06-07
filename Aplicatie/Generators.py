from qiskit import Aer, QuantumCircuit, transpile
from qiskit_finance.circuit.library import UniformDistribution
import math


class QRNG:
    def __init__(self):
        self.QC_Hadamard_1bit = QuantumCircuit(1)
        self.QC_Hadamard_1bit.h(0)
        self.QC_RY_1bit = QuantumCircuit(1)
        self.QC_RY_1bit.ry(math.pi/2, 0)
        self.QC_Hadamard_8bit = QuantumCircuit(8)
        self.QC_Hadamard_8bit.h(range(0, 8))
        self.QC_RY_8bit = QuantumCircuit(8)
        self.QC_RY_8bit.ry(math.pi/2, range(0, 8))
        self.QC_Uniform_1bit = UniformDistribution(1)
        self.QC_Uniform_8bit = UniformDistribution(8)
        self.QRNGs = [self.QC_Hadamard_1bit, self.QC_Hadamard_8bit, self.QC_RY_1bit, self.QC_RY_8bit, self.QC_Uniform_1bit, self.QC_Uniform_8bit]
        for i in range(len(self.QRNGs)):
            self.QRNGs[i].measure_all()
        self.sim = Aer.get_backend('aer_simulator')
        for i in range(len(self.QRNGs)):
            self.QRNGs[i] = transpile(self.QRNGs[i], self.sim, optimization_level=3)
        
        self.QRNGs = {
            'Hadamard1Bit': self.QC_Hadamard_1bit,
            'Hadamard8Bit': self.QC_Hadamard_8bit,
            'RY1Bit': self.QC_RY_1bit,
            'RY8Bit': self.QC_RY_8bit,
            'Uniform1Bit': self.QC_Uniform_1bit,
            'Uniform8Bit': self.QC_Uniform_8bit
        }

    def concatenate_bits(self, memory):
        numbers = []
        temp = ''
        c = 0
        for i in range(len(memory)):
            temp = temp + memory[i]
            c = c + 1
            if c == 8:
                numbers.append(temp)
                temp = ''
                c = 0
        numbers = [int(x, 2) for x in numbers]
        return numbers

    def run_Hadamard_1bit(self, amount):
        qc = self.QRNGs['Hadamard1Bit']
        result = self.sim.run(qc, shots=8*amount, memory=True).result()
        memory = result.get_memory()
        numbers = self.concatenate_bits(memory)
        return numbers