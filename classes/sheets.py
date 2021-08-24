import os
from datetime import datetime, timedelta

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from classes import Ti
from config import ROOT_DIR, SPREADSHEET_ID, DT_FORMAT


class Sheets:
    """
    Класс для записи данных из Песочницы в Google Sheets
    по работе с Google Sheets API
    см. Плейлист Google Sheets API https://www.youtube.com/playlist?list=PLWVnIRD69wY75tQAmyMFP-WBKXqJx8Wpq

    Мой сервисный аккаунт (у тебя должен быть свой)
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    """

    def __init__(self):
        pass

    def get_service_sacc(self):
        """
        Билдим клиента для доступа к Google Sheets API для Сервисного Аккаунта
        :return:
        """
        creds_json = ROOT_DIR + "/creds/sacc1.json"
        scopes = ['https://www.googleapis.com/auth/spreadsheets']

        creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
        return build('sheets', 'v4', http=creds_service)

    def write(self, ti : Ti):
        """
        Запись состояния Песочницы в Google Sheets
        :param ti:
        :return:
        """
        # Деньги
        currencies = [['currency','balance']]
        [currencies.append([c.currency.name, float(c.balance)]) for c in ti.get_sync_client().get_portfolio_currencies(ti.get_broker_account_id()).payload.currencies]

        # Операции
        to = datetime.now()
        fr = (to - timedelta(days=365))
        operations = [['operation', 'instrument', 'datetime', 'figi', 'quantity', 'price']]
        [operations.append([
            o.operation_type.name,
            o.instrument_type.name,
            o.date.strftime(DT_FORMAT),
            o.figi,
            o.quantity,
            float(o.price)
        ]) for o in ti.get_sync_client().get_operations(from_=fr, to=to).payload.operations]

        # Открытые Позиции
        positions = [['type', 'figi', 'ticker', 'lots']]
        [positions.append([p.instrument_type.name, p.figi, p.ticker, p.lots]) for p in ti.get_sync_client().get_portfolio().payload.positions]

        # Запись в Google Sheets
        # см. Плейлист Google Sheets API https://www.youtube.com/playlist?list=PLWVnIRD69wY75tQAmyMFP-WBKXqJx8Wpq
        spreadsheet = self.get_service_sacc().spreadsheets()
        spreadsheet.values().batchClear(spreadsheetId=SPREADSHEET_ID, body={'ranges':["Позиции", "Операции", "Деньги"]}).execute()
        body = {
            'valueInputOption' : 'RAW',
            'data' : [
                {'range' : 'Позиции!A1', 'values' : positions},
                {'range' : 'Операции!A1', 'values' : operations},
                {'range' : 'Деньги!A1', 'values' : currencies}
            ]
        }
        spreadsheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()