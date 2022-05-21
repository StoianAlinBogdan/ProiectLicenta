import numpy as np
import math
import matplotlib.pyplot as plt

def BoxMuller(u1, u2):
    z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * math.pi * u2)
    z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * math.pi * u2)
    return (z1, z2)
    
if __name__ == "__main__":
    u1 = np.random.rand(800000)
    plt.subplot(4,1,1)
    plt.hist(u1)
    u2 = np.random.rand(800000)
    plt.subplot(4,1,2)
    plt.hist(u2)
    z1, z2 = BoxMuller(u1, u2)
    plt.subplot(4,1,3)
    plt.hist(z1)
    plt.subplot(4,1,4)
    plt.hist(z2)
    plt.show()
    