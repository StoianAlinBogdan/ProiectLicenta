import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv("./Statistics.csv")
    print(df.groupby('Generator').agg('mean').to_latex())