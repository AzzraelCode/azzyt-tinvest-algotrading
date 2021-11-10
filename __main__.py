from classes import Ti, Sheets

print("*** Hola Azzrael Code YouTube subs!!! ***")

"""
BBG004730N88 - SBER
BBG0013HGFT4 - USDTOM
"""

ti = Ti(use_sandbox=True)
# print(ti.create_sandbox()) # не забудь записать ti_broker_account_id d creds/__init__.py в ti_broker_account_id и закоментить

# узнать номер счета, или по ссылке https://www.tinkoff.ru/invest/portfolio/<набор цифр = номер broker_account_id>/
# print(ti.get_sync_client().get_accounts().payload.accounts)
ti.buy_pseudo(10, "BBG004730N88")
print(ti.get_sync_client().get_portfolio(ti.broker_account_id))
print(ti.get_sync_client().get_portfolio_currencies(ti.broker_account_id))

# ti.buy(10, "BBG004730N88")
# ti.sell(5, "BBG004730N88")

# ti.buy_limit(200, 10000000, "BBG004730N88")
# ti.sell_limit(100000001, 97, "BBG004730N88")

# print(ti.get_sync_client().get_market_search_by_ticker("SBER"))
# print(ti.get_sync_client().get_market_orderbook("BBG004730N88", 2))
