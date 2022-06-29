import pandas as pd
import matplotlib.pyplot as plt



generators = ['Hadamard1Bit', 'Hadamard8Bit', 'RY1Bit', 'RY8Bit', 'Uniform1Bit', 'Uniform8Bit', 'LCG', 'KISS']
indices = [1, 2, 3, 4, 5, 6, 7, 8]

ax = plt.gca()
ax.set_ylim([0, 3])

if __name__ == "__main__":
    df = pd.read_csv('./Statistics.csv')
    df['Average'] = df['Average'] / 256
    for generator in generators:
        subdf = df[df['Generator'] == generator]
        subdf.drop('Generator', axis=1, inplace=True)
        subdf.melt()
        mean = subdf.mean(axis=0)
        plt.bar(height=mean.values, x=subdf.columns)
        plt.title(generator)
        plt.show()
    


