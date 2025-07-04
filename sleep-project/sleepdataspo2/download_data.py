"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/29 by Eshan Jayasundara
"""

from abc import ABC, abstractmethod
import certifi
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
from tqdm import tqdm
from colorama import Fore, Style

class DownloaderInterface(ABC):
    @abstractmethod
    def download(self, dataset: str, file_name: str, token: str, download_from: str, download_to: str) -> None:
        pass

class DownloaderNSRR(DownloaderInterface):
    def __init__(self):
        pass

    def download(self, dataset: str, file_name: str, token: str, download_from:str, download_to: str) -> None:
        file_path = f"{download_from}/{file_name}.edf"
        download_url = f"{BASE_URL}/datasets/{dataset}/files/a/{token}/m/nsrr-gem-v1-0-0/{file_path}"
        download_loc = f"{download_to}/{dataset}/{file_path}"
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
            # with session.get(download_url, stream=True, params=params, verify="cert.pem", timeout=60) as response:
            with session.get(download_url, stream=True, params=params, verify=certifi.where(), timeout=60) as response:
                if response.status_code == 200:
                    total_size = int(response.headers.get('Content-Length', 0))
                    blue = Fore.BLUE  # ANSI for sky blue
                    reset = Style.RESET_ALL
                    with open(download_loc, 'wb') as f, tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=f"{blue}Downloading {file_name}.edf{reset}",
                        bar_format="{desc} |{bar}| {percentage:3.0f}% {elapsed}",
                        ascii=False,  # minimal-style bar false
                        ncols=60,     # small width
                        colour="blue",
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                    partial = False
                    print(f"[✔] Downloaded: {download_loc} ({os.path.getsize(download_loc)} bytes)")
                elif response.status_code == 302:
                    error = "Token Not Authorized to Access Specified File"
                else:
                    error = f"{response.status_code} {response.reason}"

        except (ChunkedEncodingError, ConnectionError, Timeout) as e:
            error = f"(Retryable Error: {type(e).__name__}) {e}"
        except Exception as e:
            print(f"{self.__class__}/download", e)
            error = f"({type(e).__name__}) {e}"

        # partial downloads not aloowed
        finally:
            if partial and os.path.exists(download_loc):
                os.remove(download_loc)
                print(f"[✘] Partial file removed: {download_loc}")
            if error:
                print(f"[✘] Download failed: {error}")
                return "fail"

        return os.path.getsize(download_loc)
