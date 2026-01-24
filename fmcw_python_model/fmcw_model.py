import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Physical constant
# -------------------------
c = 3e8  # speed of light (m/s)

# -------------------------
# FMCW parameters
# -------------------------
B = 150e6        # 150 MHz Bandwidth (Hz)
T_chirp = 50e-6  # 50 microseconds Chirp duration (seconds)
Fs = 10e6        # 10 MHz Sampling rate (Hz) to satisfy Nyquist condition for beat frequency
                 # fb < Fs/2, fb = 2SR/c ≈ 2 MHz, Fs > 4 MHz

# Range Resolution = Delta R = c / (2B) = 1 Meter
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

# -------------------------
# Step 2: TX FMCW Chirp
# -------------------------

# Phase of the chirp
tx_phase = 2 * np.pi * (0.5 * S * t**2)

# Complex baseband transmit signal
tx_signal = np.exp(1j * tx_phase)

# Plot real part of TX signal (time domain)
plt.figure()
plt.plot(t[:500], np.real(tx_signal[:500]))
plt.title("FMCW TX Chirp (Real Part - Time Domain)")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid()
plt.savefig("tx_chirp_time.png")
plt.close()

# Instantaneous frequency
f_inst = S * t

plt.figure()
plt.plot(t, f_inst)
plt.title("Instantaneous Frequency of FMCW Chirp")
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency (Hz)")
plt.grid()
plt.savefig("tx_chirp_frequency.png")
plt.close()


# -------------------------
# Step 3: RX FMCW, Target + Delay
# -------------------------

# -------------------------
# Step 3: Two Targets + Delay
# -------------------------

# Target parameters
R1 = 30.0   # meters
A1 = 1.0

R2 = 70.0   # meters
A2 = 0.6

# Delays
tau1 = 2 * R1 / c
tau2 = 2 * R2 / c

# Delayed time axes
t1 = t - tau1
t2 = t - tau2

# RX signals from each target
rx1_phase = 2 * np.pi * (0.5 * S * t1**2)
rx2_phase = 2 * np.pi * (0.5 * S * t2**2)

rx1 = A1 * np.exp(1j * rx1_phase)
rx2 = A2 * np.exp(1j * rx2_phase)

# Total received signal (sum of echoes)
rx_signal = rx1 + rx2

# Plot TX and RX signals (real part)
plt.figure()
plt.plot(t[:500], np.real(tx_signal[:500]), label="TX signal")
plt.plot(t[:500], np.real(rx_signal[:500]), label="RX signal (delayed)")
plt.title("TX and RX FMCW Chirps (Time Domain)")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.savefig("tx_rx_chirp_time.png")
plt.close()


# -------------------------
# Step 4: Mixer (Beat Signal)
# -------------------------

# Mixer: TX multiplied by conjugate of RX
beat_signal = tx_signal * np.conj(rx_signal)

# Plot beat signal (real part)
plt.figure()
plt.plot(t[:500], np.real(beat_signal[:500]))
plt.title("Beat Signal (Real Part - Time Domain)")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid()
plt.savefig("beat_signal_time.png")
plt.close()


# -------------------------
# Step 5: Add Noise
# -------------------------
noise_std = 0.05  # noise strength
noise = noise_std * (np.random.randn(N) + 1j*np.random.randn(N))

beat_signal_noisy = beat_signal + noise


# -------------------------
# Step 6: Quantization (ADC model)
# -------------------------
bits = 12
max_val = 2**(bits-1) - 1

I = np.real(beat_signal_noisy)
Q = np.imag(beat_signal_noisy)

I_q = np.round(I * max_val) / max_val
Q_q = np.round(Q * max_val) / max_val

beat_quantized = I_q + 1j * Q_q


# -------------------------
# Step 7: Windowing (DSP stage)
# -------------------------
window = np.hanning(N)
processed_signal = beat_quantized * window


# -------------------------
# Step 8: FFT and Range Estimation
# -------------------------

# FFT of beat signal
fft_out = np.fft.fft(processed_signal)

# Take magnitude (absolute value)
fft_mag = np.abs(fft_out)

# Use only positive frequencies (first half)
fft_mag = fft_mag[:N//2]

# Frequency axis // Extract the frequencies according to the computed N, using N & the distance between each sampling
freqs = np.fft.fftfreq(N, d=1/Fs)
freqs = freqs[:N//2]

# Convert frequency axis to range axis
ranges = (c / (2 * S)) * freqs

plt.figure()
plt.plot(ranges, fft_mag)
plt.title("Range Profile (Two Targets)")
plt.xlabel("Range (meters)")
plt.ylabel("Magnitude")
plt.grid()
plt.savefig("range_profile_two_targets.png")
plt.close()


# -------------------------
# Step 9: Peak Detection
# -------------------------

# Find indices of the two largest peaks
peak_indices = np.argsort(fft_mag)[-2:]  # get two highest peaks
peak_indices = np.sort(peak_indices)

# Corresponding ranges
estimated_ranges = ranges[peak_indices]
peak_values = fft_mag[peak_indices]

print("Detected peak indices:", peak_indices)
print("Estimated target ranges (meters):", estimated_ranges)
print("Peak magnitudes:", peak_values)

plt.figure()
plt.plot(ranges, fft_mag, label="Range profile")
plt.plot(estimated_ranges, peak_values, "ro", label="Detected peaks")
plt.title("Range Profile with Detected Targets")
plt.xlabel("Range (meters)")
plt.ylabel("Magnitude")
plt.legend()
plt.grid()
plt.savefig("range_profile_peaks.png")
plt.close()


# -------------------------
# Step 10: Export ADC Samples
# -------------------------

# Stack I and Q samples into two columns
adc_samples = np.column_stack((np.real(beat_quantized), np.imag(beat_quantized)))

# Save to text file
np.savetxt("adc_samples.txt", adc_samples, fmt="%.6f")

print("ADC samples exported to adc_samples.txt")
