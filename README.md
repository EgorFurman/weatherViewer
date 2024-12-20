# Проект “Погода”

Веб-приложение для просмотра текущей погоды. Пользователь может зарегистрироваться и добавить в коллекцию одну или несколько локаций (городов, сёл, других пунктов), после чего главная страница приложения начинает отображать список локаций с их текущей погодой.

[Тз проекта](https://zhukovsd.github.io/python-backend-learning-course/Projects/WeatherViewer/)

## Установка и запуск
1. Склонируйте репозиторий:
	```shell
	git clone https://github.com/EgorFurman/weatherViewer.git
	```

2. Установите Docker:  
	- [Инструкции по установке Docker](https://docs.docker.com/desktop/)

3. Сконфигурируйте `.env` в соответствие с примером
	```
		WEATHER_API_KEY=YOUR_OPEN_WEATHER_API_KEY # Уникальный ключ OpenWeatherAPI
		
		# Конфигурация Postgres
		POSTGRES_DB=weather # Имя БД
		POSTGRES_USER=django_user # Имя пользователя БД
		POSTGRES_PASSWORD=1234 # Пароль пользователя БД
		POSTGRES_HOST=db # Имя контейнера БД. По умолчанию db
		POSTGRES_PORT=5432 # Порт БД
		
		# Конфигурация Django
		DJANGO_SECRET_KEY=YOUR_DJANGO_SECRET_KEY # Cекретный ключ Django
		DJANGO_DEBUG=False # Режим отладки(False - выключен, True - включен)
		DJANGO_ALLOWED_HOSTS=* # Список доменов или айпишников, которые может обслуживать приложение
		
		# Конфигурация Nginx
		NGINX_EXTERNAL_PORT=80 # Порт для подключения к приложению
	```

4. Запустите проект:
	- **Для dev версии проекта**
	    ```shell
	     docker-compose -f docker-compose.dev.yml up -d --build
	    ```
	- **Для prod версии проекта**
	    ```shell
	     docker-compose -f docker-compose.prod.yml up -d --build
	    ```

## Интерфейс
### **Авторизация**
Адрес - `/users/login`. Страница представляет собой форму для авторизации пользователя.
![auth](https://github.com/EgorFurman/weatherViewer/blob/master/docs/login.png)
### **Регистрация**
Адрес - `/users/register`. Страница представляет собой форму для регистрации пользователя.
![auth](https://github.com/EgorFurman/weatherViewer/blob/master/docs/register.png)
### **Главная страница**
Адрес - `/`. Страница представляет собой главную страницу приложения.
![auth](https://github.com/EgorFurman/weatherViewer/blob/master/docs/main.png)
### **Страница результатов поиска**
Адрес - `/search`. Представляет собой коллекцию из найденных по имени населенных пунктов. GET параметр `location` содержит имя локации.
![auth](https://github.com/EgorFurman/weatherViewer/blob/master/docs/search.png)

## Тесты
В качестве фреймворка для тестирования был использован unittest. Юнит и интеграционным тестами был покрыт основной функционал приложения. Основные тест-кейсы:
- Проверка работы внешнего API. Сервис по работе с OpenWeatherAPI покрыт Мок-тестами.
- Проверка работы форм авторизации и регистрации пользователя.
- Проверка работы контроллеров авторизации и регистрации пользователя.
- Интеграционный тест полного процесса регистрации и авторизации пользователя.

## Стек
- Python 3.12
- Django 5.1.2
- PostgreSQL
- docker
- unittest
- requests
- HTML/CSS(Bootstrap5)
