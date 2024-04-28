import pandas as pd
from dateutil.parser import *

import utils
import instrument
import ma_result

def ma_cross(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    else:
        return 0
    
def get_ma_col(ma):
    return f"MA_{ma}"

def evaluate_symbol(i_symbol, mashort, malong, price_data):

    price_data = price_data[['time', 'close', get_ma_col(mashort), get_ma_col(malong)]].copy()

    price_data['DIFF'] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data['DIFF_PREV'] = price_data.DIFF.shift(1)
    price_data['MA_CROSS'] = price_data.apply(ma_cross, axis=1)

    df_crosses = price_data[price_data.MA_CROSS != 0].copy()

    df_crosses["DELTA"] = df_crosses.close.diff().shift(-1)
    df_crosses["GAIN"] = df_crosses["DELTA"] * df_crosses["MA_CROSS"]

    df_crosses["SYMBOL"] = i_symbol.name
    df_crosses["MASHORT"] = mashort
    df_crosses["MALONG"] = malong

    del df_crosses[get_ma_col(mashort)]
    del df_crosses[get_ma_col(malong)]

    df_crosses["DURATION"] = df_crosses.time.diff().shift(-1)
    df_crosses["DURATION"] = [x.total_seconds() / 3600 for x in df_crosses.DURATION]
    df_crosses.dropna(inplace=True)

    # print(f"{i_symbol.name} {mashort} {malong} trades: {df_crosses.shape[0]} gain: {df_crosses['GAIN'].sum():.0f}")

    return ma_result.MAResult(
        df_crosses = df_crosses,
        symbol=i_symbol.name,
        params={'mashort' : mashort, 'malong' : malong}
    )

def get_price_data(symbol, interval):
    df = pd.read_pickle(utils.get_his_data_filename(symbol, interval))
    mod_cols = [x for x in df.columns if x != 'time']
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)

    return df

def process_data(ma_short, ma_long, price_data):
    ma_list = set(ma_short + ma_long)
    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.close.rolling(window=ma).mean()

    return price_data

def store_crosses(results):
    all_crosses_df_list = [x.df_crosses for x in results]
    all_crosses_df = pd.concat(all_crosses_df_list)
    all_crosses_df.to_pickle("all_crosses.pkl")

def process_results(results):
    results_list = [r.result_ob() for r in results]
    final_df = pd.DataFrame.from_dict(results_list)

    final_df.to_pickle('ma_test_res.pkl')
    print(final_df.shape, final_df.num_trades.sum())


def run():
    symbols = ["PF_ADAUSD", "PF_DOGEUSD", "PF_DOTUSD", "PF_ETHUSD", "PF_MATICUSD", "PF_SOLUSD", "PF_TRXUSD", "PF_XBTUSD", "PF_XRPUSD"]
    interval = "1h"
    ma_short = [4, 8, 16, 24, 32, 64]
    ma_long = [8, 16, 32, 64, 96, 128, 256]

    results = []

    for symbol in symbols:
        print("running...", symbol)
        i_symbol = instrument.Instrument.get_instruments_dict()[symbol]
        price_data = get_price_data(symbol, interval)
        price_data = process_data(ma_short, ma_long, price_data)
        for _malong in ma_long:
            for _mashort in ma_short:
                if _mashort >= _malong:
                    continue
                results.append(evaluate_symbol(i_symbol, _mashort, _malong, price_data))

    process_results(results)
    store_crosses(results)




            
               
if __name__ == "__main__":
    run()