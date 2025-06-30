# Sleep Apnea and Pulse Oximetry

## 1. Python Package for Preprocess and Extract Features from SpO2 Signals

Package named `sleepdataspo2` is dedicated to download datasets from NSRR and preprocess the SpO2 signal. And extract the features described in `https://oximetry-toolbox.readthedocs.io/en/latest/pobm.obm.html`.

If you need to use the package directly see the section <a href="#requirements">Requirements</a>.

#### Requirements

1. `miniconda` or any other virtual environment with `python 3.8` installed
2. `.env` which contains `NSRR_TOKEN` acqurerd from `sleepdata.org` upon request
3. `cert.pem` which used to verify the identity of the server. Acquired from following steps:
   - Head to `https://github.com/nsrr/nsrr-gem/blob/master/README.md#prerequisites`
   - install ruby and don't follow the instructions in the above page under section `usage`
   - after `gem install nsrr`, you may find `Ruby31\ssl\cert.pem` (in my case `C:\Ruby31\ssl\cert.pem`)

#### How to use:

1.  `git clone https://github.com/EshanJayasundara/Sleep-Apnea-and-Pulse-Oximetry.git`
2.  `cd sleep-project`
3.  `pip install build`
4.  `python -m build`
5.  `pip install dist/sleepdataspo2-0.1.0-py3-none-any.whl`
6.  `cd ../usage`
7.  place `.env` (which contains `NSRR_TOKEN`) and `cert.pem` (which used to verify the identity of the server. Since we only download files we don't need a private key) files into `usage` folder.
8.  Use one of the following:

    **commands**

    ```bash
      python -m sleepdataspo2.process \
             -d <dataset> \
             -p <prefix> \
             -spo2 <spo2_signal_channel_name> \
             -df <download_from> \
             -dt <download_to> \
             -s <start> \
             -e <end> \
             -t <max_threads> \
             -c <complex_features>
    ```

    or

    ```bash
     python -m sleepdataspo2.process \
             -d <dataset> \
             -p <prefix> \
             -spo2 <spo2_signal_channel_name> \
             -df <download_from> \
             -dt <download_to> \
             -l <list> \
             -t <max_threads> \
             -c <complex_features>
    ```

    **Command Line Arguments**

    | Short | Long                  | Type   | Required | Default  | Description                                                            |
    | ----- | --------------------- | ------ | -------- | -------- | ---------------------------------------------------------------------- |
    | `-d`  | `--dataset`           | `str`  | ✅ Yes   | –        | Short name of the dataset in [sleepdata.org](https://sleepdata.org)    |
    | `-p`  | `--prefix`            | `str`  | ✅ Yes   | –        | Prefix before the ID of the EDF file                                   |
    |       | `--spo2_channel_name` | `str`  | ❌ No    | `"SaO2"` | SpO₂ channel name in the EDF file (column name of the signal)          |
    | `-df` | `--download_from`     | `str`  | ✅ Yes   | –        | File path on the NSRR website                                          |
    | `-dt` | `--download_to`       | `str`  | ✅ Yes   | –        | Local path where the files will be downloaded                          |
    | `-s`  | `--start`             | `int`  | ❌ No    | `None`   | Start index for downloading files (used when `--list` is not provided) |
    | `-e`  | `--end`               | `int`  | ❌ No    | `None`   | End index for downloading files (used when `--list` is not provided)   |
    | `-l`  | `--list`              | `str`  | ❌ No    | `None`   | Space-separated list of file IDs to download                           |
    | `-t`  | `--max_threads`       | `int`  | ❌ No    | `5`      | Maximum number of threads for concurrent downloads                     |
    | `-c`  | `--complex_features`  | `bool` | ❌ No    | `False`  | Whether to calculate time-consuming complex features                   |

    **Example Usage:**

    ```bash

    python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 2 -c False

    ```

    or

    ```bash
    python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3 -c False
    ```

#### Folder Structure After Following above Steps

```bash
Sleep-Apnea-and-Pulse-Oximetry
├── LICENSE
├── README.md
├── sleep-project
│   ├── README.md
│   ├── pyproject.toml
│   └── sleepdataspo2               # 📦 Core processing package for sleep data
│       ├── __init__.py
│       ├── clean_features.py       # Cleans raw features
│       ├── constants.py            # Stores global constants
│       ├── download_data.py        # Downloads raw EDF files
│       ├── engineer_features.py    # Creates complex features from signals
│       ├── load_data.py            # Loads datasets into memory
│       ├── plot_graphs.py          # Graphing utilities for visualization
│       ├── process.py              # Main data processing pipeline
│       └── run_pipeline.py         # Entry point to run full pipeline
└── usage
    ├── INSTRUCTIONS.md
    ├── cert.pem
    ├── data                        # 📂 Main dataset storage (raw and processed)
    │   ├── cfs                     # 🧪 Canadian Frailty Study (CFS) dataset
    │   │   ├── images              # 📊 Exported image plots
    │   │   │   ├── cleaned         # Cleaned signal visualizations
    │   │   │   └── original        # Original signal visualizations
    │   │   └── polysomnography     # 📈 Sleep signal data
    │   │       └── edfs            # Raw EDF files
    │   └── shhs                    # 💤 Sleep Heart Health Study (SHHS) dataset
    │       ├── images              # 📊 Exported image plots
    │       │   ├── cleaned         # Cleaned signal visualizations
    │       │   └── original        # Original signal visualizations
    │       └── polysomnography     # 📈 Sleep signal data
    │           └── edfs
    │               └── shhs1       # EDFs for SHHS1 subset
    └── sleep_apnea_detection.ipynb # 📓 Example notebook for full pipeline

```

#### Here’s why only public `cert.pem` is enough:

- The private key belongs only to the server (sleepdata.org) — it stays secret and is used internally to establish secure TLS connections.

- You only needs:

  - Server’s public certificates (to verify the server’s identity).
  - Your authentication token (to prove you have permission).

- All encryption/decryption for the connection happens automatically via TLS.

- You never handle or need the private key yourself.

## 2. Sleep Apnea Detection Using Oximetry-Based Digital Biomarkers and Embedding-Based Learning

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
