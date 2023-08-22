import pyupbit
import kakao_send_msg
import coin_rsi
import schedule

# 스케줄로 1분마다 실행


def refresh():
    global trade_tmp
    trade_tmp = ''
    access_key = "access_key"  # 변경
    secret_key = "secret_key"  # 변경

    upbit = pyupbit.Upbit(access_key, secret_key)
    bals = upbit.get_balances()
    balance_li = []
    coin_li = []
    coin_amount_li = []
    total_coin_li = []
    tmp = 0
    for bal in bals:
        # print(bal)
        if bal['avg_buy_price'] == '0':
            continue
        else:
            if pyupbit.get_current_price("KRW-"+bal['currency'])*round(float(bal['balance']), 5) > 10000:
                balance_li.append(bal['currency']+" "+str(format(round(pyupbit.get_current_price(
                    "KRW-"+bal['currency'])*round(float(bal['balance']), 5)), ',')+"원"))
                coin_li.append("KRW-"+bal['currency'])
                coin_amount_li.append(bal['balance'])
                tmp = tmp + \
                    pyupbit.get_current_price(
                        "KRW-"+bal['currency'])*round(float(bal['balance']), 5)
    balance_li.append(
        "KRW "+str(format(int(upbit.get_balance(ticker="KRW")), ','))+"원")
    # 총매수금액
    balance_li.append(
        "총보유금액 "+str(format(round(upbit.get_balance(ticker="KRW")+tmp), ','))+"원")

    if upbit.get_balance(ticker="KRW") < 10000:
        kakao_send_li = []
        rsi_table = coin_rsi.rsi_main(coin_li)
        rsi_table['amount'] = coin_amount_li
        symbol_60 = rsi_table[(rsi_table['rsi'] >= 65) & (
            rsi_table['rsi'] < 70)][['symbol', 'amount']]  # 70%매도
        symbol_60 = symbol_60[symbol_60['symbol'] != trade_tmp]
        symbol_70 = rsi_table[rsi_table['rsi']
                              >= 70][['symbol', 'amount']]  # 풀매도
        if len(symbol_70) > 0:
            for sy, am in zip(symbol_70['symbol'], symbol_70['amount']):
                #print(sy, am)
                upbit.sell_market_order(sy, am)
                kakao_send_li.append(
                    str(sy+" "+str(float(am))+"개 100%매도"))
            if len(symbol_60) > 0:
                for sy, am in zip(symbol_60['symbol'], symbol_60['amount']):
                    trade_tmp = sy
                    print(sy, am)
                    upbit.sell_market_order(sy, float(am)*0.7)
                    kakao_send_li.append(
                        str(sy+" "+str(float(am)*0.7)+"개 70%매도"))
        else:
            if len(symbol_60) > 0:
                # print(symbol_60)
                for sy, am in zip(symbol_60['symbol'], symbol_60['amount']):
                    trade_tmp = sy
                    print(sy, am)
                    upbit.sell_market_order(sy, float(am)*0.7)
                    kakao_send_li.append(
                        str(sy+" "+am+" "+str(float(am)*0.7)+"개 70%매도"))
            else:
                kakao_send_msg.send_msg(balance_li)
                rsi_loc_li = []
                for rsi_loc in range(len(rsi_table)):
                    rsi_loc_li.append(
                        str(rsi_table['symbol'][rsi_loc])+" rsi : "+str(round(float(rsi_table['rsi'][rsi_loc]), 3)))
                kakao_send_msg.send_msg(rsi_loc_li)

        kakao_send_msg.send_msg(kakao_send_li)
        pass

    else:
        kakao_send_li = []
        rsi_table = coin_rsi.rsi_main(coin_li)
        rsi_table['amount'] = coin_amount_li
        symbol_60 = rsi_table[(rsi_table['rsi'] >= 65) & (
            rsi_table['rsi'] < 70)][['symbol', 'amount']]  # 70%매도
        symbol_60 = symbol_60[symbol_60['symbol'] != trade_tmp]
        symbol_70 = rsi_table[rsi_table['rsi']
                              >= 70][['symbol', 'amount']]  # 풀매도
        if len(symbol_70) > 0:
            for sy, am in zip(symbol_70['symbol'], symbol_70['amount']):
                #print(sy, am)
                upbit.sell_market_order(sy, am)
                kakao_send_li.append(
                    str(sy+" "+str(float(am))+"개 100%매도"))
            if len(symbol_60) > 0:
                for sy, am in zip(symbol_60['symbol'], symbol_60['amount']):
                    trade_tmp = sy
                    print(sy, am)
                    upbit.sell_market_order(sy, float(am)*0.7)
                    kakao_send_li.append(
                        str(sy+" "+str(float(am)*0.7)+"개 70%매도"))
        else:
            #
            if len(symbol_60) > 0:
                # print(symbol_60)
                for sy, am in zip(symbol_60['symbol'], symbol_60['amount']):
                    trade_tmp = sy
                    print(sy, am)
                    upbit.sell_market_order(sy, float(am)*0.7)
                    kakao_send_li.append(
                        str(sy+" "+am+" "+str(float(am)*0.7)+"개 70%매도"))
            else:
                kakao_send_msg.send_msg(balance_li)
                rsi_loc_li = []
                for rsi_loc in range(len(rsi_table)):
                    rsi_loc_li.append(
                        str(rsi_table['symbol'][rsi_loc])+" rsi : "+str(round(float(rsi_table['rsi'][rsi_loc]), 3)))
                kakao_send_msg.send_msg(rsi_loc_li)

        symbol = pyupbit.get_tickers(fiat="KRW")

        kakao_send_msg.send_msg(kakao_send_li)
        if upbit.get_balance(ticker="KRW") > 10000:
            total_coin_li = pyupbit.get_tickers(fiat="KRW")
            rsi_table = coin_rsi.rsi_main(total_coin_li)

            symbol_35 = rsi_table[rsi_table['rsi'] <= 29]['symbol']  # 풀매수
            symbol_40 = rsi_table[(rsi_table['rsi'] <= 33) &
                                  (rsi_table['rsi'] > 29)]['symbol']  # 50%매수

            symbol_40 = symbol_40[symbol_40.isin(coin_li) == False]
            current_money = upbit.get_balance(ticker="KRW")

            if len(symbol_35) > 0:
                for sy in symbol_35:
                    upbit.buy_market_order(
                        sy, int(int(current_money)/len(symbol_35)))
                    kakao_send_li.append(
                        str(sy+" "+str(int(int(current_money)/len(symbol_35)))+"원 매수"))

            elif len(symbol_40) > 0:
                upbit.buy_market_order(
                    sy, int(int(current_money)/len(symbol_40)*0.5))
                for sy in symbol_40:
                    kakao_send_li.append(
                        str(sy+" "+str(int(int(current_money)/len(symbol_40)*0.5))+"원 매수"))
            else:
                kakao_send_msg.send_msg(balance_li)
            kakao_send_msg.send_msg(kakao_send_li)
    kakao_send_msg.send_msg(balance_li)


schedule.every(1).minutes.do(refresh)
# schedule.every(0.1).seconds.do(refresh)

while True:
    schedule.run_pending()
