
import pandas as pd


def read():
    df = pd.read_excel("/Users/wlq/Desktop/team.xlsx", sheet_name="Sheet1")
    shape = df.shape


if __name__ == "__main__":
    read()
