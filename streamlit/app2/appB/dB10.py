from numpy import log10


def dB10(x):
    y = 10*log10(abs(x))

    return y
