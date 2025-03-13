from datetime import datetime
from flask import abort, make_response
import sqlite3
import pandas as pd
import json

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

con = sqlite3.connect("trades.sqlite")
TRADES = pd.read_sql_query("SELECT * from epex_12_20_12_13", con)
con.close()
#repeat of where read the database into a dataframe, but make it a constant instaed

#print(TRADES.head())

#can't figure out how to feed two inputs to a function used as an operation_id...
#so have fallen back on making TRADES globally accessible
#TODO:fid a way to do a second input
def api_compute_pnl(strategy_id):
    if strategy_id in TRADES.strategy.unique():
        this_strategy_trades_sell = TRADES[(TRADES.strategy == strategy_id) & (TRADES.side == 'sell')]
        this_strategy_trades_buy = TRADES[(TRADES.strategy == strategy_id) & (TRADES.side == 'buy')]
        sales = this_strategy_trades_sell.quantity * this_strategy_trades_sell.price
        sales_value = sales.sum()
        buys = this_strategy_trades_buy.quantity * this_strategy_trades_buy.price
        buys_value = buys.sum()
        income = sales_value - buys_value
    else:
        income = 0
    #requested a json returned in format:
    """               description: A PnL data object.
          schema:
            type: object
            properties:
              strategy:
                type: string
                example: my_strategy
              value:
                type: float
                example: 100.0
              unit:
                type: string
                example: euro
              capture_time:
                type: string
                example: "2023-01-16T08:15:46Z" """
    PnL_object = {'strategy':str(strategy_id),
                'value':float(income),
                'unit':"euro",
                'capture_time':str(get_timestamp())}
    #PnL_json = json.dumps(PnL_object)
    return PnL_object


