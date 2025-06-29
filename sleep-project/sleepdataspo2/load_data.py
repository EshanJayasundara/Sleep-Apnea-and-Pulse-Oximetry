"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import pandas as pd
import traceback
import mne

class DataLoaderInterface(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> pd.DataFrame:
        pass
    def read_edf(self, file_path: str) -> pd.DataFrame:
        pass
    def read_parquet(self, file_path: str) -> pd.DataFrame:
        pass

class PandasDataLoader(DataLoaderInterface):
    def __init__(self):
        pass

    def read_csv(self, file_path:str) -> pd.DataFrame:
        if not file_path.endswith(".csv"):
            raise ValueError("Invalid extension! `.csv` is required.")
        try:
            df = pd.read_csv(filepath_or_buffer=file_path)
        except Exception as e:
            print("Error reading CSV file:")
            print(f"{self.__class__}/read_csv", e)
        return df
    
    def read_edf(self, file_path: str) -> pd.DataFrame:
        if not file_path.endswith(".edf"):
            raise ValueError("Invalid extension! `.edf` is required.")
        try:
            info = mne.io.read_raw_edf(file_path, preload=False, verbose=False)
            # print(info.ch_names)
            # Read only the desired channel
            raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
            # Extract the data and times
            data, times = raw[info.ch_names]
            # print(raw.get_channel_types(picks=info.ch_names[0])[0])
            df = pd.DataFrame(data.T, columns=info.ch_names)
            df['time'] = times
        except Exception as e:
            print("Error reading EDF file:")
            print(f"{self.__class__}/read_edf", e)
        return df
    
    def read_parquet(self, file_path:str) -> pd.DataFrame:
        if not file_path.endswith(".parquet"):
            raise ValueError("Invalid extension! `.parquet` is required.")
        try:
            df = pd.read_parquet(filepath_or_buffer=file_path)
        except Exception as e:
            print("Error reading PARQUET file:")
            print(f"{self.__class__}/read_parquet", e)
        return df

class DataLoader(DataLoaderInterface):
    def __init__(self, data_loader: DataLoaderInterface):
        self._data_loader = data_loader

    def read_csv(self, file_path: str) -> pd.DataFrame:
        return self._data_loader.read_csv(file_path)
    
    def read_edf(self, file_path):
        return self._data_loader.read_edf(file_path)
    
    def read_parquet(self, file_path):
        return self._data_loader.read_parquet(file_path)