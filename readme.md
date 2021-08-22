# Алготрейдинг в Тинькофф Инвестициях с Python через Open API

- Этот код для видео сериала на канале [Azzrael Code](https://www.youtube.com/channel/UCf6kozNejHoQuFhBDB8cfxA) на YouTube.
- В этом сериале я покажу как можно совершать сделки через Open API Тинькофф Инвестиции.
- Все сделки буду делать в Песочнице Open API (Sandbox), однако этот код можно с минимальными усилиями
переделать под реальный аккаунт.

_Если вы новичок в Open API, то настоятельно рекомендую начать с первого видео в [Плейлисте](https://www.youtube.com/watch?v=PjKMDtLuKPU&list=PLWVnIRD69wY4ane3amNJSFQfls1inhaub). 
Там все с самого начала как, зачем и почему. 
А также базовые настройки, выбор SDK, как обращаться к API и т.д._

## Установка зависимостей

`pip install -r req.txt` Пояснения в видео и в комментариях в коде.
Также получи токены (как минимум для Песочницы) и добави их в `creds/__init__.py`.

## Полезные ссылки

- [Плейлист про Open API Тинькофф Инвестиций](https://www.youtube.com/channel/UCf6kozNejHoQuFhBDB8cfxA)
- [Окружения Open API Тинькофф Инвестиций](https://tinkoffcreditsystems.github.io/invest-openapi/env/)
- [Rest API](https://tinkoffcreditsystems.github.io/invest-openapi/rest/)
- [Swagger (методы API)](https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/)
- В коде используется НЕ ОФИЦИАЛЬНОЕ SDK от [@daxartio](https://github.com/daxartio/tinvest)

## Disclaimer

Я, все же, не считаю Open API лучшим вариантом для тестирования стратегий. 
Это скорее инструмент для тестирования взаимодействия с Open API Тинькофф Инвестиций, 
а стратегии лучше тестировать в других окружениях, например в TradingView.