import pandas as pd
import math
import numpy as np


def generate_descriptive_stats(nums):
    dict_for_df = {
        'nums': nums
    }
    df = pd.DataFrame.from_dict(dict_for_df)
    stats = {}
    stats['min'] = df['nums'].min()
    stats['max'] = df['nums'].max()
    stats['count'] = len(df['nums'])
    stats['uniques'] = len(set(df['nums']))
    stats['25%'] = df['nums'].quantile(q=0.25)
    stats['50%'] = df['nums'].quantile(q=0.5)
    stats['75%'] = df['nums'].quantile(q=0.75)
    stats['mode'] = df['nums'].mode()[0]
    stats['std'] = df['nums'].std()
    stats['mean'] = df['nums'].mean()
    stats['median'] = df['nums'].median()
    stats['skew'] = df['nums'].skew()
    stats['kurtosis'] = df['nums'].kurt()
    return stats


def Box_Muller(u1, u2):
    u1 = np.array(u1)
    u2 = np.array(u2)
    u1 = u1 / max(u1)
    u2 = u2 / max(u2)
    z1 = np.sqrt(-2 * np.log(u1, where=u1>0)) * np.cos(2 * math.pi * u2)
    z2 = np.sqrt(-2 * np.log(u1, where=u1>0)) * np.sin(2 * math.pi * u2)
    z1 = np.round_((z1 / max(z1))*255)
    z2 = np.round_((z2 / max(z2))*255)
    z1 = np.nan_to_num(z1)
    z2 = np.nan_to_num(z2)
    return (z1.tolist(), z2.tolist())
