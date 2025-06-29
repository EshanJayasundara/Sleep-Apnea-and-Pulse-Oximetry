"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/29 by Eshan Jayasundara
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
from sleepdataspo2.download_data import  *

class RunInterface(ABC):
    @abstractmethod
    def preapre_csv(self, path: str, file_name: str) -> None:
        pass
    @abstractmethod
    def preapre_parquet(self, path: str, file_name: str) -> None:
        pass
    @abstractmethod
    def delete_edf(self, path: str, file_name: str) -> None:
        pass
    @abstractmethod
    def preprocess(self, path: str, file_name: str) -> None:
        pass
    @abstractmethod
    def calculate_odi(self, file_path: str) -> Tuple[float, str]:
        pass
    @abstractmethod
    def process_single(self, dataset:str, file_name: str, token: str, nsrr_path: str, download_path: str) -> None:
        pass
    @abstractmethod
    def run_sequential(self, dataset: str, file_names: List[str], token: str, nsrr_path: str, download_path: str) -> pd.Series:
        pass
    @abstractmethod
    def run_parallel(self, dataset: str, file_names: List[str], token: str, nsrr_path:str, download_path: str, max_threads: int) -> pd.Series:
        pass
    # def write_pickle(self, objs_path: str, obj: object, name: str) -> None:
    #     os.makedirs(objs_path, exist_ok=True)
    #     with open(f"{objs_path}/{name}.pkl", 'wb') as f:
    #         pickle.dump(obj, f)

class RunSHHS(RunInterface):
    def __init__(self, downloader: DownloaderNSRR):
        self._downloader = downloader

    def preapre_csv(self, path, file_name):
        reader = DataLoader(PandasDataLoaderSHHS())
        try:
            df = reader.read_edf(file_path=f"{path}/{file_name}.edf")
            df = df[['time', 'SaO2']]
            df.to_csv(path_or_buf=f"{path}/{file_name}.csv")
            print(f"✔ Created: {path}/{file_name}.csv")
        except Exception as e:
            print(e)

    def preapre_parquet(self, path, file_name):
        reader = DataLoader(PandasDataLoaderSHHS())
        try:
            df = reader.read_edf(file_path=f"{path}/{file_name}.edf")
            df = df[['time', 'SaO2']]
            df.to_parquet(path=f"{path}/{file_name}.parquet")
            print(f"✔ Created: {path}/{file_name}.parquet")
        except Exception as e:
            print(e)

    def delete_edf(self, path, file_name):
        try:
            if os.path.exists(f"{path}/{file_name}.edf"):
                os.remove(f"{path}/{file_name}.edf")
                print(f"✔ Removed: {path}/{file_name}.edf")
            else:
                print(f"✘ Path does not exists: {path}/{file_name}.edf")
        except Exception as e:
            print(e)

    def preprocess(self, path: str, file_name: str) -> None:
        odi, _ = self.calculate_odi(f"{path}/{file_name}.edf")
        odi_path = os.path.join(path, "ODI.csv")

        # Extract just the numeric part of the file_name (e.g., "200001" from "shhs1-200001")
        patient_id = file_name.split("-")[-1]

        # Load or create the ODI.csv
        if os.path.exists(odi_path):
            df = pd.read_csv(odi_path, index_col=0)
        else:
            df = pd.DataFrame(columns=["OxygenDesaturationIndex"])
            
        # Add or update the ODI value
        df.loc[patient_id] = odi
        # Save it
        df.to_csv(odi_path)
        print(f"✔ ODI updated for {file_name}")

    def calculate_odi(self, file_path: str) -> Tuple[float, str]:
        reader = DataLoader(PandasDataLoaderSHHS())
        # scaler = MinMaxScaler((0, 100))
        cleaner = CleanFeatures(CleanSaO2SHHS())
        engineer = EngineerFeatures(EngineerOdiSHHS())
        plotter = PlotGraphs(PlotGraphsSHHS())

        if file_path.endswith(".edf"):
            df = reader.read_edf(file_path=file_path)
        elif file_path.endswith(".csv"):
            df = reader.read_csv(file_path=file_path)
        elif file_path.endswith(".parquet"):
            df = reader.read_parquet(file_path=file_path)
        # resample to 1Hz
        df = df[[True if x - int(x) == 0 else False for x in df.time]]
        # make time column as the index
        df = df.set_index("time")
        # apply the scaler
        # scaled_df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
        spo2 = cleaner.clean_single(df.SaO2)
        pd.DataFrame({
                "time": [i for i in range(len(spo2))],
                "SaO2": spo2.tolist()
            }).set_index("time").to_parquet(path=f"{file_path.split(".")[0]}_cleaned.parquet")
        odi = engineer.compute_single(spo2=spo2)

        name = file_path.split("/")[-1].split(".")[0]

        plotter.plot_one_signal(signal=df.SaO2, title=f"{name} Original Signal", save_path="images/shhs1/SaO2/original", name=name)
        plotter.plot_one_signal(signal=spo2, title=f"{name} Cleaned Signal", save_path="images/shhs1/SaO2/cleaned", name=name)

        return odi, name
    
    def process_single(self, dataset:str, file_name: str, token: str, nsrr_path: str, download_path: str) -> None:
            os.makedirs(download_path, exist_ok=True)
            # check if the file already downloaded
            file_loc = f"{download_path}/{file_name}.edf"
            if os.path.exists(file_loc):
                print(f"✔ Download terminated, file already exists: {file_loc}.edf")
                self.preprocess(path=download_path, file_name=file_name)
                self.delete_edf(path=download_path, file_name=file_name)
                return
            self._downloader.download(dataset=dataset, file_name=file_name, token=token, nsrr_path=nsrr_path, download_path=download_path)
            self.preprocess(path=download_path, file_name=file_name)
            self.delete_edf(path=download_path, file_name=file_name)

    def run_sequential(self, dataset: str, file_names: List[str], token: str, nsrr_path: str, download_path: str) -> None:
        for file_name in file_names:
            self.process_single(dataset, file_name, token, nsrr_path, download_path)

    def run_parallel(self, dataset: str, file_names: List[str], token: str, nsrr_path: str, download_path: str, max_threads: int) -> None:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self.process_single, dataset, file_name, token, nsrr_path, download_path)
                        for file_name in file_names
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error downloading: {e}")
                    