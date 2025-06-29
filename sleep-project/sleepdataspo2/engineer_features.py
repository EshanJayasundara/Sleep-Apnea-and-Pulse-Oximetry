"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class EngineerFeaturesInterface(ABC):
    @abstractmethod
    def compute_single(self, spo2: pd.Series, sampling_rate: int, drop_threshold: float, min_duration: int) -> float:
        pass

class EngineerOdi(EngineerFeaturesInterface):
    def __init__(self):
        pass

    def compute_single(self, spo2: pd.Series, sampling_rate: int=1, drop_threshold: float=3.0, min_duration: int=10) -> float:
        """
        Computes ODI3% from cleaned SpO2 signal.
        Args:
            spo2: Cleaned (filtered + interpolated) SpO2 signal
            sampling_rate: Samples per second
            drop_threshold: Desaturation threshold (default 3%)
            min_duration: Minimum duration of desaturation (in seconds)
        Returns:
            ODI value = number of desats per hour
        """
        baseline = spo2.rolling(window=300, min_periods=1, center=True).median()  # 5-min rolling median
        desat = (baseline - spo2) >= drop_threshold
        # find consecutive durations
        count = 0
        in_desat = False
        duration = 0
        for val in desat:
            if val:
                duration += 1
                if not in_desat:
                    in_desat = True
            else:
                if in_desat and duration >= min_duration:
                    count += 1
                in_desat = False
                duration = 0
        total_hours = len(spo2) / (sampling_rate * 3600)
        return count / total_hours if total_hours > 0 else np.nan
        
class EngineerFeatures(EngineerFeaturesInterface):
    def __init__(self, feature_engineer: EngineerFeaturesInterface):
        self._feature_engineer = feature_engineer

    def compute_single(self, spo2: pd.Series, sampling_rate: int=1, drop_threshold: float=3.0, min_duration: int=10) -> float:
        return self._feature_engineer.compute_single(
                    spo2=spo2,
                    sampling_rate=sampling_rate,
                    drop_threshold=drop_threshold,
                    min_duration=min_duration
                )
