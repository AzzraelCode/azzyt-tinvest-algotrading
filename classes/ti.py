from decimal import Decimal

import tinvest

import creds


class Ti:
    """
    Класс для работы с Open API Тинькофф Инвестиции
    todo: Работа с ошибками сети и апи
    """


    def __init__(self, use_sandbox=False):
        self._use_sandbox = use_sandbox
        self._key =  creds.ti_sanbox_token if use_sandbox else creds.ti_real_token
        self.sync_client = None
        self.broker_account_id = creds.ti_broker_account_id

    def get_sync_client(self):
        """
        Создаю клиента для rest запросов к Open API Тинькофф Инвестиций
        https://tinkoffcreditsystems.github.io/invest-openapi/rest/
        :return:
        """
        if not self.sync_client:
            self.sync_client = tinvest.SyncClient(self._key, use_sandbox=self._use_sandbox)

        return self.sync_client

    def create_sandbox(self):
        """
        Создание песочницы
        https://tinkoffcreditsystems.github.io/invest-openapi/env/
        и сброс старой песочнице, если она была создана ранее
        и ввод на акк виртуальных денег
        :return:
        """
        # проверка на работу в песочнице
        if not self._use_sandbox: return

        # получаю список аккаунтов (в песочнице только 1 акк)
        accounts = self.get_sync_client().get_accounts().payload.accounts

        # если аккаунт в песочнице уже создан, то удлаяю его (хотя есть и методы очистки)
        if len(accounts) > 0: self.get_sync_client().remove_sandbox_account(accounts[0].broker_account_id)


        # создаю аккаунт в песочнице и получаю его номер
        broker_account_id = self.get_sync_client().register_sandbox_account(
            tinvest.SandboxRegisterRequest(broker_account_type=tinvest.BrokerAccountType.tinkoff)
        ).payload.broker_account_id

        # закидываю на акк рубли
        self.get_sync_client().set_sandbox_currencies_balance(
            tinvest.SandboxSetCurrencyBalanceRequest(balance=1000000, currency=tinvest.SandboxCurrency('RUB') )
        )

        # и доллары
        self.get_sync_client().set_sandbox_currencies_balance(
            tinvest.SandboxSetCurrencyBalanceRequest(balance=100000, currency=tinvest.SandboxCurrency('USD') )
        )

        return broker_account_id

    def __market_order_pseudo(self, direction : tinvest.OperationType, lots : int, figi : str):
        # https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/market/get_market_orderbook
        r = self.get_sync_client().get_market_orderbook(figi, 2).payload
        # print(r)

        # todo: Проверять объемы (quantity) и trade_status. Наличие бумаги (для шортов) и много ещё чего ;) ....
        price = float(r.asks[0].price if direction == tinvest.OperationType.buy else r.bids[0].price)
        print("%s %d lots of %s at price = %f, total spent = %f" % (direction, lots, figi, price, price*lots))
        return self.__limit_order(direction, price, lots, figi )

    def buy_pseudo(self, lots=1, figi='BBG0013HGFT4'):
        """
        Эмулирую рыночную ПРОДАЖУ для Песочницы, т.к. рыночная в песочнице ничего не знает о рыночной цене,
        см. описание __market_order
        :param lots:
        :param figi:
        :return:
        """
        self.__market_order_pseudo(tinvest.OperationType.buy, lots, figi)

    def sell_pseudo(self, lots=1, figi='BBG0013HGFT4'):
        """
        Эмулирую рыночную ПРОДАЖУ для Песочницы, т.к. рыночная в песочнице ничего не знает о рыночной цене,
        см. описание __market_order
        :param lots:
        :param figi:
        :return:
        """
        self.__market_order_pseudo(tinvest.OperationType.sell, lots, figi)

    def __market_order(self, direction : tinvest.OperationType, lots : int, figi : str):
        """
        Рыночная заявка
        https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/orders/post_orders_market_order

        https://tinkoffcreditsystems.github.io/invest-openapi/faq_sandbox/
        Песочница ничего не знает о рыночных котировках, поэтому все лимитные поручения сразу, без задержек, исполняются по цене, указанной в поручении.
        Все рыночные поручения исполняются по фиксированной цене в 100.
        Т.е.
        1 долл = 100, 1 лот = 1000 долл = 100000 руб (как для покупки, так и для продажи)
        1 акция Сбера = 100, 1 лот = 10 акций = 1000 руб

        :param direction:
        :param lots:
        :param figi:
        :return:
        """
        request = tinvest.MarketOrderRequest(lots=lots, operation=direction)
        resp = self.get_sync_client().post_orders_market_order(figi, request)
        return resp

    def __limit_order(self, direction : tinvest.OperationType, price : float, lots, figi):
        """
        Песочница исполнит !!! ПО ЛЮБОЙ ЦЕНЕ !!!,
        любой объем и сразу
        https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/orders/post_orders_limit_order

        В текущей версии Open API вообще нет Stop Loss / Take Profit

        :param direction:
        :param price:
        :param lots:
        :param figi:
        :return:
        """
        request = tinvest.LimitOrderRequest(lots=lots, operation=direction, price=Decimal(price))
        resp = self.get_sync_client().post_orders_limit_order(figi, request)
        return resp

    def buy(self, lots=1, figi='BBG0013HGFT4'):
        """
        ПОКУПКА бумаги по figi
        :param lots:
        :param figi:
        :return:
        """
        return self.__market_order(tinvest.OperationType.buy, lots, figi)

    def sell(self, lots=1, figi='BBG0013HGFT4'):
        """
        ПРОДАЖА бумаги по figi
        :param lots:
        :param figi:
        :return:
        """
        return self.__market_order(tinvest.OperationType.sell, lots, figi)

    def buy_limit(self, price : float, lots=1, figi='BBG0013HGFT4'):
        """
        Лимитная заявка на ПОКУПКУ,
        Песочница исполнит по любой цене, любой объем и сразу
        :param price:
        :param lots:
        :param figi:
        :return:
        """
        return self.__limit_order(tinvest.OperationType.buy, price, lots, figi )

    def sell_limit(self, price : float, lots=1, figi='BBG0013HGFT4'):
        """
        Лимитная заявка на ПРОДАЖУ
        :param price:
        :param lots:
        :param figi:
        :return:
        """
        return self.__limit_order(tinvest.OperationType.sell, price, lots, figi )
