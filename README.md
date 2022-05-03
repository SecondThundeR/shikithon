<div align="center">
    <!-- Not a final logo :( (or not?) -->
    <img src="https://raw.githubusercontent.com/SecondThundeR/shikithon/main/assets/logo.png">
    <h1>Shikithon</h1>
    <p>Очередной враппер для Shikimori API, написанный на Python</p>
</div>

> Данная библиотека находится на ранней стадии разработки.
>
> **Большинство** функционала отстуствует на данный момент и, возможно, текущий функционал может иметь баги.
>
> На данный момент, использовать библиотеку как базу для вашего приложения стоит на свой страх и риск
> (Или если есть большое желание проверить работоспособность этой библиотеки).

## Преимущество библиотеки

Данный враппер предоставляет базовую абстракцию, которая позволяет удобнее работать с методами API и их ответами.

Для каждого метода API существует свой метод класса, который благодаря библиотеке Pydantic,
возвращает удобную модель данных.

Все данные JSON формата, возвращаемые API Shikimori, валидируются и парсятся в модели, со всеми необходимыми полями,
а также дополнительными, которые могут вернуть некоторые методы API.

Это позволяет не задумываться об обработке очередного ответа от сервера и сосредоточиться воплощать любые идеи.

Также, данная библиотека начинает свою поддержку с Python 3.8, что не требует обязательного обновления
до самой новой версии Python.

> Поддержка Python 3.6 не имеет смысла, так как она не является актуальной на момент разработки, а Python 3.7
> не поддерживается на Apple Silicon _(Основная платформа, на которой разрабатывается данная библиотека)_.
> 
> Поэтому в качестве минимальной версии и был выбран Python 3.8.

## Установка

 ```pip install shikithon```

## Пример использования

```py
from json import loads
# Необязательно
from typing import Dict
# Необязательно
from typing import List

from shikithon.api import API

# Необязательно
from shikithon.models.achievement import Achievement
# Необязательно
from shikithon.models.user import User

# Можно установить данные конфигурации в коде
config: Dict[str, str] = {
    "app_name": "...",
    "client_id": "...",
    "client_secret": "...",
    "redirect_uri": "...",
    "scopes": "...",
    "auth_code": "..."
}

# Или же прочитать его из внешнего файла
with open("config.json", "r", encoding="utf-8") as config_file:
    config_2 = loads(config_file.read())

# Инициализация объекта API
shikimori: API = API(config)

# Получение данных текущего пользователя через /users/whoami
user: User = shikimori.current_user()
print(f"Current user is {user.nickname}")

# Получение достижений пользователя через /achievements
# и вывод первого достижения
user_achievements: List[Achievement] = shikimori.achievements(
    user.id
)
print(user_achievements[0])

# >> Current user is SecondThundeR
# >> id=719972946
# >> neko_id='animelist'
# >> level=1 progress=77
# >> user_id=723052
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
>  Пример: `user_rates+messages+comments+topics+...`
> - При отсутствии каких-либо полей в данных конфигурации, библиотека выдает исключение

### Получение данных для конфигурации

Для начала вам необходимо создать новое OAuth-приложение [здесь](https://shikimori.one/oauth/applications)
*(После этого, сохраните `app_name`, `client_id`, `client_secret`, а так же `redirect_uri`)*

Позже, [на данной странице](https://shikimori.one/oauth) выберите свое приложение, необходимые разрешения
и получите код авторизации *(После этого сохраните, `scopes` и `auth_code`)*

**Теперь ваш файл конфигурации готов!**

> На первой инициализации, библиотека создаст кэш конфигурации в скрытом файле для дальнейших запросов.
> Если токены станут недоступны, библиотека автоматически обновит токены и кэшированный файл конфигурации

## Список изменений

Все изменения перечислены на [странице релизов](https://github.com/SecondThundeR/shikithon/releases)

## Помощь проекту

Хотите внести вклад или оставить репорт о баге? Великолепно!

Для таких случаев, стоит почитать [CONTRIBUTING.md](https://github.com/SecondThundeR/shikithon/blob/feature/major-rewrite/CONTRIBUTING.md)

## Зависимости проекта

Данный проект использует три библиотеки:

- [requests](https://github.com/psf/requests) для запросов к API
[(Лицензия)](https://github.com/psf/requests/blob/main/LICENSE)
- [pydantic](https://github.com/samuelcolvin/pydantic/) для валидации данных JSON и преобразования в модели
[(Лицензия)](https://github.com/samuelcolvin/pydantic/blob/master/LICENSE)
- [ratelimit](https://github.com/tomasbasham/ratelimit) для огранчений количества запросов в минуту
[(Лицензия)](https://github.com/tomasbasham/ratelimit/blob/master/LICENSE.txt)

## Лицензия проекта

Данный проект имеет MIT лицензию.
Ознакомиться с ее содержанием можно [здесь](https://github.com/SecondThundeR/shikithon/blob/main/LICENSE)
