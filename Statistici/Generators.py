from email import generator
from qiskit import Aer, QuantumCircuit, transpile, IBMQ
from qiskit_finance.circuit.library import UniformDistribution, NormalDistribution
from qiskit.extensions import Initialize
import math
from Helpers import Box_Muller
import numpy as np
from scipy import stats

class QRNG:
    def __init__(self):
        self.sim = Aer.get_backend('aer_simulator')
        self.QC_Hadamard_1bit = QuantumCircuit(1)
        self.QC_Hadamard_1bit.h(0)
        self.QC_RY_1bit = QuantumCircuit(1)
        self.QC_RY_1bit.ry(math.pi/2, 0)
        self.QC_Hadamard_8bit = QuantumCircuit(8)
        self.QC_Hadamard_8bit.h(range(0, 8))
        self.QC_RY_8bit = QuantumCircuit(8)
        self.QC_RY_8bit.ry(math.pi/2, range(0, 8))
        self.QC_Uniform_1bit = UniformDistribution(1)
        self.QC_Uniform_1bit = transpile(self.QC_Uniform_1bit, self.sim, optimization_level=3)
        self.QC_Uniform_8bit = UniformDistribution(8)
        self.QC_Uniform_8bit = transpile(self.QC_Uniform_8bit, self.sim, optimization_level=3)
        self.QC_Normal_8bit = NormalDistribution(8, mu=0, sigma=1, bounds=(-6, 6))
        self.QC_Normal_8bit = transpile(self.QC_Normal_8bit, self.sim, optimization_level=3)
        self.QC_NormalEu_8bit = self.create_normal_circuit(8)
        self.QC_NormalEu_8bit = transpile(self.QC_NormalEu_8bit, self.sim, optimization_level=3)
        self.API_KEY = None
        self.backend = None

        
        self.QRNGs = [
            self.QC_Hadamard_1bit, self.QC_Hadamard_8bit, self.QC_RY_1bit, self.QC_RY_8bit,
            self.QC_Uniform_1bit, self.QC_Uniform_8bit, self.QC_Normal_8bit, self.QC_NormalEu_8bit
         ]
        for i in range(len(self.QRNGs)):
            self.QRNGs[i].measure_all()

        self.QRNGs = {
            'Hadamard1Bit': self.QC_Hadamard_1bit,
            'Hadamard8Bit': self.QC_Hadamard_8bit,
            'RY1Bit': self.QC_RY_1bit,
            'RY8Bit': self.QC_RY_8bit,
            'Uniform1Bit': self.QC_Uniform_1bit,
            'Uniform8Bit': self.QC_Uniform_8bit,
            'Normal8Bit': self.QC_Normal_8bit,
            'NormalEu8Bit': self.QC_NormalEu_8bit
        }
        self.function_map = {
            'Hadamard1Bit': 'run_Hadamard_1bit',
            'Hadamard8Bit': 'run_Hadamard_8bit',
            'RY1Bit': 'run_RY_1bit',
            'RY8Bit': 'run_RY_8bit',
            'Uniform1Bit': 'run_Uniform_1bit',
            'Uniform8Bit': 'run_Uniform_8bit',
            'Normal8Bit': 'run_Normal_8bit',
            'NormalEu8Bit': 'run_NormalEu_8bit'
        }

    def login(self):
        provider = IBMQ.enable_account(self.API_KEY)
        self.backend = provider.get_backend('ibm_oslo')
    
    def create_normal_circuit(self, size):
        x = np.linspace(-6, 6, num=2**size)
        probabilities = stats.multivariate_normal.pdf(x, 1, 1)
        normalized_probabilities = probabilities / np.sum(probabilities)
        qc_normal = QuantumCircuit(size)
        initial = Initialize(np.sqrt(normalized_probabilities))
        distribution = initial.gates_to_uncompute().inverse()
        qc_normal.compose(distribution, inplace=True)
        return qc_normal

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

    def run_circuit(self, generator_string, amount):
        if self.API_KEY is None:
            qc = self.QRNGs[generator_string]
            if qc.num_qubits == 1:
                result = self.sim.run(qc, shots=8*amount, memory=True).result()
            else:
                result = self.sim.run(qc, shots=amount, memory=True).result()
        else:

            if generator_string == 'Hadamard1Bit':
                qc = QuantumCircuit(7)
                qc.h(range(7))
                qc.measure_all()
                qc = transpile(qc, self.backend, optimization_level=3)
                result = self.backend.run(qc, shots=8*amount, memory=True).result()
            elif generator_string == 'RY1Bit':
                qc = QuantumCircuit(7)
                qc.ry(range(7))
                qc.measure_all()
                qc = transpile(qc, self.backend, optimization_level=3)
                result = self.backend.run(qc, shots=8*amount, memory=True).result()
            elif generator_string == 'NormalEu8Bit':
                qc = self.create_normal_circuit(7)
                qc.measure_all()
                qc = transpile(qc, self.backend, optimization_level=3)
                result = self.backend.run(qc, shots=amount, memory=True).result()
            else:
                pass
        
        memory = result.get_memory()
        if qc.num_qubits == 1:
            numbers = self.concatenate_bits(memory)
        else:
            numbers = [int(x, 2) for x in memory]
        return numbers
            

    def run_Hadamard_1bit(self, amount):
        if self.API_KEY is None:
            qc = self.QRNGs['Hadamard1Bit']
            result = self.sim.run(qc, shots=8*amount, memory=True).result()
        else:
            qc = QuantumCircuit(7)
            qc.h(range(7))
            qc.measure_all()
            qc = transpile(qc, self.backend, optimization_level=3)
            result = self.backend.run(qc, memory=True).result()
        memory = result.get_memory()
        numbers = self.concatenate_bits(memory)
        return numbers

    def run_Hadamard_8bit(self, amount):
        qc = self.QRNGs['Hadamard8Bit']
        result = self.sim.run(qc, shots=amount, memory=True).result()
        memory = result.get_memory()
        for i in range(len(memory)):
            memory[i] = int(memory[i], 2)
        return memory   
    
    def run_RY_1bit(self, amount):
        qc = self.QRNGs['RY1Bit']
        result = self.sim.run(qc, shots=8*amount, memory=True).result()
        memory = result.get_memory()
        numbers = self.concatenate_bits(memory)
        return numbers
    
    def run_RY_8bit(self, amount):
        qc = self.QRNGs['RY8Bit']
        result = self.sim.run(qc, shots=amount, memory=True).result()
        memory = result.get_memory()
        for i in range(len(memory)):
            memory[i] = int(memory[i], 2) 
        return memory    

    def run_Uniform_1bit(self, amount):
        qc = self.QRNGs['Uniform1Bit']
        qc.draw(output='mpl', filename='./testImg.png')
        result = self.sim.run(qc, shots=8*amount, memory=True).result()
        memory = result.get_memory()
        numbers = self.concatenate_bits(memory)
        return numbers

    def run_Uniform_8bit(self, amount):
        qc = self.QRNGs['Uniform8Bit']
        result = self.sim.run(qc, shots=amount, memory=True).result()
        memory = result.get_memory()
        for i in range(len(memory)):
            memory[i] = int(memory[i], 2)
        return memory 

    def run_Normal_8bit(self, amount):
        qc = self.QRNGs['Normal8Bit'] 
        result = self.sim.run(qc, shots=amount, memory=True).result()
        memory = result.get_memory()
        for i in range(len(memory)):
            memory[i] = int(memory[i], 2)
        return memory
    
    def run_NormalEu_8bit(self, amount):
        qc = self.QRNGs['NormalEu8Bit']
        result = self.sim.run(qc, shots=amount, memory=True).result()
        memory = result.get_memory()
        for i in range(len(memory)):
            memory[i] = int(memory[i], 2)
        return memory


class PRNG:
    def __init__(self):
        self.LCG_rand = 6969
        self.LCG_a = 1664525
        self.LCG_c = 1013904223
        self.m = 2 ** 32
        self.jsr = 123456789
        self.jcong = 380116160
        self.z = 362436069
        self.w = 521288629

        self.generators = ['LCG', 'KISS']
        self.function_map = {
            'LCG': 'run_LCG',
            'KISS': 'run_KISS'
        }

    def run_LCG(self, shots):
        numbers = []
        for i in range(shots):
            self.LCG_rand =  (self.LCG_a * self.LCG_rand + self.LCG_c) % self.m
            numbers.append(self.LCG_rand)
        maxim = max(numbers)
        numbers = [round((i / maxim)*255) for i in numbers]
        return numbers
    
    def run_KISS(self, shots):
        numbers = []
        for i in range(shots):
            #SHR3
            self.jsr = (self.jsr ^ ((self.jsr << 17) % self.m)) % self.m
            self.jsr = (self.jsr ^ ((self.jsr >> 13 ) % self.m)) % self.m
            self.jsr = (self.jsr ^ ((self.jsr << 5) % self.m)) % self.m
            #CONG
            self.jcong = ((69069 * self.jcong) % self.m + 1234567) % self.m
            #MWC
            self.z = ((36969 * (self.z & 65535)) % 2 ** 16 + (self.z >> 16) ) % 2 ** 16
            self.w = ((18000 * (self.w & 65535)) % 2 ** 16 + (self.w >> 16) ) % 2 ** 16
            mwc = ((self.z << 16) + self.w) % self.m
            numbers.append(mwc)
        maxim = max(numbers)
        numbers = [round((i / maxim)*255) for i in numbers]
        return numbers