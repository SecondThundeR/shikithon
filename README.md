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

Данный враппер предоставляет базовую абстракцию, которая позволяет удобнее работать с методами API и их ответами.

Для каждого эндпоинта API существует свой объект с методами, которые благодаря библиотеке Pydantic,
возвращают удобную модель данных.

Все данные, возвращаемые API Shikimori, валидируются и парсятся в модели, со всеми необходимыми полями,
а также дополнительными, которые могут вернуть некоторые методы API _(Например /users/whoami и /users/:id/info возвращают разные поля)_.
Это позволяет не задумываться об обработке очередного ответа от сервера и сосредоточиться над реализацией своей идеи.

Также благодаря многочисленным проверкам при взамодействии с запросами, библиотека старается добиться максимально
безопасной работы с API: все ошибки API, переданных параметров, данных и т.д. обратываются и логируются и
возвращаются значения по умолчанию

> Данная библиотека начинает свою поддержку с Python 3.8.10.

## Установка

 ```pip install shikithon```

## Пример использования

С использованием полного конфига:

```py
import asyncio

from typing import Dict

from json import loads

from shikithon import ShikimoriAPI

# Можно установить данные конфигурации в коде
config = {
    "app_name": "...",
    "client_id": "...",
    "client_secret": "...",
    "redirect_uri": "...",
    "scopes": "...",
    "auth_code": "..."
}

# Или же прочитать его из внешнего файла
with open("config.json", "r", encoding="utf-8") as config_file:
    config_2: Dict[str, str] = loads(config_file.read())

async def main():
    # Инициализация объекта API
    shikimori = ShikimoriAPI(config)

    # Запуск сессии
    await shikimori.open()

    # Получение данных текущего пользователя через /users/whoami
    user = await shikimori.users.current()
    print(f"Current user is {user.nickname}")

    # Получение достижений пользователя через /achievements
    # и вывод первого достижения
    user_achievements = await shikimori.achievements.get(user.id)
    if user_achievements:
            print(user_achievements[0])

    # Закрытие сессии
    await shikimori.close()

asyncio.run(main())

# >> Current user is SecondThundeR

# >> id=719972946
# >> neko_id='animelist'
# >> level=1
# >> progress=77
# >> user_id=723052
# >> created_at=datetime.datetime(...)
# >> updated_at=datetime.datetime(...)

# На самом деле достижение выводится как одна строка с данными.
# Для удобства она показана здесь раздельно
```

С использованием имени приложения:

```py
import asyncio

from shikithon import ShikimoriAPI

# Можно установить имя приложения в коде
app_name = "..."

# Или же прочитать его из внешнего файла
with open("config.txt", "r", encoding="utf-8") as config_file:
    app_name_2 = config_file.readline().strip()

async def main():
    # Инициализация объекта API
    async with ShikimoriAPI(app_name) as shikimori:
        # Попытка получения данных текущего пользователя через /users/whoami
        # При попытке доступа к защищенному методу, возвращает всегда None
        user = await shikimori.users.current()
        print(user)

        # Получение достижений пользователя через /achievements
        # и вывод первого достижения
        # Можно получать достижения любого пользователя через ID
        user_achievements = await shikimori.achievements.get(1)
        if user_achievements:
            print(user_achievements[0])

asyncio.run(main())

# >> None

# >> id=811883697
# >> neko_id='aa_megami_sama'
# >> level=0
# >> progress=31
# >> user_id=1
# >> created_at=datetime.datetime(...)
# >> updated_at=datetime.datetime(...)

# На самом деле достижение выводится как одна строка с данными.
# Для удобства она показана здесь раздельно
```

Выполнение нескольких запросов одновременно с помощью метода multiple_requests:
```py
# В этом примере используется распаковка, но можно также получать весь массив с данными ответов
# в одной переменнной (chainsaw, lycoris_anime, ... -> data = await ...)
from shikithon import ShikimoriAPI

config = ...

shikimori = ShikimoriAPI(config)
await shikimori.open()

chainsaw, lycoris_chisato, lycoris_ranobe = await shikimori.multiple_requests([
    shikimori.animes.get_all(search="Бензопила"),
    shikimori.characters.search("Тисато Нисикиги"),
    shikimori.ranobes.get_all(search="Ликорис"),
])
print(chainsaw)
print(lycoris_chisato[:1])
print(lycoris_ranobe)

await shikimori.close()

# [Anime(id=44511, name='Chainsaw Man', russian='Человек-бензопила', ...]
# [Character(id=204621, name='Chisato Nishikigi', russian='Тисато Нисикиги', ...]
# [Ranobe(id=151431, name='Lycoris Recoil: Ordinary Days', russian='Ликорис Рикоил: Повседневность', ...]

# Также возможно использовать этот метод в "ограниченном режиме":
app_name = ...

async with ShikimoriAPI(app_name) as shikimori:
    lycoris_ranobe, = await shikimori.multiple_requests([
        shikimori.ranobes.get_all(search="Ликорис")
    ])
    print(lycoris_ranobe)

# [Ranobe(id=151431, name='Lycoris Recoil: Ordinary Days', russian='Ликорис Рикоил: Повседневность', ...]
```

> **Пара уточнений по использованию:**
>
> - Возможно вам придется импортировать модели для ручной аннотации возвращаемых моделей в PyCharm
> _(в нем немного некорретно работает наследование типа от функции)_
>
>
> - Поле `scopes` является строкой и разделяется "+", если значений несколько.
>
>   Пример: `user_rates+messages+comments+topics+...`
>
>
> - При отсутствии каких-либо полей в данных конфигурации, библиотека выдает исключение
>
>
> - Если вы не хотите использовать логгирование библиотеки, передайте флаг logging=False в объект API.
>
>  Пример: `shikithon = ShikimoriAPI(config, logging=False)`

### Получение данных для конфигурации

Для начала вам необходимо создать новое OAuth-приложение [здесь](https://shikimori.one/oauth/applications)
_(После этого, сохраните `app_name`, `client_id`, `client_secret`, а так же `redirect_uri`)_

Позже, [на данной странице](https://shikimori.one/oauth) выберите свое приложение, необходимые разрешения
и получите код авторизации _(После этого сохраните, `scopes` и `auth_code`)_

**Теперь ваш файл конфигурации готов!**

> На первой инициализации, библиотека создаст и сохранит собственный файл конфигурации для дальнейших запросов.
> Если токены станут недоступны, библиотека автоматически обновит токены и сохранненый файл конфигурации

Также возможно использование библиотеки в "ограниченном режиме",
используя только имя приложения для доступа к публичным методам API.

В таком случае, вы должны только передать строку с `app_name` для дальнейшей работы, как в примере выше.

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

В качестве зависимостей для разработки, проект использует четыре библиотеки:

- [pylint](https://github.com/PyCQA/pylint) для статической проверки кода
[(Лицензия)](https://github.com/PyCQA/pylint/blob/main/LICENSE)
- [yapf](https://github.com/google/yapf) для форматирования кода
[(Лицензия)](https://github.com/google/yapf/blob/main/LICENSE)
- [isort](https://github.com/PyCQA/isort) для сортировки импортов
[(Лицензия)](https://github.com/PyCQA/isort/blob/main/LICENSE)
- [pre-commit](https://github.com/pre-commit/pre-commit) для автоматизации проверки с использованием библиотек выше :)
[(Лицензия)](https://github.com/pre-commit/pre-commit/blob/main/LICENSE)

## Лицензия проекта

Данный проект имеет MIT лицензию.
Ознакомиться с ее содержанием можно [здесь](https://github.com/SecondThundeR/shikithon/blob/main/LICENSE)

Проект использует логотип сайта [Shikimori](https://shikimori.org) для логотипа в этом README.md.
Все права принадлежат правообладателям и используются по принципу _fair use_.

## Благодарности

- [shiki4py](https://github.com/ren3104/Shiki4py) - взяты некоторые идеи по рефакторингу и добавлению поддержки асинхронных запросов
[(Лицензия)](https://github.com/ren3104/Shiki4py/blob/main/LICENSE)
