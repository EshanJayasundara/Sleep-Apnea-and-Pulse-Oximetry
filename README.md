# Sleep Apnea and Pulse Oximetry

## Sleep Apnea Detection Using Oximetry-Based Digital Biomarkers and Embedding-Based Learning

This project focuses on automated detection of sleep apnea using only oximetry-derived data, eliminating the need for full polysomnography (PSG). By leveraging Oxygen Desaturation Index (ODI) and Oximetry-Based Digital Biomarkers (OBMs), the system extracts clinically relevant features from overnight SpO₂ signals.

We further propose a novel deep learning framework based on learned embeddings to enhance classification performance, with the goal of identifying sleep apnea events from minimal, non-invasive sensor input.

## What We Use

- #### ODI Model:

  A classical metric that measures the frequency of oxygen desaturations (e.g., 3% drop lasting at least 10 seconds), used as a baseline diagnostic indicator.

- #### OBM Model:

  A feature-rich model built using digital biomarkers that quantify desaturation patterns, hypoxic burden, signal complexity, periodicity, and statistical properties of SpO₂.

- #### Embedding-Based Model (Proposed):
  A new deep learning architecture that encodes temporal oximetry patterns into dense representations for robust apnea classification.

## Goals

- Demonstrate that oximetry alone can be sufficient for reliable sleep apnea screening.
- Compare traditional ODI and engineered OBM models against deep learning approaches.
- Provide a clean, reproducible pipeline for signal cleaning, feature engineering, and model evaluation.

## Tech Stack

- `Python`, `NumPy`, `Pandas`, `Matplotlib`, `Seaborn`
- `MNE` for EDF loading
- `POBM` for digital oximetry biomarkers
- `Scikit-learn` / `CatBoost` for traditional models
- `PyTorch` or `TensorFlow` (optional) for embedding-based model

## Usage

#### How to use:

1. `git clone <repo>`
2. `cd sleep-project`
3. `pip install build`
4. `python -m build`
5. `pip install dist/sleepdataspo2-0.1.0-py3-none-any.whl`
6. `cd ../usage`
7. place `.env` (which contains `NSRR_TOKEN`) and `cert.pem` (which used to verify the identity of the server. Since we only download files we don't need a private key) files into `usage` folder.
8. `python -m sleepdataspo2.download_shhs -d shhs1 -s 200028 -e 200030` or `python -m sleepdataspo2.download_shhs -d shhs1 -l "200315 200317 200313"`

#### Here’s why only public `cert.pem` is enough:

- The private key belongs only to the server (sleepdata.org) — it stays secret and is used internally to establish secure TLS connections.

- You only needs:

  - Server’s public certificates (to verify the server’s identity).
  - Your authentication token (to prove you have permission).

- All encryption/decryption for the connection happens automatically via TLS.

- You never handle or need the private key yourself.

---

## Please refer the instructions in below URL:

https://projects.ce.pdn.ac.lk/docs/how-to-add-a-project
