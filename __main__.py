from classes import Ti, Sheets

print("*** Hola Azzrael Code YouTube subs!!! ***")

"""
BBG004730N88 - SBER
BBG0013HGFT4 - USDTOM
"""

ti = Ti(use_sandbox=True)

# ti.buy(10, "BBG004730N88")
# ti.sell(5, "BBG004730N88")

# ti.buy_limit(200, 10000000, "BBG004730N88")
# ti.sell_limit(100000001, 97, "BBG004730N88")

# print(ti.get_sync_client().get_market_search_by_ticker("SBER"))
# print(ti.get_sync_client().get_market_orderbook("BBG004730N88", 2))

sheet = Sheets()
sheet.write(ti)