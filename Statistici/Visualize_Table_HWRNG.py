import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv('./HWRNG_stats.csv')
    df.mean().plot(kind='bar')
    plt.show()
    print(df.to_latex())