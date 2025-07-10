# Sleep Apnea and Pulse Oximetry

## 1. Python Package for Downloading NARR Datasets, Preprocessing, and Extracting Features from SpO2 Signals

Package named `sleepdataspo2` is dedicated to download datasets from NSRR and preprocess the SpO2 signal. And extract the features described [here](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-40604-3/MediaObjects/41467_2023_40604_MOESM1_ESM.pdf).

If you need to use the package directly see the section <a href="#requirements">Requirements</a>.

#### What `sleepdataspo2` does?

1. Download the `.edf` files from sleepdata.org (NSRR)
2. Drop non-psysiological values (below 50 and above 100)
3. Remove sharp jumps (8% quick drop or rise)
4. Smooth with median filter with window = ($spo2[i] = median(spo2[i-int(\frac{9}{2}): i+int(\frac{9}{2})+1])$)
5. Remove block artifacts (extended periods of invalid, flat, or low-quality signal, often due to sensor issues rather than true physiological events)
6. Downsample to 1Hz
7. Replace NAN by interpolating
8. Saves the cleaned SpO2 signals for later use (with the images of originaland and cleaned signals)
9. Extract the features described [here](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-40604-3/MediaObjects/41467_2023_40604_MOESM1_ESM.pdf) just before last 2-3 pages and save it
10. All happens in properely managed `multithreaded` environment to maximize the parallelism

#### Requirements

1. `miniconda` or any other virtual environment with `python 3.8` installed
2. `.env` which contains `NSRR_TOKEN` acqurerd from `sleepdata.org` upon request

#### How to use:

1.  `git clone https://github.com/EshanJayasundara/Sleep-Apnea-and-Pulse-Oximetry.git`
2.  `cd sleep-project`
3.  `pip install build`
4.  `python -m build`
5.  `pip install dist/sleepdataspo2-0.1.0-py3-none-any.whl`
6.  `cd ../usage`
7.  place `.env` (which contains `NSRR_TOKEN`) file into `usage` folder.
8.  Refer the following instructions:

    **Command Line Arguments**

    | Short   | Long                  | Type   | Required | Default  | Description                                                            |
    | ------- | --------------------- | ------ | -------- | -------- | ---------------------------------------------------------------------- |
    | `-d`    | `--dataset`           | `str`  | ✅ Yes   | –        | Short name of the dataset in [sleepdata.org](https://sleepdata.org)    |
    | `-p`    | `--prefix`            | `str`  | ✅ Yes   | –        | Prefix before the ID of the EDF file                                   |
    | `-spo2` | `--spo2_channel_name` | `str`  | ❌ No    | `"SaO2"` | SpO₂ channel name in the EDF file (column name of the signal)          |
    | `-df`   | `--download_from`     | `str`  | ✅ Yes   | –        | File path on the NSRR website                                          |
    | `-dt`   | `--download_to`       | `str`  | ✅ Yes   | –        | Local path where the files will be downloaded                          |
    | `-s`    | `--start`             | `int`  | ❌ No    | `None`   | Start index for downloading files (used when `--list` is not provided) |
    | `-e`    | `--end`               | `int`  | ❌ No    | `None`   | End index for downloading files (used when `--list` is not provided)   |
    | `-l`    | `--list`              | `str`  | ❌ No    | `None`   | Space-separated list of file IDs to download                           |
    | `-t`    | `--max_threads`       | `int`  | ❌ No    | `5`      | Maximum number of threads for concurrent downloads                     |
    | `-c`    | `--complex_features`  | `bool` | ❌ No    | `False`  | Whether to calculate time-consuming complex features                   |

    - Use `-s` and `-e` when you have to run in consecutive order.
    - Otherwise use `-l`.

    **commands to run entire pipeline**

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
             -l "<subject_id_1> <subject_id_2>" \
             -t <max_threads> \
             -c <complex_features>
    ```

    **commands to run each step seperately**

    1. Download

       ```bash
       python -m sleepdataspo2.download \
               -d <dataset> \
               -p <prefix> \
               -df "<download_from>" \
               -dt <download_to> \
               -l "<subject_id_1> <subject_id_2>" \
               -t <max_threads>
       ```

       or

       ```bash
       python -m sleepdataspo2.download \
               -d <dataset> \
               -p <prefix> \
               -df "<download_from>" \
               -dt <download_to> \
               -s <start_index> \
               -e <end_index> \
               -t <max_threads>
       ```

    2. Clean

       ```bash
       python -m sleepdataspo2.clean \
               -d <dataset> \
               -p <prefix> \
               -spo2 <spo2_channel_name> \
               -df "<download_from>" \
               -dt <download_to> \
               -l "<subject_id_1> <subject_id_2>" \
               -t <max_threads>
       ```

       or

       ```bash
       python -m sleepdataspo2.clean \
               -d <dataset> \
               -p <prefix> \
               -spo2 <spo2_channel_name> \
               -df "<download_from>" \
               -dt <download_to> \
               -s <start_index> \
               -e <end_index> \
               -t <max_threads>
       ```

    3. Flush

       ```bash
       python -m sleepdataspo2.flush \
               -d <dataset> \
               -p <prefix> \
               -df "<download_from>" \
               -dt <download_to> \
               -l "<subject_id_1> <subject_id_2>" \
               -t <max_threads>
       ```

       or

       ```bash
       python -m sleepdataspo2.flush \
               -d <dataset> \
               -p <prefix> \
               -df "<download_from>" \
               -dt <download_to> \
               -s <start_index> \
               -e <end_index> \
               -t <max_threads>
       ```

    4. Enginer

       ```bash
       python -m sleepdataspo2.engineer \
               -d <dataset> \
               -p <prefix> \
               -spo2 <spo2_channel_name> \
               -df "<download_from>" \
               -dt <download_to> \
               -l "<subject_id_1> <subject_id_2>" \
               -t <max_threads> \
               -c <complex_features>
       ```

       or

       ```bash
       python -m sleepdataspo2.engineer \
               -d <dataset> \
               -p <prefix> \
               -spo2 <spo2_channel_name> \
               -df "<download_from>" \
               -dt <download_to> \
               -s <start_index> \
               -e <end_index> \
               -t <max_threads> \
               -c <complex_features>
       ```

    **Example Usage: all at once**

    1. With `-s` and `-e`

       ```bash
       python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 2
       ```

    2. Or with `-l`

       ```bash
       python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3
       ```

    **Example Usage: one by one**

    1. With `-s` and `-e`

       ```bash
       python -m sleepdataspo2.download -d shhs -p shhs1 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 5
       ```

       ```bash
       python -m sleepdataspo2.clean -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 5
       ```

       ```bash
       python -m sleepdataspo2.flush -d shhs -p shhs1 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 5
       ```

       ```bash
       python -m sleepdataspo2.engineer -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 5
       ```

    2. Or with `-l`

       ```bash
       python -m sleepdataspo2.download -d shhs -p shhs1 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3
       ```

       ```bash
       python -m sleepdataspo2.clean -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3
       ```

       ```bash
       python -m sleepdataspo2.flush -d shhs -p shhs1 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3
       ```

       ```bash
       python -m sleepdataspo2.engineer -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3
       ```

#### Folder Structure Inside `usage` Directory After Following above Steps

```bash
Sleep-Apnea-and-Pulse-Oximetry
├── LICENSE
├── README.md
├── sleep-project
└── usage
    ├── INSTRUCTIONS.md
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
