<!-- If PyCharm or IDEA will throw a warning here, just ignore it -->
<div align="center">
    <img src="https://raw.githubusercontent.com/SecondThundeR/shikithon/main/assets/logo.png" alt="Shikithon Logo">
    <h1>Shikithon</h1>
    <p>Очередной враппер для Shikimori API, написанный на Python</p>
</div>

[![Publish Shikithon package to PyPI](https://github.com/SecondThundeR/shikithon/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/SecondThundeR/shikithon/actions/workflows/pypi-publish.yml)

> **Состояние библиотеки:** завершена основная разработка
>
> На данный момент, библиотека находится в статусе поддержки (новые функции будут добавляться только по необходимости)
>
> Начиная с версии 2.0.0, библиотека поддерживает асинхронные запросы, отдельные пути к ресурсам API и многое другое
> _[(Инструкция по миграции с версии 1.x.x)](https://github.com/SecondThundeR/shikithon/wiki/%D0%9C%D0%B8%D0%B3%D1%80%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%81-v1-%D0%BD%D0%B0-v2)_

## Описание

Данный враппер предоставляет абстракцию, которая позволяет удобнее работать с методами API и их ответами

Для каждого эндпоинта API существует свой объект с методами, и все данные, возвращаемые API Shikimori, валидируются и парсятся в модели, со всеми необходимыми полями,
а также дополнительными, которые могут вернуть некоторые методы API _(Например /users/whoami и /users/:id/info возвращают разные поля)_.
Это позволяет не задумываться об обработке очередного ответа от сервера и сосредоточиться над реализацией своей идеи

Также благодаря множеству проверок при взаимодействии с запросами, библиотека старается добиться максимально
безопасной работы с API: все ошибки API, переданных параметров, данных и т.д. обратываются, логируются и
пользователю возвращаются значения по умолчанию

> Данная библиотека начинает свою поддержку с Python 3.8.10.

## Установка

```shell
pip install shikithon

# или используя Poetry
poetry add shikithon
```

## Пример использования

```py
import asyncio

from typing import Dict

from json import loads

from shikithon import ShikimoriAPI, JSONStore

# При необходимости, можно также
# экспортировать енамы для использования в методах
from shikithon.enums import AnimeOrder, MangaKind, ...

# Можно установить данные конфигурации в коде
config = {
    "app_name": "...",
    "client_id": "...",
    "client_secret": "...",
    "auth_code": "...",
    # Необязательно
    "access_token": "...",
    "refresh_token": "..."
}

# Или же прочитать его из внешнего файла
with open("config.json", "r", encoding="utf-8") as config_file:
    config_2: Dict[str, str] = loads(config_file.read())

# Инициализируем API объект с необходимыми опциями
# В данном примере используется JSONStore и отключено логирование
api = ShikimoriAPI(app_name=config['app_name'], store=JSONStore())

async def main():
    # Используем объект без авторизации
    async with api:
        lycoris = await api.animes.get(50709)
        print(lycoris)
        # >> id=50709 name='Lycoris Recoil' russian='Ликорис Рикоил' ...

        # Важно отметить, что внутри нельзя вкладывать async with api.auth(...)

    # Используем объект с авторизацией
    # Вариант 1
    async with api.auth(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        auth_code=config["auth_code"],
    ):
        print(await api.users.current())
        # >> id=723052, nickname='SecondThundeR', ...

    # Вариант 2

    # Создаем новый объект API
    # (По умолчанию используется NullStore в качестве хранилища)
    api_2 = ShikimoriAPI(app_name="...")

    # В данном случае app_name в __init__ не будет перезаписан,
    # а токен будет обновлен при ошибке 401
    api_auth_maker = api_2.auth(
        app_name=config['app_name'],
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        access_token=config['access_token'],
        refresh_token=config['refresh_token']
    )

    # Далее созданный объект можно использовать сколько угодно раз
    async with api_auth_maker:
        ...

asyncio.run(main())
```

Выполнение нескольких запросов одновременно с помощью метода `multiple_requests`:

```py
# В этом примере используется распаковка, но можно также получать весь массив с данными ответов
# в одной переменнной (chainsaw, lycoris_anime, ... -> data = await ...)
from shikithon import ShikimoriAPI, JSONStore

config = ...

api = ShikimoriAPI(app_name=config['app_name'], store=JSONStore(), logging=False)

async def main():
    async with api:
        chainsaw, lycoris_chisato, lycoris_ranobe = await api.multiple_requests([
            api.animes.get_all(search="Бензопила"),
            api.characters.search("Тисато Нисикиги"),
            api.ranobes.get_all(search="Ликорис"),
        ])
        print(chainsaw)
        print(lycoris_chisato[:1])
        print(lycoris_ranobe)

# [AnimeInfo(id=44511, name='Chainsaw Man', russian='Человек-бензопила', ...]
# [CharacterInfo(id=204621, name='Chisato Nishikigi', russian='Тисато Нисикиги', ...]
# [RanobeInfo(id=151431, name='Lycoris Recoil: Ordinary Days', russian='Ликорис Рикоил: Повседневность', ...]
```

Также, если хочется узнать как использовать встроенные хранилища конфигов или хочется создать свой,
посмотрите [этот гайд](https://github.com/SecondThundeR/shikithon/wiki/%D0%93%D0%B0%D0%B9%D0%B4-%D0%BF%D0%BE-%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B0%D0%BC-%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%D1%83%D1%80%D0%B0%D1%86%D0%B8%D0%B8)

### Пара уточнений по использованию

- Возможно вам придется импортировать модели для ручной аннотации возвращаемых моделей в PyCharm
_(в нем немного некорретно работает наследование типа от функции)_
- При отсутствии каких-либо полей в данных конфигурации, библиотека выдает исключение
- Если вы хотите использовать логгирование библиотеки, передайте флаг `logging=True` в объект API:
`api = ShikimoriAPI(app_name="...", logging=True)`

## Получение данных для конфигурации

Для начала вам необходимо создать новое OAuth-приложение [здесь](https://shikimori.me/oauth/applications).
После этого, сохраните `app_name`, `client_id`, `client_secret`, а так же `redirect_uri`, если вы его меняли

Позже, [на данной странице](https://shikimori.me/oauth) выберите свое приложение, необходимые разрешения
и получите код авторизации и сохраните его.
_(Если необходимо, то можно также получить токены авторизации, пройдя следующий этап после получения кода авторизации)_

## Список изменений

Все изменения перечислены на [странице релизов](https://github.com/SecondThundeR/shikithon/releases)

## Помощь проекту

Хотите внести вклад или оставить репорт о баге? Великолепно!

Для таких случаев, стоит почитать [CONTRIBUTING.md](https://github.com/SecondThundeR/shikithon/blob/main/CONTRIBUTING.md)

## Зависимости проекта

Данный проект использует семь библиотек:

- [aiohttp](https://github.com/aio-libs/aiohttp) для асинхронных запросов к API
[(Лицензия)](https://github.com/aio-libs/aiohttp/blob/master/LICENSE.txt)
- [pydantic](https://github.com/samuelcolvin/pydantic/) для валидации данных JSON и преобразования в модели
[(Лицензия)](https://github.com/samuelcolvin/pydantic/blob/master/LICENSE)
- [pyrate-limiter](https://github.com/vutran1710/PyrateLimiter) для огранчений количества запросов к API
[(Лицензия)](https://github.com/vutran1710/PyrateLimiter/blob/master/LICENSE)
- [backoff](https://github.com/litl/backoff) для повторения запросов при их ограничении
[(Лицензия)](https://github.com/litl/backoff/blob/master/LICENSE)
- [loguru](https://github.com/Delgan/loguru) для удобного логгирования
[(Лицензия)](https://github.com/Delgan/loguru/blob/master/LICENSE)
- [validators](https://github.com/kvesteri/validators) для проверки строк на наличие ссылки в ней
[(Лицензия)](https://github.com/kvesteri/validators/blob/master/LICENSE)
- [typing-extensions](https://github.com/python/typing_extensions) для корректной типизации декораторов
[(Лицензия)](https://github.com/python/typing_extensions/blob/main/LICENSE)

Также, данный проект использует две библиотеки в качестве зависимостей для разработки:

- [pre-commit](https://github.com/pre-commit/pre-commit) для автоматизации форматирования и проверки кода
[(Лицензия)](https://github.com/pre-commit/pre-commit/blob/main/LICENSE)
- [mypy](https://github.com/python/mypy) для проверки типов [(Лицензия)](https://github.com/python/mypy/blob/master/LICENSE)

## Лицензия проекта

Данный проект имеет MIT лицензию.
Ознакомиться с ее содержанием можно [здесь](https://github.com/SecondThundeR/shikithon/blob/main/LICENSE)

Проект использует логотип сайта [Shikimori](https://shikimori.org) для логотипа в этом README.md.
Все права принадлежат правообладателям и используются по принципу _fair use_

## Благодарности

- [shiki4py](https://github.com/ren3104/Shiki4py) - взяты некоторые идеи по рефакторингу и добавлению поддержки асинхронных запросов
[(Лицензия)](https://github.com/ren3104/Shiki4py/blob/main/LICENSE)
