import numpy as np
import math
import matplotlib.pyplot as plt

def BoxMuller(u1, u2):
    z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * math.pi * u2)
    return z
    
if __name__ == "__main__":
    u1 = np.random.rand(800000) * 10
    plt.subplot(3,1,1)
    plt.hist(u1)
    u2 = np.random.rand(800000) * 10
    plt.subplot(3,1,2)
    plt.hist(u2)
    z = BoxMuller(u1, u2)
    plt.subplot(3,1,3)
    plt.hist(z)
    plt.show()
    