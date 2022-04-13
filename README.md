<div align="center">
    <!-- Not a final logo :( -->
    <img src="assets/logo.png">
    <h1>Shikithon</h1>
    <p>Очередной враппер для Shikimori API, написанный на Python</p>
</div>

> Данная библиотека находится в активной стадии разработки ~~и является плодом больной фантазии автора~~
>
> Это значит, что **скорее всего** большинство  функционала отстуствует на данный момент, или тот, что присутствует, может работать непредсказуемо.
>
> Использовать можно на свой *страх и риск*... ну или есть большое желание проверить работу этой библиотеки

## В чем же фишка?

Данный враппер предоставляет базовую абстракцию, которая позволяет удобнее работать с методами API и их ответами

Благодаря библиотеке Pydantic, все данные JSON формата, возвращаемые API Shikimori, конвертируются в модели, которые имеют все необходимые поля, которые могут быть возвращены сервером, а также дополнительные, которые могут вернуть некоторые методы

Используя данное преимущество, можно воплощать любые идеи, не задумываясь о том, что вернет очередной метод

## Пример использования

```py
from shikithon.api import API

from shikithon.models.Achievement import Achievement
from shikithon.models.User import User

# Конфигурация в коде
config: dict[str, str] = {
    "app_name": "...",
    "client_id": "...",
    "client_secret": "...",
    "redirect_uri": "...",
    "scopes": "...",
    "auth_code": "...",
    "access_token": "...",
    "refresh_token": "..."
}

# Или можно прочитать конфиг из файла
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Инициализация объекта API
api: API = API(config)

# Получение текущего пользователя через /users/whoami
current_user: User = api.get_current_user()
# >> Current user is SecondThundeR
print(f"Current user is: {current_user.nickname}")

# Получение достижений пользователя через /achievements
user_achievements: list[Achievement] = api.get_achievements(
    current_user.id
)

# На самом деле выводится одна строка с данными полей.
# Для удобства они выведены здесь раздельно

# >> id=719972946
# >> neko_id='animelist'
# >> level=1
# >> progress=77
# >> user_id=723052
# >> created_at=datetime.datetime(2020, 12, 15, ...)
# >> updated_at=datetime.datetime(2022, 4, 11, ...)
print(user_achievements[0])
```

> Пара уточнений:
> - Не обязательно импортировать модели, если вы не используете функцию аннотации типов
> - Поле `scopes` является строкой и разделяется "+", если значений несколько. Пример: `user_rates+messages+comments+topics+...`
> - При отсутсвии каких-либо критических полей, библиотека завершает работу и выводит информацию о том, чего не хватило

## Как установить?

На данный момент, этот проект не был ещё залит на PyPI, поэтому для установки библиотеки обратитесь на пункт ниже

## Как собрать?

В первую очередь, убедитесь, что у вас стоят свежие `setuptools` и `wheel` и склонирован данный репозиторий

После этого, запустите в терминале команду:

```bash
pip install .
```

Это соберет всю библиотеку и установит ее сразу

Если же необходимо собрать `dist`-версию библиотеки, запустите:

```bash
python3 setup.py check && python3 setup.py sdist
```

## О зависимостях

Данный проект использует две библиотеки:

- [requests](https://github.com/psf/requests) для запросов к API
- [pydantic](https://github.com/samuelcolvin/pydantic/) для валидации данных JSON и преобразования в модели

## Лицензия?

Да! Данный проект имеет MIT лицензию. Ознакомиться с ее содержанием можно [здесь](https://github.com/SecondThundeR/shikithon/blob/main/LICENSE)
