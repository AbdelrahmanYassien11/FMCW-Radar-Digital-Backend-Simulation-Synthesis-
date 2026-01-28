<p align="center">
  <img src="https://img.shields.io/badge/FPGA-6B2B44?style=for-the-badge&logo=FPGA&logoColor=white" />
  <img src="https://img.shields.io/badge/Verilog-AA1745?style=for-the-badge&logo=verilog&logoColor=white" />
  <img src="https://img.shields.io/badge/UVM-FF6A21?style=for-the-badge&logo=uvm&logoColor=white" />
  <img src="https://img.shields.io/badge/SVA-5A47FF?style=for-the-badge&logo=sva&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3B36E9?style=for-the-badge&logo=gnu&logoColor=white" />
</p>

<h1 align="center" style="color:#6B2B44;">🔎 UFMCW Radar Digital Back-End – Python Reference Model 🔎</h1>

This project focuses on the design and implementation of a **digital back-end (DBE) for an FMCW radar system**.  
The final objective is to build, simulate, and and synthesize the digital signal processing chain used for **range estimation** in FMCW radar.

The current stage of the project implements a **Python reference (golden) model** that will later be used as a reference for RTL and hardware implementation.

---

## 🎯 Project Objectives

- Develop a mathematical and digital model of an FMCW radar signal chain  
- Build a Python reference implementation for algorithm verification  
- Model realistic radar effects (noise, ADC quantization, windowing)  
- Perform FFT-based range estimation and peak detection  
- Export ADC samples for future RTL testbench and verification  

Later phases of the project will map the algorithm to:
- RTL design (Verilog/SystemVerilog)  
- Simulation and verification  
- Synthesis / FPGA implementation  

---

## 📌 Current Status (Python Modeling Phase)

Implemented so far:

- FMCW radar parameter definition  
- Chirp slope derivation  
- Baseband FMCW transmit chirp generation  
- Two-target echo modeling with round-trip delay  
- Mixer (beat signal) generation  
- Additive noise modeling  
- ADC quantization (fixed-point model)  
- Windowing (Hann window)  
- FFT-based range estimation  
- Peak detection for multiple targets  
- Export of ADC I/Q samples to file  

Outputs generated:
- Time-domain chirp plots  
- Beat signal plot  
- Range profile plot  
- Range profile with detected peaks  
- `adc_samples.txt` for RTL testbench input  

---

## 📐 Theory Overview

An FMCW radar transmits a linear frequency chirp:

\[
f(t) = f_0 + S t
\]

where:
- \( f_0 \) is the carrier frequency  
- \( S = \frac{B}{T_{chirp}} \) is the chirp slope  
- \( B \) is bandwidth  
- \( T_{chirp} \) is chirp duration  

The baseband transmit signal is:

\[
s_{tx}(t) = e^{j\pi S t^2}
\]

A target at range \( R \) introduces a round-trip delay:

\[
\tau = \frac{2R}{c}
\]

After mixing the transmitted and received signals, a beat frequency is produced:

\[
f_b = \frac{2SR}{c}
\]

This beat frequency is proportional to the target range and is extracted using an FFT:

\[
R = \frac{c}{2S} f_b
\]

Multiple targets produce multiple beat frequencies, resulting in multiple peaks in the FFT-based range profile.

---

## 🔁 Signal Processing Chain (Current Implementation)

The current Python model implements the following pipeline:

TX Chirp Generation
↓
Target Echo Modeling (Two Targets + Delay)
↓
Mixer (Beat Signal)
↓
Add Noise
↓
ADC Quantization (12-bit model)
↓
Windowing (Hann window)
↓
FFT (Range Estimation)
↓
Peak Detection
↓
Export ADC Samples


This pipeline closely matches a real FMCW radar digital back-end.

---

## 🛠 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

🐍 Virtual Environment Setup

It is recommended to use a Python virtual environment.

Create and activate the environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

▶️ How to Run
python fmcw_model.py

# This will generate:

Plots in the project directory
adc_samples.txt containing quantized I/Q samples

# 📂 Generated Files

tx_chirp_time.png

tx_chirp_frequency.png

beat_signal_time.png

range_profile_two_targets.png

range_profile_peaks.png

adc_samples.txt

# 🚀 Future Work

Planned next stages of the project include:

Fixed-point optimization and bit-width analysis

CFAR detection

Doppler processing (2D FFT)

RTL implementation of mixer, FFT, and peak detector

Verification against Python golden model

FPGA synthesis and timing analysis

# 📖 Notes

This Python model serves as a golden reference for the FMCW radar digital back-end and will be used for:

Algorithm validation

RTL verification

Hardware testing

# Block Level Diagram
==================== FMCW Radar Digital Back-End ====================

        ┌───────────────┐
        │  Chirp Signal │
        │   Generator   │
        └───────┬───────┘
                │ Tx Chirp
                ▼
        ┌───────────────┐
        │   Target &    │
        │ Channel Model │
        │ (Delay + Att) │
        └───────┬───────┘
                │ Rx Signal
                ▼
        ┌───────────────┐
        │   Mixer /     │
        │ Dechirping    │
        └───────┬───────┘
                │ IF Signal
                ▼
        ┌───────────────┐
        │   Low-Pass    │
        │    Filter     │
        └───────┬───────┘
                │ Beat Signal
                ▼
        ┌───────────────┐
        │      ADC      │
        │ (Sampling &   │
        │ Quantization) │
        └───────┬───────┘
                │ Digital Samples
                ▼
        ┌───────────────┐
        │     Window    │
        │  (Hann/Hamming│
        │    or Blackman│
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │      FFT      │
        │  (Range FFT)  │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │  Magnitude &  │
        │ Power Spectrum│
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Peak Detection│
        │ & Range Est.  │
        └───────────────┘

=====================Digital blocks to be implemented in RTL (a first look, ignoring cdc..etc)=========================


```
                ┌──────────────────┐
ADC I/Q  ──────▶│      Mixer       │─────▶ Beat Signal (I/Q)
                └──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │   Window Block   │
                └──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │     FFT Block    │
                └──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │   Magnitude      │
                │   Calculation    │
                └──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │  Peak Detector   │
                └──────────────────┘
                          │
                          ▼
                Range Estimate (meters)
```
=================================================================
