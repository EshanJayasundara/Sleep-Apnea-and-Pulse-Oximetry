"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
from typing import List
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

from sleepdataspo2.load_data import *
from sleepdataspo2.engineer_features import *
from sleepdataspo2.clean_features import *
from sleepdataspo2.plot_graphs import *

class RunInterface(ABC):
    @abstractmethod
    def run_sequential(self, file_paths: List[str]) -> pd.Series:
        pass
    @abstractmethod
    def run_parallel(self, file_paths: List[str]) -> pd.Series:
        pass
    def write_pickle(self, objs_path: str, obj: object, name: str) -> None:
        os.makedirs(objs_path, exist_ok=True)
        with open(f"{objs_path}/{name}.pkl", 'wb') as f:
            pickle.dump(obj, f)

class RunSHHS(RunInterface):
    def __init__(self):
        pass

    def run_sequential(self, file_paths: List[str]) -> pd.Series:
        reader = DataLoader(PandasDataLoaderSHHS())
        # scaler = MinMaxScaler((0, 100))
        cleaner = CleanFeatures(CleanSaO2SHHS())
        engineer = EngineerFeatures(EngineerOdiSHHS())
        plotter = PlotGraphs(PlotGraphsSHHS())

        series = pd.Series(name="OxygenDesaturationIndex")
        for file_path in file_paths:
            if file_path.endswith(".edf"):
                df = reader.read_edf(file_path=file_path)
            elif file_path.endswith(".csv"):
                df = reader.read_csv(file_path=file_path)
            # resample to 1Hz
            df = df[[True if x - int(x) == 0 else False for x in df.time]]
            # make time column as the index
            df = df.set_index("time")
            # apply the scaler
            # scaled_df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
            spo2 = cleaner.clean_single(df.SaO2)
            odi = engineer.compute_single(spo2=spo2)

            name = file_path.split("/")[-1].split(".")[0]
            series.loc[name.split("-")[-1]] = odi

            plotter.plot_one_signal(signal=df.SaO2, title=f"{name} Original Signal", save_path="images/shhs1/SaO2/original", name=name)
            plotter.plot_one_signal(signal=spo2, title=f"{name} Cleaned Signal", save_path="images/shhs1/SaO2/cleaned", name=name)

        objs_path = "objects/shhs1"
        super().write_pickle(objs_path=objs_path, obj=reader, name="reader")
        # super().write_pickle(objs_path=objs_path, obj=scaler, name="scaler")
        super().write_pickle(objs_path=objs_path, obj=cleaner, name="cleaner")
        super().write_pickle(objs_path=objs_path, obj=engineer, name="engineer")

        return series

    def run_parallel(self, file_paths: List[str], objs_path: str) -> pd.Series:
        # TODO: Use multi-threading here
        pass