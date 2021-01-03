from simulator import Simulator
from marketools import Stock, Wallet, store_data, StockQuotes
from stock_index import wig20_2019, mwig40
from tqdm import tqdm


from strategies import ema_strategy as my_strategy
from strategies.ema_strategy import *


StockQuotes.check_for_update = False
store_data()

# === SIMULATOR CONFIG =========================================================
START_DATE = '2015-01-01'  # '2015-01-01'
END_DATE = '2019-12-31'  # '2019-12-31'
TRADING_DAYS = Stock('WIG').ohlc[START_DATE:END_DATE].index
MY_WALLET = Wallet(commission_rate=0.0038, min_commission=3.0)
MY_WALLET.money = 10000
TRADED_TICKERS = wig20_2019
TRADED_TICKERS.update(mwig40)
# ==============================================================================


if __name__ == '__main__':
    print('Preparing data...')
    wig = Stock('WIG')
    stocks_data = dict()
    for tck in tqdm(TRADED_TICKERS):
        stocks_data[tck] = Stock(tck)
    print()

    my_simulator = Simulator(TRADING_DAYS, stocks_data, MY_WALLET, show_plot=False)

    for i_min in range(1000, 4001, 500):
        set_min_investment(i_min)

        my_simulator.reset()
        result = my_simulator.run(my_strategy).tail(1)['Wallet state']
        result = float(result)
        summary = f'{i_min}\t{result}\n'

        with open('strategy_optimization.txt', 'a') as f:
            f.write(summary)