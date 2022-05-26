from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

abspath = os.path.abspath(os.getcwd())
path = str(abspath)

def pctsmokercorrelationsvis(frame, features):
    spr = pd.DataFrame()
    spr['feature'] = features
    spr['spearman'] = [frame[f].corr(frame['% Smokers'], 'spearman') for f in features]
    spr = spr.sort_values('spearman')
    plt.figure(figsize=(6, 0.25*len(features)))
    sns.barplot(data=spr, y='feature', x='spearman', orient='h')
    plt.show()

def correlationmatrixvis(frame):
    sns.heatmap(frame[frame.columns[list(range(1, frame.shape[0]))].tolist()], yticklabels=frame.columns.tolist()[1:])
    plt.show()
