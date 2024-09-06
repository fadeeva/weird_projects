import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


map_data = pd.read_csv('../data/SHR65_22.csv', index_col=0)

def get_data_by_params(params):
    data = map_data.copy()
    
    for k, v in params.items():
        if k in data.columns and v in data[k].unique():
            data = data[data[k]==v]
    
    return data


def get_cases_above_75(by, data_params={}, visualize=True):
    data = get_data_by_params(data_params)
    _75 = data.groupby(by).count().quantile(q=.75)[0]
    
    data = data.groupby(by).count()['CNTYFIPS'].to_frame()
    data.rename(columns={'CNTYFIPS': 'all cases'}, inplace=True)
    
    cases_above_p75 = data[data['all cases']>_75].copy()
    cases_above_p75.rename(columns={'all cases': 'cases above p75'}, inplace=True)
    
    data['below p75'] = data['all cases']
    data.loc[data['below p75'] > _75, 'below p75'] = _75
    data['above p75'] = data['all cases'] - data['below p75']
    
    if visualize:
        visualize_outliers(data, data_params)
    
    return data, cases_above_p75


def visualize_outliers(data, title):
    if isinstance(data.index, pd.MultiIndex):
        visualize_multiindex(data, title)
        return
    
    visualize_cases_above_75(data, title)


def visualize_cases_above_75(data, title):
    fig, ax = plt.subplots(1, figsize=(21, 4))

    data['all cases'].plot(kind='area', ax=ax, color=['r'], label='Above 75%')
    data['below p75'].plot(kind='area', ax=ax, color=['b'], label='Below 75%')
    if not title:
        title = 'All cases'
    ax.set_title(title)
    
    if data.index.name != 'Year':
        x_labels = data.index.to_list()
        ax.set_xticks(np.arange(0, len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=90)
    else:
        x_labels = np.arange(1976, 2023)
        ax.set_xticks(x_labels)
        ax.set_xticklabels(x_labels, rotation=45)
    
    ax.legend()


def visualize_multiindex(data, title):
    fig, ax = plt.subplots(1, figsize=(21, 21))

    x_labels = data.index.get_level_values(0).unique()
    y_labels = data.index.get_level_values(1).unique()

    ax.set_xticks(np.arange(0, len(x_labels)))
    ax.set_yticks(np.arange(0, len(y_labels)))
    
    ax.set_ylim(-1, 51)
    
    ax.set_xticklabels(x_labels, rotation=90)
    ax.set_yticklabels(y_labels);

    for n, i in enumerate(data.index.get_level_values(1).unique()):
        s = data.loc[:, i, :]['above p75']>1
        s = s.astype(int)
        s.index = pd.RangeIndex(len(s.index))
        vector = s[s==1].index.to_list()
        ax.scatter(vector, np.ones(len(vector))*n, color='w')

