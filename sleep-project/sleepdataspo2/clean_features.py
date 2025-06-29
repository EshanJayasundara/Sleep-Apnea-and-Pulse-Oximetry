"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from pobm.prep import set_range, resamp_spo2, median_spo2, block_data

class CleanFeaturesInterface(ABC):
    @abstractmethod
    def clean_single(self, spo2: pd.Series, original_frequency: int) -> pd.Series:
        pass
    def dfilter(self, signal, Diff=4):
        signal = np.array(signal)
        clean = signal.copy()

        diffs = np.abs(np.diff(signal))

        for i in range(1, len(signal)):
            if diffs[i - 1] > Diff:
                clean[i] = (clean[i - 1] + clean[i]) / 2

        return clean

class CleanSpO2(CleanFeaturesInterface):
    def __init__(self):
        pass

    def clean_single(self, spo2: pd.Series, original_frequency: int) -> pd.Series:
        # Trim the first and last 5 minutes
        raw_spo2 = spo2.truncate(before=5*60*original_frequency, after=spo2.shape[0]-5*60*original_frequency-1)
        print(f"{spo2.shape[0]} - {2*5*60*original_frequency} = {raw_spo2.shape[0]}")
        # if length is more than 7h then choose first 7h
        target_length = 7*60*60*original_frequency
        if raw_spo2.shape[0] > target_length:
            raw_spo2 = spo2.truncate(after=target_length-1)
        elif raw_spo2.shape[0] == target_length:
            pass
        else:
            pad_len = target_length - raw_spo2.shape[0]
            raw_spo2 = np.concatenate([raw_spo2, 98*np.ones(pad_len)])

        print(f"✔ length after padding: {raw_spo2.shape[0]}")

        # Example: spo2 is a 1D numpy array sampled at {original_frequency} Hz
        raw_spo2 = np.array(raw_spo2.tolist())
        # 1. Remove non-physiological values (<50% or >100%)
        spo2 = set_range(raw_spo2, Range_min=50, Range_max=100)
        # # 2. Downsample to 1 Hz
        spo2 = resamp_spo2(spo2, OriginalFreq=original_frequency)
        # 3. Apply Delta Filter (remove sharp jumps/artifacts)
        # print(f"[DEBUG] SPO2 length: {len(spo2)}")
        spo2 = super().dfilter(spo2, Diff=4)
        # 4. Smooth with median filter to avoid spikes
        # print(f"[DEBUG] SPO2 length: {len(spo2)}")
        spo2 = median_spo2(spo2, FilterLength=9)
        # 5. Remove block artifacts (extended low signal sections)
        spo2 = block_data(spo2, treshold=50)
        
        print(f"✔ length after cleaning: {raw_spo2.shape[0]}")

        return pd.Series(spo2)
    
class CleanFeatures(CleanFeaturesInterface):
    def __init__(self, feature_cleaner: CleanFeaturesInterface):
        self._feature_cleaner = feature_cleaner

    def clean_single(self, spo2: pd.Series, original_frequency: int) -> pd.Series:
        return self._feature_cleaner.clean_single(
                    spo2=spo2,
                    original_frequency=original_frequency
                )