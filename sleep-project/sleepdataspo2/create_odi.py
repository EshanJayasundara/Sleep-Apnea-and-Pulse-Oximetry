import os
from sleepdataspo2.run_pipeline import *
import argparse

def main():
    parser = argparse.ArgumentParser(description="Parse your arguments here to create OxygenDesaturationIndex feature.")

    parser.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="relative file path to the downloaded dataset which contains .csv files."
    )

    parser.add_argument(
        "-n", "--name",
        type=str,
        required=True,
        help="name without file extension to save created odi feature."
    )

    parser.add_argument(
        "-s", "--save",
        type=str,
        required=True,
        help="path to save created odi feature into a .csv file."
    )

    args = parser.parse_args()

    runner = RunSHHS()

    files_list = []
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith(".csv"):
                files_list.append(f"{root}/{file}")

    print(files_list)

    odi = runner.run_sequential(files_list)

    if len(odi):
        odi.to_csv(path_or_buf=f"{args.save}/{args.name}.csv")
        print(f"✔ .csv file for feature `OxygenDesaturationIndex` created at {args.save}/{args.name}.csv")

if __name__ == "__main__":
    main()