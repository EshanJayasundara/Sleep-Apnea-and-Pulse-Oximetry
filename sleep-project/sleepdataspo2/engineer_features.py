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
from colorama import Fore, Style

class EngineerFeaturesInterface(ABC):
    @abstractmethod
    def compute_single(self, spo2: pd.Series, complex_features: bool) -> float:
        pass

class EngineerOdi(EngineerFeaturesInterface):
    def __init__(self):
        pass

    def compute_single(self, spo2: pd.Series, complex_features: bool=False) -> float:
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
        light_green = Fore.LIGHTGREEN_EX
        reset = Style.RESET_ALL
        
        desat_class_3_relative = DesaturationsMeasures(ODI_Threshold=3, threshold_method=DesatMethodEnum.Relative)
        desat_class_5_relative = DesaturationsMeasures(ODI_Threshold=5, threshold_method=DesatMethodEnum.Relative)
        desat_class_83_hard = DesaturationsMeasures(hard_threshold=83, threshold_method=DesatMethodEnum.Hard)
        desat_class_85_hard = DesaturationsMeasures(hard_threshold=85, threshold_method=DesatMethodEnum.Hard)
        desat_class_90_hard = DesaturationsMeasures(hard_threshold=90, threshold_method=DesatMethodEnum.Hard)
        # Compute the biomarkers with known desaturation locations
        print(f"{light_green}[DEBUG]{reset} Computing desaturation features")
        results_desat_3_relative = desat_class_3_relative.compute(spo2)
        results_desat_5_relative = desat_class_5_relative.compute(spo2)
        results_desat_83_hard = desat_class_83_hard.compute(spo2)
        results_desat_85_hard = desat_class_85_hard.compute(spo2)
        results_desat_90_hard = desat_class_90_hard.compute(spo2)
        print(f"{light_green}[DEBUG]{reset} Completed computing desaturation features")

        hypoxic_class_3_relative = HypoxicBurdenMeasures(results_desat_3_relative.begin, results_desat_3_relative.end, CT_Threshold=90, CA_Baseline=90)
        hypoxic_class_5_relative = HypoxicBurdenMeasures(results_desat_5_relative.begin, results_desat_5_relative.end, CT_Threshold=90, CA_Baseline=90)
        hypoxic_class_83_hard = HypoxicBurdenMeasures(results_desat_83_hard.begin, results_desat_83_hard.end, CT_Threshold=90, CA_Baseline=90)
        hypoxic_class_85_hard = HypoxicBurdenMeasures(results_desat_85_hard.begin, results_desat_85_hard.end, CT_Threshold=90, CA_Baseline=90)
        hypoxic_class_90_hard = HypoxicBurdenMeasures(results_desat_90_hard.begin, results_desat_90_hard.end, CT_Threshold=90, CA_Baseline=90)
        # Compute the biomarkers
        print(f"{light_green}[DEBUG]{reset} Computing burden features")
        results_hypoxic_3_relative = hypoxic_class_3_relative.compute(spo2)
        results_hypoxic_2_relative = hypoxic_class_5_relative.compute(spo2)
        results_hypoxic_83_hard = hypoxic_class_83_hard.compute(spo2)
        results_hypoxic_85_hard = hypoxic_class_85_hard.compute(spo2)
        results_hypoxic_90_hard = hypoxic_class_90_hard.compute(spo2)
        print(f"{light_green}[DEBUG]{reset} Completed computing burden features")

        if complex_features:
            complexity_class = ComplexityMeasures(CTM_Threshold=0.25, DFA_Window=20, M_Sampen=3, R_Sampen=0.2, M_ApEn=2, R_ApEn=0.25)
            # Compute the biomarkers
            print(f"{light_green}[DEBUG]{reset} Computing complexity features")
            results_complexity = complexity_class.compute(spo2)
            print(f"{light_green}[DEBUG]{reset} Completed computing complexity features")

        statistics_class = OverallGeneralMeasures(ZC_Baseline=90, percentile=1, M_Threshold=2, DI_Window=12)
        # Compute the biomarkers
        print(f"{light_green}[DEBUG]{reset} Computing statistical features")
        results_statistics = statistics_class.compute(spo2)
        print(f"{light_green}[DEBUG]{reset} Completed computing statistical features")

        prsa_class_10 = PRSAMeasures(PRSA_Window=10, K_AC=2)
        prsa_class_20 = PRSAMeasures(PRSA_Window=20, K_AC=2)
        # Compute the biomarkers
        print(f"{light_green}[DEBUG]{reset} Computing prsa periodicity features")
        results_PRSA_10 = prsa_class_10.compute(spo2)
        results_PRSA_20 = prsa_class_20.compute(spo2)
        print(f"{light_green}[DEBUG]{reset} Completed computing prsa periodicity features")

        psd_class = PSDMeasures()
        # Compute the biomarkers
        print(f"{light_green}[DEBUG]{reset} Computing psd periodicity features")
        results_PSD = psd_class.compute(spo2)
        print(f"{light_green}[DEBUG]{reset} Completed computing psd periodicity features")

        features = {
            # ---- Relative thresholds ----
            # 3%
            "ODI_thr3": results_desat_3_relative.ODI,
            "DL_u_thr3": results_desat_3_relative.DL_u,
            "DL_sd_thr3": results_desat_3_relative.DL_sd,
            "DA100_u_thr3": results_desat_3_relative.DA100_u,
            "DA100_sd_thr3": results_desat_3_relative.DA100_sd,
            "DAmax_u_thr3": results_desat_3_relative.DAmax_u,
            "DAmax_sd_thr3": results_desat_3_relative.DAmax_sd,
            "DD100_u_thr3": results_desat_3_relative.DD100_u,
            "DD100_sd_thr3": results_desat_3_relative.DD100_sd,
            "DDmax_u_thr3": results_desat_3_relative.DDmax_u,
            "DDmax_sd_thr3": results_desat_3_relative.DDmax_sd,
            "DS_u_thr3": results_desat_3_relative.DS_u,
            "DS_sd_thr3": results_desat_3_relative.DS_sd,
            "TD_u_thr3": results_desat_3_relative.TD_u,
            "TD_sd_thr3": results_desat_3_relative.TD_sd,

            "CA_thr3": results_hypoxic_3_relative.CA,
            "CT_thr3": results_hypoxic_3_relative.CT,
            "POD_thr3": results_hypoxic_3_relative.POD,
            "AODmax_thr3": results_hypoxic_3_relative.AODmax,
            "AOD100_thr3": results_hypoxic_3_relative.AOD100,

            # 5%
            "ODI_thr5": results_desat_5_relative.ODI,
            "DL_u_thr5": results_desat_5_relative.DL_u,
            "DL_sd_thr5": results_desat_5_relative.DL_sd,
            "DA100_u_thr5": results_desat_5_relative.DA100_u,
            "DA100_sd_thr5": results_desat_5_relative.DA100_sd,
            "DAmax_u_thr5": results_desat_5_relative.DAmax_u,
            "DAmax_sd_thr5": results_desat_5_relative.DAmax_sd,
            "DD100_u_thr5": results_desat_5_relative.DD100_u,
            "DD100_sd_thr5": results_desat_5_relative.DD100_sd,
            "DDmax_u_thr5": results_desat_5_relative.DDmax_u,
            "DDmax_sd_thr5": results_desat_5_relative.DDmax_sd,
            "DS_u_thr5": results_desat_5_relative.DS_u,
            "DS_sd_thr5": results_desat_5_relative.DS_sd,
            "TD_u_thr5": results_desat_5_relative.TD_u,
            "TD_sd_thr5": results_desat_5_relative.TD_sd,

            "CA_thr5": results_hypoxic_2_relative.CA,
            "CT_thr5": results_hypoxic_2_relative.CT,
            "POD_thr5": results_hypoxic_2_relative.POD,
            "AODmax_thr5": results_hypoxic_2_relative.AODmax,
            "AOD100_thr5": results_hypoxic_2_relative.AOD100,

            # ---- Hard thresholds ----
            # 83%
            "DL_u_thr83": results_desat_83_hard.DL_u,
            "DL_sd_thr83": results_desat_83_hard.DL_sd,
            "DA100_u_thr83": results_desat_83_hard.DA100_u,
            "DA100_sd_thr83": results_desat_83_hard.DA100_sd,
            "DAmax_u_thr83": results_desat_83_hard.DAmax_u,
            "DAmax_sd_thr83": results_desat_83_hard.DAmax_sd,
            "DD100_u_thr83": results_desat_83_hard.DD100_u,
            "DD100_sd_thr83": results_desat_83_hard.DD100_sd,
            "DDmax_u_thr83": results_desat_83_hard.DDmax_u,
            "DDmax_sd_thr83": results_desat_83_hard.DDmax_sd,
            "DS_u_thr83": results_desat_83_hard.DS_u,
            "DS_sd_thr83": results_desat_83_hard.DS_sd,
            "TD_u_thr83": results_desat_83_hard.TD_u,
            "TD_sd_thr83": results_desat_83_hard.TD_sd,

            "CA_thr83": results_hypoxic_83_hard.CA,
            "CT_thr83": results_hypoxic_83_hard.CT,
            "POD_thr83": results_hypoxic_83_hard.POD,
            "AODmax_thr83": results_hypoxic_83_hard.AODmax,
            "AOD100_thr83": results_hypoxic_83_hard.AOD100,

            # 85%
            "DL_u_thr85": results_desat_85_hard.DL_u,
            "DL_sd_thr85": results_desat_85_hard.DL_sd,
            "DA100_u_thr85": results_desat_85_hard.DA100_u,
            "DA100_sd_thr85": results_desat_85_hard.DA100_sd,
            "DAmax_u_thr85": results_desat_85_hard.DAmax_u,
            "DAmax_sd_thr85": results_desat_85_hard.DAmax_sd,
            "DD100_u_thr85": results_desat_85_hard.DD100_u,
            "DD100_sd_thr85": results_desat_85_hard.DD100_sd,
            "DDmax_u_thr85": results_desat_85_hard.DDmax_u,
            "DDmax_sd_thr85": results_desat_85_hard.DDmax_sd,
            "DS_u_thr85": results_desat_85_hard.DS_u,
            "DS_sd_thr85": results_desat_85_hard.DS_sd,
            "TD_u_thr85": results_desat_85_hard.TD_u,
            "TD_sd_thr85": results_desat_85_hard.TD_sd,

            "CA_thr85": results_hypoxic_85_hard.CA,
            "CT_thr85": results_hypoxic_85_hard.CT,
            "POD_thr85": results_hypoxic_85_hard.POD,
            "AODmax_thr85": results_hypoxic_85_hard.AODmax,
            "AOD100_thr85": results_hypoxic_85_hard.AOD100,

            # 90%
            "DL_u_thr90": results_desat_90_hard.DL_u,
            "DL_sd_thr90": results_desat_90_hard.DL_sd,
            "DA100_u_thr90": results_desat_90_hard.DA100_u,
            "DA100_sd_thr90": results_desat_90_hard.DA100_sd,
            "DAmax_u_thr90": results_desat_90_hard.DAmax_u,
            "DAmax_sd_thr90": results_desat_90_hard.DAmax_sd,
            "DD100_u_thr90": results_desat_90_hard.DD100_u,
            "DD100_sd_thr90": results_desat_90_hard.DD100_sd,
            "DDmax_u_thr90": results_desat_90_hard.DDmax_u,
            "DDmax_sd_thr90": results_desat_90_hard.DDmax_sd,
            "DS_u_thr90": results_desat_90_hard.DS_u,
            "DS_sd_thr90": results_desat_90_hard.DS_sd,
            "TD_u_thr90": results_desat_90_hard.TD_u,
            "TD_sd_thr90": results_desat_90_hard.TD_sd,

            "CA_thr90": results_hypoxic_90_hard.CA,
            "CT_thr90": results_hypoxic_90_hard.CT,
            "POD_thr90": results_hypoxic_90_hard.POD,
            "AODmax_thr90": results_hypoxic_90_hard.AODmax,
            "AOD100_thr90": results_hypoxic_90_hard.AOD100,

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

            # PRSA features (Phase Rectified Signal Averaging)
            "PRSAc_win10": results_PRSA_10.PRSAc,             # PRSA capacity
            "PRSAad_win10": results_PRSA_10.PRSAad,           # PRSA amplitude difference
            "PRSAos_win10": results_PRSA_10.PRSAos,           # PRSA overall slope
            "PRSAsb_win10": results_PRSA_10.PRSAsb,           # PRSA slope before anchor point
            "PRSAsa_win10": results_PRSA_10.PRSAsa,           # PRSA slope after anchor point

            # Autocorrelation
            "AC_win10": results_PRSA_10.AC,                   # Autocorrelation of the signal

            # PRSA features (Phase Rectified Signal Averaging)
            "PRSAc_win20": results_PRSA_20.PRSAc,             # PRSA capacity
            "PRSAad_win20": results_PRSA_20.PRSAad,           # PRSA amplitude difference
            "PRSAos_win20": results_PRSA_20.PRSAos,           # PRSA overall slope
            "PRSAsb_win20": results_PRSA_20.PRSAsb,           # PRSA slope before anchor point
            "PRSAsa_win20": results_PRSA_20.PRSAsa,           # PRSA slope after anchor point

            # Autocorrelation
            "AC_win20": results_PRSA_20.AC,                   # Autocorrelation of the signal

            # Power spectral density features
            "PSD_total": results_PSD.PSD_total,     # Total amplitude of the power spectrum
            "PSD_band": results_PSD.PSD_band,       # Amplitude in a specific frequency band
            "PSD_ratio": results_PSD.PSD_ratio,     # Ratio PSD_band / PSD_total
            "PSD_peak": results_PSD.PSD_peak,       # Peak value in desired frequency band
        }

        if complex_features:
            features["ApEn"] = results_complexity.ApEn      # Approximate entropy
            features["LZ"] = results_complexity.LZ          # Lempel-Ziv complexity
            features["CTM"] = results_complexity.CTM        # Central tendency measure
            features["SampEn"] = results_complexity.SampEn  # Sample entropy
            features["DFA"] = results_complexity.DFA        # Detrended fluctuation analysis   

        return features   
        
class EngineerFeatures(EngineerFeaturesInterface):
    def __init__(self, feature_engineer: EngineerFeaturesInterface):
        self._feature_engineer = feature_engineer

    def compute_single(self, spo2: pd.Series, complex_features: bool) -> float:
        return self._feature_engineer.compute_single(
                    spo2=spo2,
                    complex_features=complex_features,
                )
