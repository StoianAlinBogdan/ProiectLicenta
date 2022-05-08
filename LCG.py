rand = 6969
def lcg():
    global rand
    a = 1664525
    c = 1013904223 # se mentine teorema Hull-Dobell
    m = 2**32
    rand = (a * rand + c) % m
    return rand
    
    
if __name__ == "__main__":
    x = set()
    for i in range(10000000):
        x.add(lcg())
    
    print(len(x))