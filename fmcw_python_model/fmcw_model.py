import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Physical constant
# -------------------------
c = 3e8  # speed of light (m/s)

# -------------------------
# FMCW parameters
# -------------------------
B = 150e6        # 150MHZ Bandwidth (Hz)
T_chirp = 50e-6  # 50*(10^-6) Chirp duration (seconds)
Fs = 10e6        # 10^6 MHZ Sampling rate (Hz) to satisfy nyquist constant for beat freqency i.e. 
                 # fb < fs/2, fb = 2SR/C, fb = 2 MHz, Fs has to be > 4 MHz

# Range Resolution = Delta R = C/2B = 1 Meter

# Slope = B / Tchirp = 3*10^12 Hz/s

# -------------------------
# Derived parameters
# -------------------------
S = B / T_chirp              # Chirp slope (Hz/s)
N = int(T_chirp * Fs)        # Number of samples
t = np.arange(N) / Fs        # Time vector (seconds)

# Debug prints
print("Chirp slope S =", S, "Hz/s")
print("Number of samples N =", N)
print("First 5 time samples:", t[:5])
