import numpy as np


def spl(windows, dB_max):
    voices = []
    for window in windows:
        spl1 = 20 * np.log10(np.sqrt(np.mean(np.square(window[0:len(window) // 2]))))
        spl2 = 20 * np.log10(np.sqrt(np.mean(np.square(window[len(window) // 2:-1]))))

        if spl1<dB_max or spl2<dB_max:
            voice = False
        else:
            voice = True

        voices = np.append(voices,voice)

    return voices
