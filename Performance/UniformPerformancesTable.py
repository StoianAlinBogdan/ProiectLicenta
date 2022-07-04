import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv('./data_QPH.csv')
    df['HWRNG'] = df['HWRNG'] * 0.396
    df.mean().plot(kind='bar')
    plt.show()
    print(df.mean().to_latex())
    
    