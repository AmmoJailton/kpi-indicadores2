from dataclasses import dataclass

import pandas as pd


@dataclass
class IDFPlot:
    df_plot: pd.DataFrame
    title: str