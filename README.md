<!-- If PyCharm or IDEA will throw a warning here, just ignore it -->
<div align="center">
    <img src="https://raw.githubusercontent.com/SecondThundeR/shikithon/main/assets/logo.png" alt="Shikithon Logo">
    <h1>Shikithon</h1>
    <p>Очередной враппер для Shikimori API, написанный на Python</p>
</div>

[![Publish Shikithon package to PyPI](https://github.com/SecondThundeR/shikithon/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/SecondThundeR/shikithon/actions/workflows/pypi-publish.yml)

> **Состояние библиотеки:** завершена основная разработка
>
> На данный момент, библиотека поддерживает лишь синхронное взаимодействие с API,
> асинхронное взаимодействие и прочие улучшения будут добавлены в будущем

## Преимущество библиотеки

Данный враппер предоставляет базовую абстракцию, которая позволяет удобнее работать с методами API и их ответами.

Для каждого метода API существует свой метод класса, который благодаря библиотеке Pydantic,
возвращает удобную модель данных для работы.

Все данные, возвращаемые API Shikimori, валидируются и парсятся в модели, со всеми необходимыми полями,
а также дополнительными, которые могут вернуть некоторые методы API _(Например /users/whoami и /users/:id/info)_.

Это позволяет не задумываться об обработке очередного ответа от сервера и сосредоточиться над реализацией своей идеи.

Также, данная библиотека поддерживает ранние версии Python, начиная с 3.8.10.

> Поддержка Python 3.6.x не имеет смысла, так как она не является актуальной на момент разработки, а Python 3.7.x
> не поддерживается на Apple Silicon _(Основная платформа, на которой разрабатывается данная библиотека)_.
>
> Поэтому в качестве минимальной версии был выбран Python 3.8.10
## Установка

 ```pip install shikithon```

## Пример использования

С использованием полного конфига:

```py
from typing import Dict

from json import loads

from shikithon import API

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

# Инициализация объекта API
shikimori = API(config)

# Получение данных текущего пользователя через /users/whoami
user = shikimori.current_user()
print(f"Current user is {user.nickname}")

# Получение достижений пользователя через /achievements
# и вывод первого достижения
user_achievements = shikimori.achievements(user.id)
print(user_achievements[0])

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
from shikithon import API

# Можно установить имя приложения в коде
app_name = "..."

# Или же прочитать его из внешнего файла
with open("config.txt", "r", encoding="utf-8") as config_file:
    app_name_2 = config_file.readline().strip()

# Инициализация объекта API
shikimori = API(app_name)

# Попытка получения данных текущего пользователя через /users/whoami
# При попытке доступа к защищенному методу, возвращает всегда None
user = shikimori.current_user()
print(user)

# Получение достижений пользователя через /achievements
# и вывод первого достижения
# Можно получать достижения любого пользователя через ID
user_achievements = shikimori.achievements(1)
print(user_achievements[0])

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

> **Пара уточнений по использованию:**
>
> - Не обязательно импортировать модели, если вы не используете функцию аннотации типов
> - Поле `scopes` является строкой и разделяется "+", если значений несколько.
>
>   Пример: `user_rates+messages+comments+topics+...`
> - При отсутствии каких-либо полей в данных конфигурации, библиотека выдает исключение
> - Посмотреть список поддерживаемых методов API вместе с названиями для них в библиотеке, можно [здесь](https://github.com/SecondThundeR/shikithon/projects/1#column-18695394)

### Получение данных для конфигурации

Для начала вам необходимо создать новое OAuth-приложение [здесь](https://shikimori.one/oauth/applications)
_(После этого, сохраните `app_name`, `client_id`, `client_secret`, а так же `redirect_uri`)_

Позже, [на данной странице](https://shikimori.one/oauth) выберите свое приложение, необходимые разрешения
и получите код авторизации _(После этого сохраните, `scopes` и `auth_code`)_

**Теперь ваш файл конфигурации готов!**

> На первой инициализации, библиотека создаст кэш конфигурации в скрытом файле для дальнейших запросов.
> Если токены станут недоступны, библиотека автоматически обновит токены и кэшированный файл конфигурации

Также возможно использование библиотеки в "ограниченном режиме",
используя только имя приложения для доступа к публичным методам API.

В таком случае, вы должны только передать строку с `app_name` для дальнейшей работы, как в примере выше.

## Список изменений

Все изменения перечислены на [странице релизов](https://github.com/SecondThundeR/shikithon/releases)

## Помощь проекту

Хотите внести вклад или оставить репорт о баге? Великолепно!

Для таких случаев, стоит почитать [CONTRIBUTING.md](https://github.com/SecondThundeR/shikithon/blob/main/CONTRIBUTING.md)

## Зависимости проекта

Данный проект использует пять библиотек:

- [requests](https://github.com/psf/requests) для запросов к API
[(Лицензия)](https://github.com/psf/requests/blob/main/LICENSE)
- [pydantic](https://github.com/samuelcolvin/pydantic/) для валидации данных JSON и преобразования в модели
[(Лицензия)](https://github.com/samuelcolvin/pydantic/blob/master/LICENSE)
- [ratelimit](https://github.com/tomasbasham/ratelimit) для огранчений количества запросов в минуту
[(Лицензия)](https://github.com/tomasbasham/ratelimit/blob/master/LICENSE.txt)
- [loguru](https://github.com/Delgan/loguru) для удобного логгирования
[(Лицензия)](https://github.com/Delgan/loguru/blob/master/LICENSE)
- [validators](https://github.com/kvesteri/validators) для проверки строк на наличие ссылки в ней
[(Лицензия)](https://github.com/kvesteri/validators/blob/master/LICENSE)

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
