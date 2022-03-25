from math import pi
import math
import numpy as np
from scipy.signal import lfilter
import TskinDSP as tskin

def SIBIF_output_Journal_Z_Scores(Q1, Q2, Q3, gain, acc, fWeibel, Hsub1, Zsub2):
    w = 2*pi*fWeibel #rad/s
    acc = acc*gain
    Tskin_sym_smooth, Tskin_sym_smooth_inv, tskin_sym_smooth_inv = tskin.TskinDSP(Q1, Q2, Q3, w, Hsub1, Zsub2)

    gvv_acc = lfilter(tskin_sym_smooth_inv,1,np.concatenate((acc,np.zeros(len(tskin_sym_smooth_inv))), axis=None))

    gvv_acc = gvv_acc[math.floor(len(tskin_sym_smooth_inv)/2):math.floor(len(gvv_acc)-len(tskin_sym_smooth_inv)/2)]

    return gvv_acc
