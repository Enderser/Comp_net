# Comp_net
## Task 1: ping
Пингануть 10 адресов, результаты записать в .csv (какие конкретно данные - решайте сами)
## Task 2: SSH
2.1 Подключение к удаленному серверу через ssh БЕЗ ПАРОЛЯ
2.2 ПУШ В удаленный репозиторий через ssh БЕЗ ПАРОЛЯ
результат выполнения будет проверяться либо лично на паре, либо присылайте скриншоты.
# Task 3: Parser
Написать скрипт - парсер, ИСПОЛЬЗУЯ SELENIUM.
Обязательно должен иметь пагинацию
Желательно авторизацию
Парсим что угодно, новостной сайт, интернет-магазин, без разницы.
Параметров сохраняет не менее 4ёх.
Записывает всё в csv файл.
# Task 4: API
Поднять API точку, перейдя по которой, или дернув через curl, передав в параметре url (например: 127.0.0.1/parse?url=https://site.com/page), запустится ваш парсер, отработает, запишет результат в базу PostgresSQL (можно и другую, но не SQlite)
отдельным методом должны извлекаться данные из ТАБЛИЦЫ БД и отдаваться в виде json
# Task 5: Docker
Развернуть отдельно 2 докер контейнера, (БЕЗ  docker-compose) и настроить сеть между ними,
- 1ый контейнер - ваше приложение (на порту отличном от 80)
- 2ой контейнер - база данных

p.s. Вырезать парсер, первый метод с url теперь просто записывает этот url в базу данных, а второй метод возвращает все url, которые есть в бд