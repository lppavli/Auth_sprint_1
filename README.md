# Auth
Ссылка на репозиторий - https://github.com/lppavli/Auth_sprint_1

# Основные сущности
- Пользователи - логин, пароль, является ли суперюзером, роль.
- Роль - имя.
- Пользователь-Роль - пользователь, роль.
- История аутентификации - пользователь, клиент входа (агент), ip-адрес, дата и время посещения.

# Основные компоненты системы
- Cервер WSGI — сервер с запущенным приложением.
- Nginx — прокси-сервер, который является точкой входа для веб-приложения.
- PostgreSQL — хранилище данных, в котором лежит вся необходимая информация для сервса.
- Redis — хранилище данных для токенов.
- SQLAlchemy - используется как ORM.
# Используемые технологии
- Flask + gevent
- PostgreSQL
- Redis
- Docker
- Pytest
- SQLAlchemy
# Запуск приложения
```
docker-compose up -d- --build 
```
# Миграции
```
docker exec -it auth cd auth && alembic upgrade head
```
# Документация доступна по адресу
http://127.0.0.1/apidocs/
# Создание суперпользователя
```
docker exec -it auth cd auth && flask superuser create <login> <password>
```
# Тестирование
```
docker-compose -f docker-compose-test.yml up -d- --build
```
# Проектная работа 6 спринта

С этого модуля вы больше не будете получать чётко расписанное ТЗ, а задания для каждого спринта вы найдёте внутри уроков. Перед тем как начать программировать, вам предстоит продумать архитектуру решения, декомпозировать задачи и распределить их между командой.

В первом спринте модуля вы напишете основу вашего сервиса и реализуете все базовые требования к нему. Старайтесь избегать ситуаций, в которых один из ваших коллег сидит без дела. Для этого вам придётся составлять задачи, которые можно выполнить параллельно и выбрать единый стиль написания кода.

К концу спринта у вас должен получиться сервис авторизации с системой ролей, написанный на Flask с использованием gevent. Первый шаг к этому — проработать и описать архитектуру вашего сервиса. Это значит, что перед тем, как приступить к разработке, нужно составить план действий: из чего будет состоять сервис, каким будет его API, какие хранилища он будет использовать и какой будет его схема данных. Описание нужно сдать на проверку. Вам предстоит выбрать, какой метод организации доступов использовать для онлайн-кинотеатра, и систему прав, которая позволит ограничить доступ к ресурсам. 

Для описания API рекомендуем использовать [OpenAPI](https://editor.swagger.io){target="_blank"}, если вы выберете путь REST. Или используйте текстовое описание, если вы планируете использовать gRPC. С этими инструментами вы познакомились в предыдущих модулях. Обязательно продумайте и опишите обработку ошибок. Например, как отреагирует ваш API, если обратиться к нему с истёкшим токеном? Будет ли отличаться ответ API, если передать ему токен с неверной подписью? А если имя пользователя уже занято? Документация вашего API должна включать не только ответы сервера при успешном завершении запроса, но и понятное описание возможных ответов с ошибкой.

После прохождения ревью вы можете приступать к программированию. 

Для успешного завершения первой части модуля в вашем сервисе должны быть реализованы API для аутентификации и система управления ролями. Роли понадобятся, чтобы ограничить доступ к некоторым категориям фильмов. Например, «Фильмы, выпущенные менее 3 лет назад» могут просматривать только пользователи из группы 'subscribers'.  

## API для сайта и личного кабинета

- регистрация пользователя;
- вход пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh токен); 
- обновление access-токена;
- выход пользователя из аккаунта;
- изменение логина или пароля (с отправкой email вы познакомитесь в следующих модулях, поэтому пока ваш сервис должен позволять изменять личные данные без дополнительных подтверждений);
- получение пользователем своей истории входов в аккаунт;

## API для управления доступами

- CRUD для управления ролями:
  - создание роли,
  - удаление роли,
  - изменение роли,
  - просмотр всех ролей.
- назначить пользователю роль;
- отобрать у пользователя роль;
- метод для проверки наличия прав у пользователя. 

## Подсказки

1. Продумайте, что делать с анонимными пользователями, которым доступно всё, что не запрещено отдельными правами.
2. Метод проверки авторизации будет всегда нужен пользователям. Ходить каждый раз в БД — не очень хорошая идея. Подумайте, как улучшить производительность системы.
3. Добавьте консольную команду для создания суперпользователя, которому всегда разрешено делать все действия в системе.
4. Чтобы упростить себе жизнь с настройкой суперпользователя, продумайте, как сделать так, чтобы при авторизации ему всегда отдавался успех при всех запросах.
5. Для реализации ограничения по фильмам подумайте о присвоении им какой-либо метки. Это потребует небольшой доработки ETL-процесса.


## Дополнительное задание

Реализуйте кнопку «Выйти из остальных аккаунтов», не прибегая к хранению в БД активных access-токенов.

## Напоминаем о требованиях к качеству

Перед тем как сдать ваш код на проверку, убедитесь, что 

- Код написан по правилам pep8: при запуске [линтера](https://semakin.dev/2020/05/python_linters/){target="_blank"} в консоли не появляется предупреждений и возмущений;
- Все ключевые методы покрыты тестами: каждый ответ каждой ручки API и важная бизнес-логика тщательно проверены;
- У тестов есть понятное описание, что именно проверяется внутри. Используйте [pep257](https://www.python.org/dev/peps/pep-0257/){target="_blank"}; 
- Заполните README.md так, чтобы по нему можно было легко познакомиться с вашим проектом. Добавьте короткое, но ёмкое описание проекта. По пунктам опишите как запустить приложения с нуля, перечислив полезные команды. Упомяните людей, которые занимаются проектом и их роли. Ведите changelog: описывайте, что именно из задания модуля уже реализовано в вашем сервисе и пополняйте список по мере развития.
- Вы воспользовались лучшими практиками описания конфигурации приложений из урока. 
