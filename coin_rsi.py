import pandas as pd
import time
import pyupbit


def rsiindex(symbol):
    tmpli_t = []
    for i in symbol:
        # print(i)
        df = pyupbit.get_ohlcv(i, interval="minute15")
        # print(df)
        rsi_tmp = rsi(df, 14).iloc[-1]
        # print(rsi_tmp)
        tmpli_t.append(rsi_tmp)
        time.sleep(0.07)
    return tmpli_t


def rsi(ohlc: pd.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    au = up.ewm(com=(period - 1), min_periods=period).mean()
    ad = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = au / ad
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")


def rsi_main(symbol):
    #symbol = pyupbit.get_tickers(fiat="KRW")
    rsi_table = pd.DataFrame()
    rsi_table['symbol'] = symbol
    rsi_table['rsi'] = rsiindex(symbol)
    rsi_table = rsi_table.sort_values(by='rsi')
    rsi_table = rsi_table.reset_index(drop=True)
    return rsi_table
