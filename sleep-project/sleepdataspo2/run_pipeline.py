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
    def preapre_csv(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        pass
    @abstractmethod
    def preapre_parquet(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        pass
    @abstractmethod
    def delete_edf(self, dataset, download_from, download_to, file_name) -> None:
        pass
    @abstractmethod
    def preprocess(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        pass
    @abstractmethod
    def calculate_features(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> Tuple[float, str]:
        pass
    @abstractmethod
    def process_single(self, dataset:str, file_name: str, token: str, download_from:str, download_to: str, spo2_channel_name: str) -> None:
        pass
    @abstractmethod
    def run_sequential(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, spo2_channel_name: str) -> pd.Series:
        pass
    @abstractmethod
    def run_parallel(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, spo2_channel_name: str, max_threads: int) -> pd.Series:
        pass
    # def write_pickle(self, objs_path: str, obj: object, name: str) -> None:
    #     os.makedirs(objs_path, exist_ok=True)
    #     with open(f"{objs_path}/{name}.pkl", 'wb') as f:
    #         pickle.dump(obj, f)

class Run(RunInterface):
    def __init__(self, downloader: DownloaderNSRR):
        self._downloader = downloader

    def preapre_csv(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        reader = DataLoader(PandasDataLoader())
        try:
            df = reader.read_edf(file_path=f"{path}/{file_name}.edf")
            df = df[['time', spo2_channel_name]]
            df.to_csv(path_or_buf=f"{path}/{file_name}.csv")
            print(f"✔ Created: {path}/{file_name}.csv")
        except Exception as e:
            print(f"{self.__class__}/preapre_csv", e)

    def preapre_parquet(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        reader = DataLoader(PandasDataLoader())
        try:
            df = reader.read_edf(file_path=f"{path}/{file_name}.edf")
            df = df[['time', spo2_channel_name]]
            df.to_parquet(path=f"{path}/{file_name}.parquet")
            print(f"✔ Created: {path}/{file_name}.parquet")
        except Exception as e:
            print(f"{self.__class__}/preapre_parquet", e)

    def delete_edf(self, dataset, download_from, download_to, file_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        try:
            if os.path.exists(f"{path}/{file_name}.edf"):
                os.remove(f"{path}/{file_name}.edf")
                print(f"✔ Removed: {path}/{file_name}.edf")
            else:
                print(f"✘ Path does not exists: {path}/{file_name}.edf")
        except Exception as e:
            print(f"{self.__class__}/delete_edf", e)

    def preprocess(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        features, _ = self.calculate_features(dataset, download_from, download_to, f"{file_name}.edf", spo2_channel_name)
        
        csv_path = os.path.join(path, f"extracted_{len(features)}_features.csv")

        # Extract just the numeric part of the file_name (e.g., "200001" from "shhs1-200001")
        patient_id = file_name.split("-")[-1]

        # Load or create the ODI.csv
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, index_col=0)
        else:
            df = pd.DataFrame(columns=features.keys())
            
        # Add or update the ODI value
        df.loc[patient_id] = features
        # Save it
        df.to_csv(csv_path)
        print(f"✔ ODI updated for {file_name}")

    def calculate_features(self, dataset, download_from, download_to, file_name,  spo2_channel_name) -> Tuple[float, str]:
        path = f"{download_to}/{dataset}/{download_from}"

        reader = DataLoader(PandasDataLoader())
        cleaner = CleanFeatures(CleanSpO2())
        engineer = EngineerFeatures(EngineerOdi())
        plotter = PlotGraphs(PlotGraphsNSRR())

        file_path = f"{path}/{file_name}"
        if file_name.endswith(".edf"):
            df = reader.read_edf(file_path=file_path)
        elif file_name.endswith(".csv"):
            df = reader.read_csv(file_path=file_path)
        elif file_name.endswith(".parquet"):
            df = reader.read_parquet(file_path=file_path)

        intervals = df['time'].diff().dropna()
        if not np.allclose(intervals, intervals.iloc[0]):
            raise ValueError("Warning: Irregular sampling intervals detected!")
        if 1 / intervals.iloc[0] != int(1 / intervals.iloc[0]):
            raise ValueError(f"original_frequency = {1 / intervals.iloc[0]} is impossible. It should be an integer.")
        original_frequency = int(1 / intervals.iloc[0])

        spo2 = cleaner.clean_single(df[spo2_channel_name], original_frequency)

        pd.DataFrame({
                "time": [i for i in range(len(spo2))],
                "SaO2": spo2.tolist()
            }).set_index("time").to_parquet(path=f"{path}/{file_name.split('.')[0]}_cleaned.parquet")
        
        features = engineer.compute_single(spo2=spo2)

        name = file_name.split(".")[0]

        plotter.plot_one_signal(signal=df[spo2_channel_name], title=f"{name} Original Signal", save_path=f"{download_to}/{dataset}/images/original", name=name)
        plotter.plot_one_signal(signal=spo2, title=f"{name} Cleaned Signal", save_path=f"{download_to}/{dataset}/images/cleaned", name=name)

        return features, name
    
    def process_single(self, dataset:str, file_name: str, token: str, download_from:str, download_to: str, spo2_channel_name:str) -> None:
            download_path = f"{download_to}/{dataset}/{download_from}"
            os.makedirs(download_path, exist_ok=True)
            # check if the file already downloaded
            file_loc = f"{download_path}/{file_name}.edf"
            if os.path.exists(file_loc):
                print(f"✔ Download terminated, file already exists: {file_loc}.edf")
                self.preprocess(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name, spo2_channel_name=spo2_channel_name)
                self.delete_edf(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name)
                return
            self._downloader.download(dataset=dataset, file_name=file_name, token=token, download_from=download_from, download_to=download_to)
            self.preprocess(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name, spo2_channel_name=spo2_channel_name)
            self.delete_edf(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name)

    def run_sequential(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, spo2_channel_name: str) -> None:
        for file_name in file_names:
            self.process_single(dataset, file_name, token, download_from, download_to, spo2_channel_name)

    def run_parallel(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, spo2_channel_name: str, max_threads: int) -> None:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self.process_single, dataset, file_name, token, download_from, download_to, spo2_channel_name)
                        for file_name in file_names
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error downloading: {e}")
                    traceback.print_exc()