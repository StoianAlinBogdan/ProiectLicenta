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
    stats['Kologomorov-Smirnov test vs. uniform (value should be very close to 0 for uniform):'] = KS_uniform(nums)
    stats['Z-test vs. uniform (Value should be <-2.5 or >2.5: '] = Z_test(nums)
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

def KS_uniform(nums):
    nums = np.clip(np.divide(nums, 255), 0.0001, 0.9999)
    D_plus = 0
    D_minus = 0
    N = len(nums)
    memory_cdf = np.sort(nums)
    arange1 = np.arange(1.0, N + 1) / N
    arange2 = np.arange(0.0, N) / N
    D_plus = (arange1 - memory_cdf).max()
    D_minus = (memory_cdf - arange2).max()
    return(max(D_plus, D_minus))


def Z_test(nums):
    unique_numbers = list(set(nums))
    my_counts = {x: nums.count(x) for x in unique_numbers}
    df_dict = {"number": my_counts.keys(), "counts": my_counts.values()} 
    df = pd.DataFrame.from_dict(df_dict)
    dist_uniform = np.random.randint(df['counts'].min(), df['counts'].max(), len(df))
    numbers_dist_uniform = range(0, len(dist_uniform))
    dict_dist_uniform = {numbers_dist_uniform[i]: dist_uniform[i] for i in range(len(dist_uniform))}
    data_dist_uniform = {"number": dict_dist_uniform.keys(), "counts": dict_dist_uniform.values()}
    df2 = pd.DataFrame.from_dict(data_dist_uniform)
    z_calc = (df['counts'].mean() - df2['counts'].mean()) / (math.sqrt(df.var()['counts'] / len(df['counts']) + df2.var()['counts'] / len(df2['counts'])))
    return z_calc