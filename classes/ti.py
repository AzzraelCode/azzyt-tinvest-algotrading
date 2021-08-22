import tinvest

import creds


class Ti:
    """
    Класс для работы с Open API Тинькофф Инвестиции
    todo: Работа с ошибками сети и апи
    """


    def __init__(self, use_sandbox = True):
        self._use_sandbox = use_sandbox
        # пока этот код использовать в реале не планируется (только песочница)
        # однако минимальную подготовку по токенам сделал
        self._key = creds.ti_sanbox_token if use_sandbox else creds.ti_real_token

        self.sync_client = None

    def get_sync_client(self):
        """
        Создаю клиента для rest запросов к Open API Тинькофф Инвестиций
        https://tinkoffcreditsystems.github.io/invest-openapi/rest/
        :return:
        """
        if not self.sync_client: self.sync_client = tinvest.SyncClient(self._key, use_sandbox=self._use_sandbox)
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

    def buy(self, figi='BBG0013HGFT4', lots=1):
        """
        Покупка бумаги по figi
        :param figi:
        :param lots:
        :return:
        """
        request = tinvest.MarketOrderRequest(lots=lots, operation=tinvest.OperationType.buy)
        resp = self.get_sync_client().post_orders_market_order(figi, request)
        return resp
