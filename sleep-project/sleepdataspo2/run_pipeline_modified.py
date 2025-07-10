"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/29 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
from typing import List
import pandas as pd
import os
from filelock import FileLock, Timeout
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    def clean_signal(self, dataset, download_from, download_to, file_name,  spo2_channel_name) -> str:
        pass
    @abstractmethod
    def engineer_features(self, dataset, download_from, download_to, file_name, spo2_channel_name, complex_features) -> str:
        pass
    @abstractmethod
    def run_all_steps(self, dataset:str, file_name: str, token: str, download_from:str, download_to: str, spo2_channel_name: str, complex_features: bool) -> None:
        pass
    @abstractmethod
    def run_downloader_parallel(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, max_threads: int) -> None:
        pass
    @abstractmethod
    def run_cleaner_parallel(self, dataset: str, file_names: List[str], download_from: str, download_to: str, spo2_channel_name: str, max_threads: int) -> None:
        pass
    @abstractmethod
    def run_flusher_parallel(self, dataset: str, file_names: List[str], download_from: str, download_to: str, max_threads: int) -> None:
        pass
    @abstractmethod
    def run_engineer_parallel(self, dataset: str, file_names: List[str], download_from: str, download_to: str, spo2_channel_name: str, complex_features: bool, max_threads: int) -> None:
        pass
    @abstractmethod
    def run_all_steps_parallel(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, spo2_channel_name: str, max_threads: int, complex_features: bool) -> pd.Series:
        pass

class Run(RunInterface):
    def __init__(
        self,
        downloader: DownloaderNSRR = None,
        reader: DataLoader = None,
        cleaner: CleanFeatures = None,
        plotter: PlotGraphs = None,
        engineer: EngineerFeatures = None,
    ):
        self._downloader = downloader
        self._reader = reader
        self._cleaner = cleaner
        self._plotter = plotter
        self._engineer = engineer

    def preapre_csv(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        try:
            df = self._reader.read_edf(file_path=f"{path}/{file_name}.edf")
            df = df[['time', spo2_channel_name]]
            df.to_csv(path_or_buf=f"{path}/{file_name}.csv")
            print(f"[✔] Created: {path}/{file_name}.csv")
        except Exception as e:
            print(f"{self.__class__}/preapre_csv", e)

    def preapre_parquet(self, dataset, download_from, download_to, file_name, spo2_channel_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        try:
            df = self._reader.read_edf(file_path=f"{path}/{file_name}.edf")
            df = df[['time', spo2_channel_name]]
            df.to_parquet(path=f"{path}/{file_name}.parquet")
            print(f"[✔] Created: {path}/{file_name}.parquet")
        except Exception as e:
            print(f"{self.__class__}/preapre_parquet", e)

    def delete_edf(self, dataset, download_from, download_to, file_name) -> None:
        path = f"{download_to}/{dataset}/{download_from}"
        try:
            if os.path.exists(f"{path}/{file_name}.edf"):
                os.remove(f"{path}/{file_name}.edf")
                print(f"[✔] Removed: {path}/{file_name}.edf")
            else:
                print(f"[✘] Path does not exists: {path}/{file_name}.edf")
        except Exception as e:
            print(f"{self.__class__}/delete_edf", e)
        

    def clean_signal(self, dataset, download_from, download_to, file_name,  spo2_channel_name) -> str:
        path = f"{download_to}/{dataset}/{download_from}"
        file_path = f"{path}/{file_name}"
        file_exists_flag = os.path.exists(file_path)
        if file_path.endswith(".edf") and file_exists_flag:
            df = self._reader.read_edf(file_path=file_path)
        elif file_path.endswith(".csv") and file_exists_flag:
            df = self._reader.read_csv(file_path=file_path)
        elif file_path.endswith(".parquet") and file_exists_flag:
            df = self._reader.read_parquet(file_path=file_path)
        else:
            raise FileNotFoundError(f"{file_path} does not exists...")

        intervals = df['time'].diff().dropna()
        if not np.allclose(intervals, intervals.iloc[0]):
            raise ValueError("Warning: Irregular sampling intervals detected!")
        if 1 / intervals.iloc[0] != int(1 / intervals.iloc[0]):
            raise ValueError(f"original_frequency = {1 / intervals.iloc[0]} is impossible. It should be an integer.")
        original_frequency = int(1 / intervals.iloc[0])

        spo2 = self._cleaner.clean_single(df[spo2_channel_name], original_frequency)

        name = file_name.split(".")[0]

        pd.DataFrame({
                "time": [i for i in range(len(spo2))],
                "SaO2": spo2.tolist()
            }).set_index("time").to_parquet(path=f"{path}/{name}_cleaned.parquet")
        
        self._plotter.plot_one_signal(signal=df[spo2_channel_name], title=f"{name} Original Signal", save_path=f"{download_to}/{dataset}/images/original", name=name)
        self._plotter.plot_one_signal(signal=spo2, title=f"{name} Cleaned Signal", save_path=f"{download_to}/{dataset}/images/cleaned", name=name)
        
        return name

    def engineer_features(self, dataset, download_from, download_to, file_name,  spo2_channel_name, complex_features: bool) -> str:
        path = f"{download_to}/{dataset}/{download_from}"

        file_path = f"{path}/{file_name}_cleaned.parquet"
        if file_path.endswith(".parquet") and os.path.exists(file_path):
            df = self._reader.read_parquet(file_path=file_path)
        else:
            raise FileNotFoundError(f"{file_path} does not exists...")
        
        features = self._engineer.compute_single(spo2=df[spo2_channel_name], complex_features=complex_features)
        
        csv_path = os.path.join(path, f"extracted_{len(features)}_features.csv")
        lock_path = csv_path + ".lock"

        # Extract just the numeric part of the file_name (e.g., "200001" from "shhs1-200001")
        nsrr_id = file_name.split("-")[-1]

        # Use a file lock to avoid concurrent write issues
        lock = FileLock(lock_path, timeout=180)  # waits up to 180 seconds

        try:
            # 1. Lock is acquired at the start of the with block
            # 2. If an exception occurs inside the block:
            #       The with statement guarantees that __exit__() is called.
            #       This automatically releases the lock, even if the block was exited due to an error.
            with lock:
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path, index_col="nsrrid")
                    df.index = df.index.astype(str).str.strip()  # enforce string + trim whitespace
                    df = df[~df.index.duplicated(keep='last')]   # drop any existing duplicates
                else:
                    df = pd.DataFrame(columns=features.keys())
                    df.index.name = "nsrrid"
                    df.index = df.index.astype(str).str.strip()

                df.loc[nsrr_id] = features
                # print(type(nsrr_id))
                df = df[~df.index.duplicated(keep='last')] # ensure no duplicates
                df.to_csv(csv_path)
                print(f"[✔] Updated: {csv_path}")

        except Timeout:
            print(f"[✘] Timeout while waiting for the lock: {lock_path}")
        except Exception as e:
            print(f"[✘] Error during preprocessing for {file_name}: {e}")
    
    def run_all_steps(self, dataset:str, file_name: str, token: str, download_from:str, download_to: str, spo2_channel_name:str, complex_features: bool) -> None:
            download_path = f"{download_to}/{dataset}/{download_from}"
            os.makedirs(download_path, exist_ok=True)
            # check if the file already downloaded
            file_loc = f"{download_path}/{file_name}.edf"
            if os.path.exists(file_loc):
                print(f"[✔] Download terminated, file already exists: {file_loc}")
                self.clean_signal(dataset=dataset, download_from=download_from, download_to=download_to, file_name=f"{file_name}.edf",  spo2_channel_name=spo2_channel_name)
                self.delete_edf(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name)
                self.engineer_features(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name, spo2_channel_name=spo2_channel_name, complex_features=complex_features)
                return
            self._downloader.download(dataset=dataset, file_name=file_name, token=token, download_from=download_from, download_to=download_to)
            self.clean_signal(dataset=dataset, download_from=download_from, download_to=download_to, file_name=f"{file_name}.edf",  spo2_channel_name=spo2_channel_name)
            self.delete_edf(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name)
            self.engineer_features(dataset=dataset, download_from=download_from, download_to=download_to, file_name=file_name, spo2_channel_name=spo2_channel_name, complex_features=complex_features)

    def run_downloader_parallel(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, max_threads: int) -> None:
        download_path = f"{download_to}/{dataset}/{download_from}"
        os.makedirs(download_path, exist_ok=True)
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self._downloader.download, dataset, file_name, token, download_from, download_to)
                        for file_name in file_names
                        # if ".edf" already exists don't download it again
                        if not os.path.exists(f"{download_path}/{file_name}.edf")
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error downloading: {e}")
                    traceback.print_exc()

    def run_cleaner_parallel(self, dataset: str, file_names: List[str], download_from: str, download_to: str, spo2_channel_name: str, max_threads: int) -> None:
        download_path = f"{download_to}/{dataset}/{download_from}"
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self.clean_signal, dataset, download_from, download_to, f"{file_name}.edf", spo2_channel_name)
                        for file_name in file_names
                        # if "<>_cleaned.parquet" already exists don't clean original signal again
                        if not os.path.exists(f"{download_path}/{file_name}_cleaned.parquet")
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error cleaning: {e}")
                    traceback.print_exc()

    def run_flusher_parallel(self, dataset: str, file_names: List[str], download_from: str, download_to: str, max_threads: int) -> None:
        download_path = f"{download_to}/{dataset}/{download_from}"
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self.delete_edf, dataset, download_from, download_to, file_name)
                        for file_name in file_names
                        # if file does not exists dont try to delete it
                        if os.path.exists(f"{download_path}/{file_name}.edf")
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error deleting: {e}")
                    traceback.print_exc()

    def run_engineer_parallel(self, dataset: str, file_names: List[str], download_from: str, download_to: str, spo2_channel_name: str, complex_features: bool, max_threads: int) -> None:
        download_path = f"{download_to}/{dataset}/{download_from}"
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self.engineer_features, dataset, download_from, download_to, file_name, spo2_channel_name, complex_features)
                        for file_name in file_names
                        # if "<>_cleaned.parquet" exists, do feature engineering
                        if os.path.exists(f"{download_path}/{file_name}_cleaned.parquet")
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error deleting: {e}")
                    traceback.print_exc()

    def run_all_steps_parallel(self, dataset: str, file_names: List[str], token: str, download_from: str, download_to: str, spo2_channel_name: str, max_threads: int, complex_features: bool) -> None:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(self.run_all_steps, dataset, file_name, token, download_from, download_to, spo2_channel_name, complex_features)
                        for file_name in file_names
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error: {e}")
                    traceback.print_exc()
