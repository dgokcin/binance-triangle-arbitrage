import os

from binance.client import Client

API_PUBLIC = os.environ.get("PUBLIC_KEY")
API_SECRET = os.environ.get("SECRET_KEY")

client = Client(API_PUBLIC, API_SECRET)


def _format(price):
	return "{:.8f}".format(price)


def buy_limit(symbol, quantity, buy_price):
	"""
	Orders a limit buy.
	"""
	order = client.order_limit_buy(symbol, quantity, buy_price)

	#   Buy order created.
	return order['order_id']


def sell_limit(symbol, quantity, sell_price):
	"""
	Orders a limit sell.
	"""
	order = client.order_limit_sell(symbol, quantity, sell_price)

	#   Sell order created.
	return order


def buy_market(symbol, quantity):
	"""
	Orders a market buy.
	"""
	order = client.order_market_buy(symbol, quantity)

	#   Buy order created.
	return order


def sell_market(symbol, quantity):
	"""
	Orders a market sell.
	"""
	order = client.order_market_sell(symbol, quantity)

	#   Sell order created.
	return order


def cancel_order(symbol, order_id):
	"""
	Given the symbol and the order_id, cancel an order.
	"""
	cancel = client.cancel_order(symbol=symbol, orderId=order_id)


def topup_bnb(min_balance: float, topup: float):
	"""
	Top up BNB balance if it drops below minimum specified balance
	"""
	bnb_balance = client.get_asset_balance(asset='BNB')
	bnb_balance = float(bnb_balance['free'])
	if bnb_balance < min_balance:
		qty = round(topup - bnb_balance, 5)
		print(qty)
		order = client.order_market_buy(symbol='BNBUSDT', quantity=qty)
		return order
	return False

