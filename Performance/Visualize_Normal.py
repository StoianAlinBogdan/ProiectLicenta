import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df = pd.read_csv("data_NormalDists.csv")
    df.plot(y=df.columns, kind='line')
    plt.show()