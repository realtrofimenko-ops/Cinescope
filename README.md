# 🎬 Cinescope API Tests

Автоматизированные тесты для API сервиса Cinescope (эндпоинт `/movies`).

## 🧰 Стек

* Python
* pytest
* requests

## 📁 Структура

* clients/ — API-клиенты
* custom_requester/ — базовый класс для запросов
* utils/ — генерация данных
* tests/ — тесты

## 🔐 Авторизация

Используется отдельный сервис:
https://auth.dev-cinescope.coconutqa.ru

Токен получается автоматически в фикстуре.

## 🚀 Запуск

```bash
pip install -r requirements.txt
pytest -v
```

## ✅ Покрытие

* GET /movies
* GET /movies/{id}
* POST /movies
* PATCH /movies/{id}
* DELETE /movies/{id}

## 🧪 Тесты

* позитивные
* негативные
* фильтрация

## 👨‍💻 Автор

Ivan
