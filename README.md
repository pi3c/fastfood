# fastfood
Fastapi веб приложение реализующее api для общепита.

## Оглавление

<a href="#description">Описание</a>

<a name="description"></a>
## Описание
Данный проект, это результат выполнения практического домашнего задания интенсива от YLAB Development. Проект реализован на фреймворке fastapi, с использованием sqlalchemy. В качестве базы данных используется postgresql.

### Техническое задание
Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет приложена Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.
Даны 3 сущности: Меню, Подменю, Блюдо.

Зависимости:
- У меню есть подменю, которые к ней привязаны.
- У подменю есть блюда.

Условия:
- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
- Во время запуска тестового сценария БД должна быть пуста.

В папке ./postman_scripts находятся фалы тестов Postman, для тестирования функционала проекта.

## Возможности
В проекте реализованы 3 сущности: Menu, SubMenu и Dish. Для каждого них реализованы 4 метода http запросов: GET, POST, PATCH и DELETE c помощью которых можно управлять данными.
Для Menu доступен метод GET возвращающий все его SubMenu. Аналогично для SubMenu реализован метод для возврата всех Dish.


## Зависимости
- postgresql Для работы сервиса необходима установленная СУБД. Должна быть создана база данных и пользователь с правами на нее.
- poetry - Система управления зависимостями в Python.

Остальное добавится автоматически на этапе установки.

## Установка
### Linux
Установите и настройте postgresql согласно офф. документации. Создайте пользователя и бд. 

Установите систему управления зависимостями
> `$ pip[x] install poetry`

Клонируйте репозиторий
> `$ git clone https://git.pi3c.ru/pi3c/fastfood.git`

Перейдите в каталог

> `$ cd fastfood`

> `$ poetry install --no-root`

Создастся виртуальное окружение и установятся зависимости

Файл example.env является образцом файла .env, который необходимо создать перед запуском проекта.
В нем указанны переменные необходимые для подключения к БД.
Созданим файл .env

>`$ cp ./example.env ./.env`

Далее отредактируйте .env файл в соответствии с Вашими данными подключения к БД

## Запуск
Запуск проекта возможен в 2х режимах:
- Запуск в режиме "prod" с ключем --run-server
        Подразумевает наличие уже созданных таблиц в базе данных(например с помощью Alembic). Манипуляций со структурой БД не происходит. Данные не удаляются. 

- Запуск в режиме "dev" c ключем --run-test-server
        В этом случае при каждом запуске проекта все таблицы с данными удаляются из БД и создаются снова согласно описанных моделей.


Для запуска проекта сначала активируем виртуальное окружение

> `$ poetry shell`

и запускаем проект в соответстующем режиме

>`$ python[x] manage.py  --ключ`

вместо этого, так же допускается и другой вариант запуска одной командой без предварительной активации окружения

>`$ poetry run python[x] manage.py --ключ`


## TODO
-  Добавить миграции
-  Провести рефакторинг, много дублирующего кода
-  Много чего другого :)

## Авторы
-  Сергей Ванюшкин <pi3c@yandex.ru>

## Лицензия
Распространяется под [MIT лицензией](https://mit-license.org/).


