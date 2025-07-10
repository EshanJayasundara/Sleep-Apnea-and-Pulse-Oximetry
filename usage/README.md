## Sleep Apnea Detection Using Oximetry-Based Digital Biomarkers and Embedding-Based Learning

This project focuses on automated detection of sleep apnea using only oximetry-derived data, eliminating the need for full polysomnography (PSG). By leveraging Oxygen Desaturation Index (ODI) and Oximetry-Based Digital Biomarkers (OBMs), the system extracts clinically relevant features from overnight SpO₂ signals.

We further propose a novel deep learning framework based on learned embeddings to enhance classification performance, with the goal of identifying sleep apnea events from minimal, non-invasive sensor input.

#### What We Use

- **ODI Model**:

  A classical metric that measures the frequency of oxygen desaturations (e.g., 3% drop lasting at least 10 seconds), used as a baseline diagnostic indicator.

- **OBM Model**:

  A feature-rich model built using digital biomarkers that quantify desaturation patterns, hypoxic burden, signal complexity, periodicity, and statistical properties of SpO₂.

- **Embedding-Based Model (Proposed)**:

  A new deep learning architecture that encodes temporal oximetry patterns into dense representations for robust apnea classification.

#### Goals

- Demonstrate that oximetry alone can be sufficient for reliable sleep apnea screening.
- Compare traditional ODI and engineered OBM models against deep learning approaches.
- Provide a clean, reproducible pipeline for signal cleaning, feature engineering, and model evaluation.

#### Tech Stack

- `Python`, `NumPy`, `Pandas`, `Matplotlib`, `Seaborn`
- `MNE` for EDF loading
- `POBM` for digital oximetry biomarkers
- `Scikit-learn` / `CatBoost` for traditional models
- `PyTorch` or `TensorFlow` (optional) for embedding-based model

$env:http_proxy = "socks5://127.0.0.1:7999"
$env:https_proxy = "socks5://127.0.0.1:7999"
