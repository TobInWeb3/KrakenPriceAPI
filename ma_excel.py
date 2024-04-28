import pandas as pd
import xlsxwriter

def create_excel(ma_test_res):
    filename = "ma_results.xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    ma_test_res = ma_test_res[['symbol']]

if __name__ == "__main__":
    df = pd.read_pickle("ma_test_res.pkl")
    create_excel(df)