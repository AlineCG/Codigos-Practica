from math import pi
import math
import numpy as np
import dB10
from scipy.fft import fft, fftshift, irfft

def TskinDSP(Q1, Q2, Q3, w, Hsub1, Zsub2):

    Rm = 2320*Q1
    Mm = 2.4*Q2
    Km = 491e3*Q3

    Sacc = pi*(2.3/2)**2 #accel surface
    Macc = 1.1/Sacc #accel mass per unit area
    Zrad = 1j*w*Macc #put loading in l/cm^4 unit
    Zskin = Rm + 1j*(w*Mm - Km/w) + Zrad
    Tdiff = 1j*w

    Tskin0 = -(Hsub1*Zsub2/(Zsub2*1+Zskin))*Tdiff

    len(Tskin0)
    delay=0
    Tskin0 = Tskin0*np.exp(-delay*1j * w / (2 * w[-1]))
    Tskin = Tskin0

    Tskin0 = np.concatenate((Tskin0,np.flip(Tskin0.conjugate())))


    smoothDC = "on"
    if smoothDC == "on":
        fSmooth = 80 #in Hz
        w_0dB = 2*pi*fSmooth
        fade = (abs(Tskin[np.nonzero(w<=w_0dB)])<1).nonzero()

        fade = round(fade[0][-1])
        win = np.kaiser(fade*2,8)

        abs_Tskin = 10**(dB10.dB10(Tskin[0:fade])*win[0:fade].conj().transpose()/10)
        Tskin[0:fade] = abs_Tskin*np.exp(1j*np.angle(Tskin[0:fade]))

        Tskin_sym_smooth = np.concatenate((Tskin,np.flip(Tskin.conjugate())))
    else:
        Tskin_sym_smooth = np.concatenate((Tskin,np.flip(Tskin.conjugate())))
        print("Warning: Tskin is not smooth to DC")

    Tskin_sym_smooth_inv = 1/Tskin_sym_smooth

    tskin_sym_smooth_inv = irfft(Tskin_sym_smooth_inv[0:len(w)+1])
    tskin_sym_smooth_inv = fftshift(tskin_sym_smooth_inv)

    Tskin_sym_smooth_inv = fft(tskin_sym_smooth_inv)


    return Tskin_sym_smooth, Tskin_sym_smooth_inv, tskin_sym_smooth_inv
