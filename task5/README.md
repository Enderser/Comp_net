# Task 5: Docker
Развернуть отдельно 2 докер контейнера, (БЕЗ  docker-compose) и настроить сеть между ними,
- 1ый контейнер - ваше приложение (на порту отличном от 80)
- 2ой контейнер - база данных

p.s. Вырезать парсер, первый метод с url теперь просто записывает этот url в базу данных, а второй метод возвращает все url, которые есть в бд
# Комментарии по запуску
1. Создайте сеть 
   ```
	docker network create my-network
	```
2. Запустите контейнер db
   ```
	docker run -d --name db --network my-network -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydb -p 5432:5432 postgres:latest
	```
3.  Соберите контейнер
	```
	docker build -t my-app .
	```
	В случае проблем с доступом PyPl, добавьте ```--no-cache``` в конце.
4. Запустите контейнер my-app
	```
	docker run -d --name my-app --network my-network -p 8080:8080 my-app
	```
5. Проверьте работу контейнеров (необязательно)
	```
	docker ps
	```
	Ожидается:
	- db на порту 5432.
	- my-app на порту 8080.
6. Работа приложения
   
	1. Добавить URL:
		```
		curl -X POST "http://localhost:8080/urls/" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
		```
		Ожидаемый ответ:
		```
		{"message": "URL added", "url": "https://example.com"}
		```
	2. Получить все URL:
		```
		curl "http://localhost:8080/urls/"
		```
		Ожидаемый ответ (добавлен один URL):
		```
		[{"id": 1, "url": "https://example.com"}]
		```
	3. Проверка уникальности:
		```
		curl -X POST "http://localhost:8080/urls/" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
		```
		Ожидаемый ответ:
		```
		{"error": "URL already exists"}
		```
8. Очистка
	```
	docker stop my-app db
	docker rm my-app db
	docker network rm my-network
	docker rmi my-app
	```
	
