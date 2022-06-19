import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("./data.csv")
    df2 = pd.read_csv("./data_hwrng.csv")
    frames = [df, df2]
    fin = pd.concat(frames, axis=1)
    fin.to_csv('data_QPH.csv', index=False, header=True)