import struct

with open("/dev/random", "rb") as f:
    for i in range(10):
        x = f.read(4)
        tup = struct.unpack("I", x)
        print(tup[0])