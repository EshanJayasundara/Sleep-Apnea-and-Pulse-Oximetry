"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/28 by Eshan Jayasundara
"""

from sleepdataspo2.download_data import *
from dotenv import load_dotenv, find_dotenv
import argparse
import os

def main():
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

    parser = argparse.ArgumentParser(description="Parse your arguments here to download files")

    # Add arguments
    parser.add_argument(
        "-d", "--dataset",             # argument flag
        type=str,             # type of argument
        required=True,      # required
        help="short name of the dataset in sleepdata.org"  # help message
    )

    parser.add_argument(
        "-s", "--start",     # short and long option
        type=int,
        required=False,
        default=None,
        help="An integer argument for initial file to bedownloaded. Use when --list is not provided"
    )

    parser.add_argument(
        "-e", "--end",     # short and long option
        type=int,
        required=False,
        default=None,
        help="An integer argument for initial file to be downloaded. Use when --list is not provided"
    )

    parser.add_argument(
        "-l", "--list",     # short and long option
        type=str,
        required=False,
        default=None,
        help="String of list of integers indicating set of files each seperated by an space"
    )

    parser.add_argument(
        "-t", "--max_threads",
        type=int,
        required=False,
        default=5,
        help="Number of maximum threds to speedup downlods"
    )

    # Parse the command line arguments
    args = parser.parse_args()
    # Args validation
    if args.start != None and args.end != None and args.list != None:
        raise ValueError("one of '--start and --end' or --list should be provided")
    elif args.start != None and args.end == None and args.list != None:
        raise ValueError("one of '--start and --end' or --list should be provided")
    elif args.start != None and args.end == None and args.list == None:
        raise ValueError("one of '--start and --end' or --list should be provided")
    elif args.start == None and args.end != None and args.list != None:
        raise ValueError("one of '--start and --end' or --list should be provided")
    elif args.start == None and args.end != None and args.list == None:
        raise ValueError("one of '--start and --end' or --list should be provided")
    elif args.start == None and args.end == None and args.list == None:
        raise ValueError("one of '--start and --end' or --list should be provided")
    
    downloader = DownloaderNSRRFcade()

    if args.list:
        range_list = args.list.split(" ")
    else:
        range_list = range(args.start, args.end+1)

    files_to_download = []
    for i in range_list:
        files_to_download.append(f"{args.dataset}-{i}")

    print(files_to_download)

    downloader.download(
        dataset=args.dataset, 
        file_names=files_to_download, 
        token=os.environ["NSRR_TOKEN"], 
        download_path=f"data/shhs/polysomnography/edfs/{args.dataset}", 
        max_threads=args.max_threads
        )

if __name__ == "__main__":
    main()