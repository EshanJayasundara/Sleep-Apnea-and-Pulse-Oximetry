"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/28 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import traceback
import requests
import os
from sleepdataspo2.load_data import *
from sleepdataspo2.run_pipeline import *
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import ChunkedEncodingError, ConnectionError, Timeout
from sleepdataspo2 import BASE_URL, MAX_RETRIES

class DownloaderInterface(ABC):
    @abstractmethod
    def download(self, dataset: str, file_name: str, token: str, download_path: str, max_threads: int) -> None:
        pass
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

class DownloaderNSRR(DownloaderInterface):
    def __init__(self):
        pass

    def download(self, dataset: str, file_name: str, token: str, download_path: str, max_threads: int):
        file_path = f"polysomnography/edfs/{dataset}/{file_name}.edf"
        download_url = f"{BASE_URL}/datasets/shhs/files/a/{token}/m/nsrr-gem-v1-0-0/{file_path}"
        download_loc = f"{download_path}/{file_name}.edf"
        error = None
        partial = True
        params = {"auth_token": token}

        # Setup retry-capable session
        session = requests.Session()
        retries = Retry(
            total=MAX_RETRIES,
            backoff_factor=1,  # wait 1s, 2s, 4s, etc.
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        try:
            with session.get(download_url, stream=True, params=params, verify="cert.pem", timeout=60) as response:
                if response.status_code == 200:
                    with open(download_loc, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    partial = False
                    print(f"✔ Downloaded: {download_loc} ({os.path.getsize(download_loc)} bytes)")
                elif response.status_code == 302:
                    error = "Token Not Authorized to Access Specified File"
                else:
                    error = f"{response.status_code} {response.reason}"

        except (ChunkedEncodingError, ConnectionError, Timeout) as e:
            error = f"(Retryable Error: {type(e).__name__}) {e}"
        except Exception as e:
            print(e)
            error = f"({type(e).__name__}) {e}"

        # partial downloads not aloowed
        finally:
            if partial and os.path.exists(download_loc):
                os.remove(download_loc)
                print(f"✘ Partial file removed: {download_loc}")
            if error:
                print(f"✘ Download failed: {error}")
                return "fail"

        return os.path.getsize(download_loc)

        
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

    def preprocess(self, path, file_name):
        runner = RunSHHS()
        odi, _ = runner.run_single(f"{path}/{file_name}.edf")
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


class DownloaderNSRRFcade:
    def __init__(self):
        self._downloader = DownloaderNSRR()

    def download(self, dataset: str, file_names: List[str], token: str, download_path: str, max_threads: int):
        def download_single(dataset:str, file_name: str, token: str, download_path: str):
            os.makedirs(download_path, exist_ok=True)
            # check if the file already downloaded
            file_loc = f"{download_path}/{file_name}.edf"
            if os.path.exists(file_loc):
                print(f"✔ Download terminated, file already exists: {file_loc}.edf")
                self._downloader.preprocess(path=download_path, file_name=file_name)
                self._downloader.delete_edf(path=download_path, file_name=file_name)
                return
            self._downloader.download(dataset=dataset, file_name=file_name, token=token, download_path=download_path, max_threads=max_threads)
            self._downloader.preprocess(path=download_path, file_name=file_name)
            self._downloader.delete_edf(path=download_path, file_name=file_name)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [
                        executor.submit(download_single, dataset, file_name, token, download_path)
                        for file_name in file_names
                    ]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    print(f"Error downloading: {e}")
