jsr = 123456789 # nu-s de acord, dar marsaglia e bazat
jcong = 380116160 # cine stie cum dracu a facut rost de numarul asta

#znew = 36969 * (362436069 and 65535) + (362436069 >> 16)
#wnew = 18000 * (521288629 and 65535) + (521288629 >> 16)
z = 362436069
w = 521288629


def SHR3():
    global jsr
    jsr = jsr ^ (jsr << 17)
    jsr = jsr ^ (jsr >> 13)
    jsr = jsr ^ (jsr << 5)
    jsr = jsr % (2**32)
    return jsr
    

def CONG():
    global jcong
    jcong = (69069 * jcong + 1234567) % (2 ** 32)
    return jcong
    

def znew():
    global z
    z = (36969 * (z and 65536) + (z >> 16) )% (2 ** 32)
    return z
    

def wnew():
    global w 
    w = (18000 * (w and 65535) + (w >> 16) )% (2 ** 32)
    return w
    

def MWC():
    return ((znew() << 16) + wnew()) % (2 ** 32)
    

def KISS():
    return (MWC() ^ CONG()) + SHR3() % (2 ** 32)
    

if __name__ == "__main__":
    x = set()
    for i in range(10000):
        x.add(KISS())
    print(len(x))
    

