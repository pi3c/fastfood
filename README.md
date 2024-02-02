# fastfood
Fastapi веб приложение реализующее api для общепита.

## Описание
Данный проект, это результат выполнения практических домашних заданий интенсива от YLAB Development. Проект реализован на фреймворке fastapi, с использованием sqlalchemy. В качестве базы данных используется postgresql.

## Техническое задание
### Спринт 1 - Создание API
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

### Спринт 2 - Docker && pytest
В этом домашнем задании надо написать тесты для ранее разработанных ендпоинтов вашего API после Вебинара №1.

Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде “docker-compose up -d” или той которая описана вами в readme.md.

Образы для Docker:
(API) python:3.10-slim
(DB) postgres:15.1-alpine

1.Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
2.Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в README.md
3.* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
4.** Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest
Если FastAPI синхронное - тесты синхронные, Если асинхронное - тесты асинхронные


*Оборачиваем приложение в докер.
**CRUD – create/update/retrieve/delete.

<a href="https://drive.google.com/drive/folders/13t6fsMO0B6Ls0qYl-uVgAHWOyhFTFv4Z?usp=sharing">Дополнительные материалы</a>

## Возможности
### Спринт 1
В проекте реализованы 3 сущности: Menu, SubMenu и Dish. Для каждого них реализованы 4 метода http запросов: GET, POST, PATCH и DELETE c помощью которых можно управлять данными.
Для Menu доступен метод GET возвращающий все его SubMenu. Аналогично для SubMenu реализован метод для возврата всех Dish.

### Спринт 2
- 1й пункт ТЗ
Тесты реализованы в виде 2х классов
`TastBaseCrud` включает 3 подкласса `Menu`, `Submenu`, `Dish` которые реализуют интерфейсы взаимодействия с endpoint'ами реализованных на предыдущем спринте сущностей. Каждый подкласс реализует методы GET(получение всех сущностей), Get(получение конкректной сущности), Post(создание), Patch(обновление), Delete(удаления). Так же в классе реализованы 3 тестовых функции, которые осуществляют тестирование соответствующих endpoint'ов
`TestContinuity` реализует последовательность сценария «Проверка кол-ва блюд и подменю в меню» из Postman

- 2й пункт ТЗ
Реализованы 3 контейнера(db, app, tests). В db написан блок "проверки здоровья", от которого зависят контейнеры app и test, который гарантирует, что зависимые контейнеры не будут запущены о полной готовности db.

- 3й пункт ТЗ
см. функцию `get_menu_item` на 28 строке в файле
<base_dir>/fastfood/crud/menu.py

- 4й пункт ТЗ
см. класс `TestContinuity` в файле
<base_dir>/tests/test_api.py

## Зависимости
Для локальной установки
- postgresql Для работы сервиса необходима установленная СУБД. Должна быть создана база данных и пользователь с правами на нее.
- poetry - Система управления зависимостями в Python.

Остальное добавится автоматически на этапе установки.

Для запуска в контейнере
- docker
- docker-compose

## Установка

Клонируйте репозиторий
> `$ git clone https://git.pi3c.ru/pi3c/fastfood.git`

Перейдите в каталог
> `$ cd fastfood`

Создадим файл .env из шаблона
>`$ cp ./example.env ./.env`

Если планируется запуск проекта в Docker контейнере, то `.env` можно не изменять. Если запуск будет локальным, то необходимо изменить переменные окружения, для подключения к БД postgres.

### Docker
Для запуска необходимы установленные приложения docker и docker-compose
Для теста изменять  файл .env не требуется.
Однако Вы можете изменить имя пользователя, пароль и имя базы данных по своему усмотрению.

И запустите образы:

- Запуск FAstAPI приложения
> `$ docker-compose -f compose_app.yml up `

По завершении работы остановите контейнеры
> `$ docker-compose -f compose_app.yml down`

После успешного запуска образов документация по API будет доступна по адресу <a href="http://localhost:8000/docs">http://localhost:8000</a>


- Запуск тестов
> `$ docker-compose -f compose_test.yml up`

По завершении работы остановите контейнеры
> `$ docker-compose -f compose_test.yml down`


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
-  Написать тесты для кривых данных
-  Провести рефакторинг, много дублирующего кода
-  Много чего другого :)

## Авторы
-  Сергей Ванюшкин <pi3c@yandex.ru>

## Лицензия
Распространяется под [MIT лицензией](https://mit-license.org/).
