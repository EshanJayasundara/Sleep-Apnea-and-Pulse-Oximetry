"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from pobm.obm.desat import DesaturationsMeasures
from pobm.obm.burden import HypoxicBurdenMeasures
from pobm.obm.complex import ComplexityMeasures
from pobm.obm.general import OverallGeneralMeasures
from pobm.obm.periodicity import  PRSAMeasures, PSDMeasures
from pobm._ResultsClasses import DesatMethodEnum

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

        desat_class = DesaturationsMeasures(ODI_Threshold=3, threshold_method=DesatMethodEnum.Relative)
        # Compute the biomarkers with known desaturation locations
        results_desat = desat_class.compute(spo2)

        hypoxic_class = HypoxicBurdenMeasures(results_desat.begin, results_desat.end, CT_Threshold=90, CA_Baseline=90)
        # Compute the biomarkers
        results_hypoxic = hypoxic_class.compute(spo2)

        complexity_class = ComplexityMeasures(CTM_Threshold=0.25, DFA_Window=20, M_Sampen=3, R_Sampen=0.2, M_ApEn=2, R_ApEn=0.25)
        # Compute the biomarkers
        results_complexity = complexity_class.compute(spo2)

        statistics_class = OverallGeneralMeasures(ZC_Baseline=90, percentile=1, M_Threshold=2, DI_Window=12)
        # Compute the biomarkers
        results_statistics = statistics_class.compute(spo2)

        prsa_class = PRSAMeasures(PRSA_Window=10, K_AC=2)
        # Compute the biomarkers
        results_PRSA = prsa_class.compute(spo2)

        psd_class = PSDMeasures()
        # Compute the biomarkers
        results_PSD = psd_class.compute(spo2)


        return {
            # Desaturation event features
            "ODI": results_desat.ODI,                 # Oxygen Desaturation Index: Number of desaturations per hour
            "DL_u": results_desat.DL_u,               # Mean desaturation duration
            "DL_sd": results_desat.DL_sd,             # Std deviation of desaturation duration
            "DA100_u": results_desat.DA100_u,         # Mean area under desaturation curve (baseline = 100%)
            "DA100_sd": results_desat.DA100_sd,       # Std deviation of DA100
            "DAmax_u": results_desat.DAmax_u,         # Mean desaturation area (baseline = max value)
            "DAmax_sd": results_desat.DAmax_sd,       # Std deviation of DAmax
            "DD100_u": results_desat.DD100_u,         # Mean desaturation depth from 100%
            "DD100_sd": results_desat.DD100_sd,       # Std deviation of DD100
            "DDmax_u": results_desat.DDmax_u,         # Mean desaturation depth from max value
            "DDmax_sd": results_desat.DDmax_sd,       # Std deviation of DDmax
            "DS_u": results_desat.DS_u,               # Mean slope of desaturation events
            "DS_sd": results_desat.DS_sd,             # Std deviation of desaturation slopes
            "TD_u": results_desat.TD_u,               # Mean time between desaturation events
            "TD_sd": results_desat.TD_sd,             # Std deviation of time between desaturations

            # Cumulative oxygen metrics
            "CA": results_hypoxic.CA,                   # Integral of SpO2 below a threshold, normalized by total time
            "CT": results_hypoxic.CT,                   # % of time spent below threshold SpO2
            "POD": results_hypoxic.POD,                 # % of desaturation events over total time
            "AODmax": results_hypoxic.AODmax,           # Area under desaturation curve using max SpO2 as baseline, normalized
            "AOD100": results_hypoxic.AOD100,           # Cumulative area below 100% SpO2 baseline, normalized

            # Nonlinear complexity measures
            "ApEn": results_complexity.ApEn,               # Approximate entropy
            "LZ": results_complexity.LZ,                   # Lempel-Ziv complexity
            "CTM": results_complexity.CTM,                 # Central tendency measure
            "SampEn": results_complexity.SampEn,           # Sample entropy
            "DFA": results_complexity.DFA,                 # Detrended fluctuation analysis

            # Statistical features of the SpO2 signal
            "AV": results_statistics.AV,                   # Mean (average) SpO2
            "MED": results_statistics.MED,                 # Median SpO2
            "Min": results_statistics.Min,                 # Minimum SpO2 value
            "SD": results_statistics.SD,                   # Standard deviation of SpO2
            "RG": results_statistics.RG,                   # SpO2 range (max - min)
            "P": results_statistics.P,                     # Percentile value (e.g., 5th or 95th)
            "M": results_statistics.M,                     # % of time below median SpO2 - x%
            "ZC": results_statistics.ZC,                   # Number of zero-crossing points
            "DI": results_statistics.DI,                   # Delta Index
            "K": results_statistics.K,                     # Kurtosis of SpO2 signal
            "SK": results_statistics.SK,                   # Skewness of SpO2 signal
            "MAD": results_statistics.MAD,                 # Mean absolute deviation

            # PRSA features (Phase Rectified Signal Averaging)
            "PRSAc": results_PRSA.PRSAc,             # PRSA capacity
            "PRSAad": results_PRSA.PRSAad,           # PRSA amplitude difference
            "PRSAos": results_PRSA.PRSAos,           # PRSA overall slope
            "PRSAsb": results_PRSA.PRSAsb,           # PRSA slope before anchor point
            "PRSAsa": results_PRSA.PRSAsa,           # PRSA slope after anchor point

            # Autocorrelation
            "AC": results_PRSA.AC,                   # Autocorrelation of the signal

            # Power spectral density features
            "PSD_total": results_PSD.PSD_total,     # Total amplitude of the power spectrum
            "PSD_band": results_PSD.PSD_band,       # Amplitude in a specific frequency band
            "PSD_ratio": results_PSD.PSD_ratio,     # Ratio PSD_band / PSD_total
            "PSD_peak": results_PSD.PSD_peak,       # Peak value in desired frequency band
        }
        
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
