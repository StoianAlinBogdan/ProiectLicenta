import pandas as pd


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
