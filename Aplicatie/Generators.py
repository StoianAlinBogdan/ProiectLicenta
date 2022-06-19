from qiskit import Aer, QuantumCircuit, transpile
from qiskit_finance.circuit.library import UniformDistribution
import math
import numpy as np

def Box_Muller(u1, u2):
    u1 = np.array(u1)
    u2 = np.array(u2)
    u1 = u1 / max(u1)
    u2 = u2 / max(u2)
    z1 = np.sqrt(-2 * np.log(u1, where=u1>0)) * np.cos(2 * math.pi * u2)
    z2 = np.sqrt(-2 * np.log(u1, where=u1>0)) * np.sin(2 * math.pi * u2)
    z1 = np.round_((z1 / max(z1))*255)
    z2 = np.round_((z2 / max(z2))*255)
    z1 = np.nan_to_num(z1)
    z2 = np.nan_to_num(z2)
    return (z1.tolist(), z2.tolist())

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
        self.QRNGs = [self.QC_Hadamard_1bit, self.QC_Hadamard_8bit, self.QC_RY_1bit, self.QC_RY_8bit, self.QC_Uniform_1bit, self.QC_Uniform_8bit]
        for i in range(len(self.QRNGs)):
            self.QRNGs[i].measure_all()

        self.QRNGs = {
            'Hadamard1Bit': self.QC_Hadamard_1bit,
            'Hadamard8Bit': self.QC_Hadamard_8bit,
            'RY1Bit': self.QC_RY_1bit,
            'RY8Bit': self.QC_RY_8bit,
            'Uniform1Bit': self.QC_Uniform_1bit,
            'Uniform8Bit': self.QC_Uniform_8bit
        }
        self.function_map = {
            'Hadamard1Bit': 'run_Hadamard_1bit',
            'Hadamard8Bit': 'run_Hadamard_8bit',
            'RY1Bit': 'run_RY_1bit',
            'RY8Bit': 'run_RY_8bit',
            'Uniform1Bit': 'run_Uniform_1bit',
            'Uniform8Bit': 'run_Uniform_8bit'
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