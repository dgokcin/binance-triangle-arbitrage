from collections import defaultdict
from operator import itemgetter
from time import time
import os

from binance.client import Client
import binance_api as api

API_PUBLIC = os.environ.get("PUBLIC_KEY")
API_SECRET = os.environ.get("SECRET_KEY")

FEE = 0.0005
PERCENTAGE = 5  # percentage of the primary coin budget to use for arbitrage.
STARTING_COIN = 'BTC'

with open('primary.txt') as f:
    PRIMARY = [line.rstrip() for line in f]

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

    #   not sure about how to determine to the price parameter.
    #   not sure which method to use, LIMIT or MARKET
    #   note that this is not an actual order but a test order.
    # TODO:
    #   - you need to figure out a relationship between budget and price.
    #   - you need to make sure that coins[i] + coins[j] market exist(
    #   BNB->COMP) does not exist.
    #

    # buy_order_limit = client.create_test_order(symbol=coins[1] + coins[0],
    #                                            side='BUY',
    #                                            type='LIMIT',
    #                                            timeInForce='GTC',
    #                                            quantity=0.5,
    #                                            price=0.00001)

    #   note that this is an actual order
    # buy_order_limit = client.order_limit_buy(symbol=coins[1] + coins[0],
    #                                          quantity=budget,
    #                                          price=200)

    # amount = client.get_asset_balance(coins[1])['free']
    # sell_order_limit = client.create_test_order(symbol=coins[0] + coins[1],
    #                                             side='SELL',
    #                                             type='LIMIT',
    #                                             timeInForce='GTC',
    #                                             quantity=api._format(amount),
    #                                             price=200)


def main():
    start_time = time()

    prices = get_prices()
    prices_time = time()
    print(f"Downloaded in: {prices_time - start_time:.4f}s")

    triangles = list(find_triangles(prices))
    print(f"Computed in: {time() - prices_time:.4f}s")

    if triangles:
        for triangle in sorted(triangles, key=itemgetter('profit'), reverse=True):
            describe_triangle(prices, triangle)
    else:
        print("No triangles found, trying again!")
        main()


def get_prices():
    prices = client.get_orderbook_tickers()
    prepared = defaultdict(dict)
    for ticker in prices:
        pair = ticker['symbol']
        ask = float(ticker['askPrice'])
        bid = float(ticker['bidPrice'])
        if ask == 0.0:
            continue
        for primary in PRIMARY:
            if pair.endswith(primary):
                secondary = pair[:-len(primary)]
                prepared[primary][secondary] = 1 / ask
                prepared[secondary][primary] = bid
    return prepared


def find_triangles(prices):
    triangles = []
    starting_coin = STARTING_COIN
    for triangle in recurse_triangle(prices, starting_coin, starting_coin):
        coins = set(triangle['coins'])
        if not any(prev_triangle == coins for prev_triangle in triangles):
            yield triangle
            triangles.append(coins)


def recurse_triangle(prices, current_coin, starting_coin, depth_left=3, amount=1.0):
    if depth_left > 0:
        pairs = prices[current_coin]
        for coin, price in pairs.items():
            new_price = (amount * price) * (1.0 - FEE)
            for triangle in recurse_triangle(prices, coin, starting_coin, depth_left - 1, new_price):
                triangle['coins'] = triangle['coins'] + [current_coin]
                yield triangle
    elif current_coin == starting_coin and amount > 1.0:
        yield {
            'coins': [current_coin],
            'profit': amount
        }


def describe_triangle(prices, triangle):
    coins = triangle['coins']
    price_percentage = (triangle['profit'] - 1.0) * 100
    execute_triangular_arbitrage(coins, PERCENTAGE, STARTING_COIN)
    print(f"{'->'.join(coins):26} {round(price_percentage, 4):-7}% <- profit!")
    for i in range(len(coins) - 1):
        first = coins[i]
        second = coins[i + 1]
        print(f"     {second:4} / {first:4}: {prices[first][second]:-17.8f}")
    print('')


if __name__ == '__main__':
    main()
