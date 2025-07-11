"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import sys
from pobm.prep import set_range, resamp_spo2, median_spo2, block_data,  dfilter
from colorama import Fore, Style

class CleanFeaturesInterface(ABC):
    @abstractmethod
    def clean_single(self, spo2: pd.Series, original_frequency: int) -> pd.Series:
        pass
    
    def dfilter(self, signal, Diff=4):
        """
        Apply Delta Filter to the signal.

        :param signal: 1-d array, of shape (N,) where N is the length of the signal
        :param Diff: parameter of the delta filter.
        :type Diff: int, optional

        :return: preprocessed signal, 1-d numpy array.
        """
        signal_filtered = []
        for i, data in enumerate(signal):
            if i == 0:
                signal_filtered.append(data)
            else:
                if (((signal_filtered[-1] - data) / signal_filtered[-1]) * 100) < Diff:
                    signal_filtered.append(data)
        return np.array(signal_filtered)
    
    def nan_interp(self, signal):
        nans = np.isnan(signal)
        not_nans = ~nans
        signal[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(not_nans), signal[not_nans])
        return signal
    
    def safe_nan_interp(self, x):
        """Interpolate and fill start/end NaNs with nearest values."""
        x = pd.Series(x)
        x_interp = x.interpolate(method='linear', limit_direction='both')
        return x_interp.to_numpy()


class CleanSpO2(CleanFeaturesInterface):
    def __init__(self):
        pass

    def clean_single(self, spo2: pd.Series, original_frequency: int) -> pd.Series:
        # spo2 is a 1D numpy array sampled at {original_frequency} Hz
        print("[✔] original frequency:", original_frequency)
        # Trim the first and last 5 minutes
        raw_spo2 = spo2.truncate(before=5*60*original_frequency, after=spo2.shape[0]-5*60*original_frequency-1)
        # print(f"{spo2.shape[0]} - {2*5*60*original_frequency} = {raw_spo2.shape[0]}")

        light_green = Fore.LIGHTGREEN_EX
        light_red = Fore.LIGHTRED_EX
        reset = Style.RESET_ALL

        raw_spo2 = np.array(raw_spo2.tolist())
        # 1. Remove non-physiological values (<50% or >100%)
        spo2 = set_range(raw_spo2, Range_min=50, Range_max=100)
        print(f"{light_green}[DEBUG]{reset} length after removing non-physiological values: {spo2.shape[0]}")
        # 2. Apply Delta Filter (remove sharp jumps/artifacts)
        # print(f"{light_green}[DEBUG]{reset} SPO2 length: {len(spo2)}")
        spo2 = super().dfilter(spo2, Diff=8)
        print(f"{light_green}[DEBUG]{reset} length after applying delta filter: {spo2.shape[0]}")
        # 3. Smooth with median filter to avoid spikes
        # print(f"{light_green}[DEBUG]{reset} SPO2 length: {len(spo2)}")
        spo2 = median_spo2(spo2, FilterLength=9)
        print(f"{light_green}[DEBUG]{reset} length after smoothing: {spo2.shape[0]}")
        # 4. Remove block artifacts (extended low signal sections)
        spo2 = block_data(spo2, treshold=50)
        print(f"{light_green}[DEBUG]{reset} length after removing block artifacts: {spo2.shape[0]}")
        # 5. Downsample to 1 Hz
        spo2 = resamp_spo2(spo2, OriginalFreq=original_frequency)
        print(f"{light_green}[DEBUG]{reset} length after downsampling: {spo2.shape[0]}")
        # 6. Interpolate to replace NAN
        spo2 = super().safe_nan_interp(spo2)

        spo2_series = pd.Series(spo2)

        # if length is lowr than 4h skip the process
        if spo2_series.shape[0] < 4*60*60:
            print(f"{light_red}[SKIPED]{reset} Skipped due to small length (less than 4 hours) in the spo2 signal")
            sys.exit(0)

        # if length is more than 7h then choose first 7h else pad to 7h
        seven_hours_in_sec = 7*60*60
        target_length = seven_hours_in_sec*1
        if spo2_series.shape[0] > target_length:
            spo2_series = spo2_series.truncate(after=target_length-1)
        elif spo2_series.shape[0] == target_length:
            pass
        else:
            pad_len = target_length - spo2_series.shape[0]
            pad_val = np.nanmean(spo2_series) if not np.isnan(spo2_series).all() else 98
            spo2_series = np.concatenate([spo2_series, pad_val * np.ones(pad_len)])
        print(f"{light_green}[DEBUG]{reset} length after padding: {spo2_series.shape[0]}")

        print(f"[✔] Final signal length (1Hz, {seven_hours_in_sec}): {spo2_series.shape[0]}")

        return spo2_series
    
class CleanFeatures(CleanFeaturesInterface):
    def __init__(self, feature_cleaner: CleanFeaturesInterface):
        self._feature_cleaner = feature_cleaner

    def clean_single(self, spo2: pd.Series, original_frequency: int) -> pd.Series:
        return self._feature_cleaner.clean_single(
                    spo2=spo2,
                    original_frequency=original_frequency
                )