"""
Author: Eshan Jayasundara
Co-Author 1: 
Co-Author 2:
Last Modified: 2025/06/27 by Eshan Jayasundara
"""

import matplotlib
matplotlib.use("Agg")  # Use a backend that does not need a display
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Tuple
import os

class PlotGraphsInterface(ABC):
    @abstractmethod
    def plot_one_signal(self, signal: pd.Series, figsize: Tuple[float, float], title: str, xlabel: str, ylabel: str, save_path: str, name: str) -> None:
        pass

class PlotGraphsNSRR(PlotGraphsInterface):
    def __init__(self):
        pass

    def plot_one_signal(self, signal: pd.Series, figsize: Tuple[float, float]=(100, 5), title: str="Original Signal", xlabel: str="Time (sec)", ylabel: str="SaO2", save_path: str=None, name: str=None) -> None:
        x = np.arange(len(signal))

        plt.figure(figsize=figsize)
        plt.plot(x, signal.tolist())
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        os.makedirs(save_path, exist_ok=True)
        if (save_path != None and name != None):
            plt.savefig(f"{save_path}/{name}.png")

        plt.close()

class PlotGraphs(PlotGraphsInterface):
    def __init__(self, graph_plotter: PlotGraphsInterface):
        self._graph_plotter = graph_plotter

    def plot_one_signal(self, signal, figsize = (100, 5), title = "Original Signal", xlabel = "Time (sec)", ylabel = "SaO2", save_path: str=None, name: str=None) -> None:
        self._graph_plotter.plot_one_signal(
            signal=signal,
            figsize=figsize,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            save_path=save_path,
            name=name
        )