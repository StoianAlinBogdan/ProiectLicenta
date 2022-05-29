from Performances import QRNG, PRNG
import os
import sys

if __name__ == "__main__":
    PRNGs = PRNG()
    '''
    QRNGs = QRNG()
    numbers = QRNGs.run_Hadamard_1bit()
    with open('Hadamard1Bit.csv', 'w+') as f:
        for number in numbers:
            f.write(str(number) + '\n')
    '''
    '''
    numbers = PRNGs.run_KISS(1000000)
    header = b'#==================================================================\n# generator KISS  seed = 123456789\n#==================================================================\ntype: d\ncount: 1000000\nnumbit: 32\n'
    with open('KISS.out', 'wb') as f:
        f.write(header)
        for number in numbers:
            f.write(bytes(str(number), 'ascii') + b'\n')
    '''
    while True:
        print(PRNGs.run_LCG(1)[0], end='')