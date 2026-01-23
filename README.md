# FMCW Radar Digital Back-End – Python Reference Model

This project focuses on the design and implementation of a **digital back-end (DBE) for an FMCW radar system**.  
The final objective is to build, simulate, and synthesize the digital signal processing chain used for range estimation in FMCW radar.

The current stage of the project implements a **Python reference model** that serves as a golden model for future RTL and hardware implementation.

---

## 🎯 Project Objectives

- Develop a mathematical and digital model of an FMCW radar signal chain
- Build a Python reference implementation for verification
- Later map the algorithm to:
  - RTL design (Verilog/SystemVerilog)
  - Simulation and verification
  - Synthesis / FPGA implementation

---

## 📌 Current Status (Python Modeling Phase)

Implemented so far:
- FMCW radar parameter definition
- Chirp slope derivation
- Baseband FMCW transmit chirp generation
- Time-domain signal modeling

Upcoming steps:
- Target delay modeling
- Mixer (beat signal) generation
- FFT-based range estimation
- ADC sample export
- Noise and multiple target modeling

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

The baseband transmit signal is given by:

\[
s_{tx}(t) = e^{j\pi S t^2}
\]

Target range introduces a round-trip delay:

\[
\tau = \frac{2R}{c}
\]

which leads to a beat frequency after mixing:

\[
f_b = \frac{2SR}{c}
\]

This beat frequency is used to estimate target range using FFT.

---

## 🛠 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

## 🐍 Virtual Environment Setup

It is recommended to use a Python virtual environment.

Create and activate the environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```