import os

from binance.client import Client

API_PUBLIC = os.environ.get("PUBLIC_KEY")
API_SECRET = os.environ.get("SECRET_KEY")

client = Client(API_PUBLIC, API_SECRET)


def execute_triangular_arbitrage(coins, percentage, starting_coin):
    free = client.get_asset_balance(starting_coin)['free']
    budget = (float(free) / 100) * percentage

    print("The " + str(percentage) + "% of your total " + str(free) + " " +
          starting_coin + " is: " + f"{budget:.9f}" + " " + starting_coin +
          ".")

    # TODO:
    #   - Buy coins[1] with coins[0] with a budget of budget.
    #   - Sell all coins[1] in (coins[1] + coins[2]) market.
    #   - Buy coins[3] in (coins[2] + coins[3]) market.


def buy_limit(symbol, quantity, buy_price):
    order = client.order_limit_buy(symbol, quantity, buy_price)

    #   Buy order created.
    return order['order_id']


def sell_limit(symbol, quantity, sell_price):
    order = client.order_limit_sell(symbol, quantity, sell_price)

    #   Sell order created.
    return order


def buy_market(symbol, quantity):
    order = client.order_market_buy(symbol, quantity)

    #   Buy order created.
    return order


def sell_market(symbol, quantity):
    order = client.order_market_sell(symbol, quantity)

    #   Sell order created.
    return order
