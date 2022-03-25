# features.py
import numpy as np
import scipy as sp
import math
from sklearn.preprocessing import normalize
from acoustics.cepstrum import real_cepstrum, minimum_phase
from sklearn.linear_model import HuberRegressor, LinearRegression
from scipy import signal


def f0_PSD_pwelch(x, fs):
    """Entrega f0 y la PSD de la sennal x, con una frecuencia de muestreo fs

    Args:
        x (numpy array): Arreglo de numeros flotantes
        fs (int): frecuencia de muestreo

    Returns:
        [float, array]:
    """

    Welch_window = len(x) / 2 / fs * 1000
    win_len = int(Welch_window / 1000 * fs)
    ww = signal.get_window('hann', win_len, False)  # signal.get_window('hann', int(len(x)/10), False)
    f, pxx = signal.welch(x - np.mean(x), fs=fs, window=ww, noverlap=0, nfft=max(len(x), 2 ** 10), return_onesided=True,
                          scaling='spectrum')

    # Calculo de la frecuencia fundamental (f0) de la ventana
    psd = PSD(pxx)
    f = np.linspace(0, fs // 2, len(psd))
    f0 = f[np.argmax(psd)]

    return [f0, psd]


def harm(PSD, fs, f0, f):
    """Obtiene los harmonicos de la sennal a partir de la PSD de esta.

    Args:
        PSD ([numpy array]): PSD de una sennal.
        fs (float): Frecuencia de muestreo de la sennal
        f0 (float): Frecuencia fundamental de la sennal
        f ([numpy array]): No entiendo bien que es :c

    Returns:
        List : Lista con los harmonicos de la sennal (creo?)
    """
    BW = f0 * 0.3
    HARM = np.array([])
    for k in np.arange(f0, (fs / 2), f0):
        rang = np.where((f > (k - BW)) & (f < (k + BW)))
        HARM = np.append(HARM, np.max(PSD[rang]))
    return HARM


def PSD(pxx):
    """Entrega la PSD a partir de una de las salidas de pwelch.

    Args:
        pxx (array): Una de las salidas que entrega pwelch

    Returns:
        array: Arreglo con la PSD obtenida a partir de pxx
    """
    return 10 * np.log10(np.abs(pxx) / np.max(np.abs(pxx)))


def hrf(harm_arr):
    """Entrega el valor HRF a partir del arreglo con los harmonicos.

    Args:
        harm_arr (numpy array): Arreglo con los harmonicos. (Se obtiene a partir de harm)

    Returns:
        [float]: Valor HRF de la sennal.
    """
    return 10 * np.log10(np.sum(10 ** (harm_arr[1:] / 10)))


def h1h2_hrf(psd, fs, f0):
    """Entrega dos caracteristicas de la sennal a partir de pxx (una de las salidas de pwelch)

    Args:
        pxx (array): Salida de pwelch.
        fs (float): Frecuencia de muestreo de la sennal.
        f0 (float): Frecuencia fundamental de la sennal.

    Returns:
        [type]: [description]
    """
    # pxx se obtiene de pwelch
    PSD1 = psd
    f = np.linspace(0, fs / 2, len(PSD1))
    harm_arr = harm(PSD1, fs, f0, f)
    H1H2 = -harm_arr[1]
    HRF = hrf(harm_arr)
    return [H1H2, HRF]


def ac_flow(x, n0):
    """
    Calcula AC Flow de una ventana
    x : ventana
    n0 : f0 / fs (frecuencia fundamental / frecuencia de muestreo)
    """
    return np.max(x) - np.min(x)


def mfdr(dx, n0):
    """[summary]

    Args:
        dx ([numpy array]): [Derivada ]
        n0 ([type]): [description]

    Returns:
        [type]: [description]
    """
    return -np.min(dx)


def rms(x):
    """ Calcula el valor RMS utilizando todos los valores del arreglo x

    Args:
        x ([array]): [Arreglo de numeros int o float de una dimension]

    Returns:
        [float]: [Valor RMS calculado.]
    """

    return np.sqrt(np.mean(x ** 2))


def SPL(rms_x):
    """Calcula el valor SPL de un numero.

    Args:
        rms_x ([float]): Un valor flotante. En este caso el valor rms de x.

    Returns:
        [float]: SPL de el numero de entrada.
    """
    return 20 * np.log10(rms_x)


def HP_filter(x, fs, varargin=None):
    """Filtro pasa altos aplicado a la sennal x. Por defecto la frecuencia de corte es 80hz y el filtro es de orden 6.

    Args:
        x (numpy array): Un arreglo de numpy.
        fs (float): Frecuencia de muestreo de la sennal.
        varargin ([arreglo de 2 elementos], optional): Permite entregar la frecuencia de corte en el primer elemento
                                            y el orden del filtro en el segundo elemento. Defaults to None.

    Returns:
        [numpy array]: Entrega la sennal x pasada por un filtro pasa altos y luego por un filtro de fase 0.
    """
    if varargin != None:
        fc = varargin[0]
        order = varargin[1]
    else:
        fc = 60
        order = 6
    Wn = 2 * fc / fs
    [b, a] = sp.signal.butter(order, Wn, btype='highpass')
    return sp.signal.filtfilt(b, a, x, padlen=3 * (max(len(b), len(a)) - 1))


def CPP_HillmanUpdate(x, fs, f0, w):
    """No se bien que es esto :(

    Args:
        x (numpy array): Arreglo numpy con una sennal.
        fs (float): Frecuencia de muestreo de la sennal x.
        f0 (float): Frecuencia fundamental de la sennal x.
        w (numpy array): Ventana de hanning con el largo de la sennal. (np.hanning(len(x)))

    Returns:
        float: No se que es :(
    """
    try:
        if np.isnan(f0):
            n = np.array(range(round(fs / 400) - 1, round(fs / 100)))
        else:
            n = range(round(fs / f0) - 10 - 1, round(fs / f0) + 10)
        hp_filt = HP_filter(x, fs)
        normalized_vector = hp_filt / np.max(np.abs(hp_filt))  # sp.stats.zscore(hp_filt, ddof=1)
        c = real_cepstrum(w * normalized_vector)
        c = c[0:len(c) // 2]
        dBc = 20 * np.log10(np.abs(c))
        maxdBc = max(dBc[n])
        maxIndexdBc = np.argmax(dBc[n])
        index = n[0]
        n = np.array(range(n[0], len(dBc)))
        n = np.reshape(n, [-1, 1])
        huber = HuberRegressor().fit(n, dBc[index:])
        Cpp = maxdBc - (huber.coef_[0] * (maxIndexdBc + 1) + huber.intercept_)
    except:
        Cpp = 0

    return Cpp


def ac_mf_sq_oq(x, fs, f0):
    """ Funcion utilizada para calcular 4 parametros de la ventana x.
    AC Flow, MFDR, SQ y OQ.

    Args:
        x (numpy array): Sennal a la que se le calculan estos parametros.
        fs (float): Frecuencia de muestreo de x.
        f0 (float): Frecuencia fundamental de x.

    Returns:
        numpy array: Arreglo con 4 caracteristicas de la senal. [AC_Flow, MFDR, SQ, OQ]
    """
    m = 0
    n0 = fs / f0
    n0 = round(n0)
    ac_flow_arr = np.array([])
    sq_arr = np.array([])
    oq_arr = np.array([])
    mfdr_arr = np.array([])
    dx = np.append(np.diff(x) * fs, 0)
    for k in range(0, len(x) - n0 - 1, n0):
        local_x = x[round(k): round(k + n0 + 1)]
        local_dx = dx[round(k): round(k + n0 + 1)]
        # Get AC Flow and MFDR
        ac_flow_arr = np.append(ac_flow_arr, ac_flow(local_x, n0))  # ac_flow local
        mfdr_arr = np.append(mfdr_arr, mfdr(local_dx, n0))  # mfdr local

        # Get SQ and OQ
        n_max_local = np.argmax(local_x)
        n_max = int(n_max_local + np.floor(k))
        n_in = n_max
        n_out = n_max

        threshold = 0.5 * ac_flow_arr[m]  # %50% decay to find initial baseline
        while (x[n_out] > x[n_max] - threshold) and (n_out < len(x) - 1):
            n_out = n_out + 1
        while (x[n_in] > x[n_max] - threshold) and (n_in > 0):
            n_in = n_in - 1

        # Linear regression to extend the range
        xL = [n_in + 1, n_max + 1]
        xR = [n_max + 1, n_out + 1]
        yL = [x[n_in], x[n_max]]
        yR = [x[n_max], x[n_out]]
        pL = np.polyfit(xL, yL, 1)
        pR = np.polyfit(xR, yR, 1)
        mL = pL[0]
        nL = pL[1]
        mR = pR[0]
        nR = pR[1]
        n_in_star = round((x[n_max] - 0.95 * ac_flow_arr[m] - nL) / mL)
        n_out_star = round((x[n_max] - 0.95 * ac_flow_arr[m] - nR) / mR)

        n_in = n_in_star
        n_out = n_out_star

        # SQ and OQ definitions
        sq_arr = np.append(sq_arr, 100 * (n_max + 1 - n_in) / (n_out - (n_max + 1)))
        oq_arr = np.append(oq_arr, 100 * (n_out - n_in) / n0)
        m = m + 1
    return [np.nanmean(ac_flow_arr), np.nanmean(mfdr_arr), np.nanmean(sq_arr[2:-2]), np.nanmean(oq_arr[2: -2])]
