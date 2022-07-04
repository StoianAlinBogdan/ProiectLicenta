import pandas as pd
import matplotlib.pyplot as plt
from Helpers import generate_descriptive_stats

dict_for_csv = {
    'Generator': [],
    'Average': [],
    'KS Test': [],
    'Z Test': [],
    'Chi Squared Test': [],
    'Product of successive values': [],
    'Correlation Coefficient': []
}

def append_data(name, stats):
    dict_for_csv['Generator'].append(name)
    dict_for_csv['Average'].append(stats['mean'])
    dict_for_csv['KS Test'].append(stats['Kologomorov-Smirnov test vs. uniform (value should be very close to 0 for uniform):'])
    dict_for_csv['Z Test'].append(stats['Z-test vs. uniform (Value should be <-2.5 or >2.5: '])
    dict_for_csv['Chi Squared Test'].append(stats['Chi squared test for uniformity (Value should be close to 1 for uniform): '])
    dict_for_csv['Product of successive values'].append(stats['Product of successive values (should be 1/4 for uniform): '])
    dict_for_csv['Correlation Coefficient'].append(stats['Correlation coefficient (should be 0 for uniform): '])

if __name__ == "__main__":
    numbers = []
    with open('./numbers_hwrng.txt', 'r') as f:
        for line in f:
            x = line[:-1]
            numbers.append(int(x))
    stats = generate_descriptive_stats(numbers)
    append_data('HWRNG', stats)
    
    df = pd.DataFrame.from_dict(dict_for_csv)
    df['Average'] = df['Average'] / 256
    df.to_csv('./HWRNG_stats.csv', index=False)