## Python Package for Preprocess and Extract Features from SpO2 Signals

Package named `sleepdataspo2` is dedicated to download datasets from NSRR and preprocess the SpO2 signal. And extract the features described in `https://oximetry-toolbox.readthedocs.io/en/latest/pobm.obm.html`.

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

    python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -s 200001 -e 200005 -t 2

    ```

    or

    ```bash
    python -m sleepdataspo2.process -d shhs -p shhs1 -spo2 SaO2 -df "polysomnography/edfs/shhs1" -dt data -l "200001 200003 200007" -t 3
    ```
