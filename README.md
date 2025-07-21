# Car Service CRM

**RESTful API для управління записами на обслуговування автомобілів для СТО**

---

## Можливості

- CRUD для клієнтів, автомобілів, послуг, механіків, документів та записів на обслуговування
- Ролі: **admin**, **mechanic**, **customer**
- Авторизація через JWT (Bearer Token)
- Розділення прав доступу за ролями
- Завантаження документів та локальне зберігання файлів
- Призначення механіків на записи
- Автоматична email-підтвердження після створення запису (асинхронно)
- Генерація інтерактивної документації Swagger/OpenAPI

---

## Структура бази даних

- **users**: user_id, name, email, password, role
- **cars**: car_id, user_id, brand, model, year, plate_number, vin
- **services**: service_id, name, description, price, duration
- **mechanics**: mechanic_id, name, birth_date, login, password, role, position
- **documents**: document_id, mechanic_id, type, file_path
- **appointments**: appointment_id, user_id, car_id, service_id, mechanic_id, appointment_date, status

---

## Швидкий старт

1. **Клонувати репозиторій**

   git clone <https://github.com/shulika-w/car_service_crm_test.git>
   cd car_service_crm

2. **Встановити залежності**

   poetry install

3. **Налаштувати .env** 

MYSQL_HOST=...
MYSQL_PORT=...
MYSQL_DB=...
MYSQL_USER=...
MYSQL_PASSWORD=...

SECRET_KEY=...

SMTP_HOST=...
SMTP_PORT=...
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_FROM=...

5. **(Опційно) Запуск MySQL через Docker**

    docker compose up -d

5. **Запуск застосунку**

    poetry run uvicorn src.car_service_crm.main:app --reload

6. **Документація**

    Swagger UI: http://localhost:8000/docs

---

## Ролі користувачів

	•	admin — адміністратор (перший користувач створюється як admin автоматично)
	•	customer — клієнт (реєструється самостійно)
	•	mechanic — механік (створюється тільки адміном)

---

## Основні ендпоінти

	•	/users/register — реєстрація клієнта (email, name, password)
	•	/users/login — авторизація (отримання JWT)
	•	/users/me — перегляд власного профілю
	•	/cars — управління автомобілями клієнта
	•	/services — CRUD для послуг (адмін)
	•	/mechanics — CRUD для механіків (адмін)
	•	/documents — завантаження/перегляд документів механіка
	•	/appointments — записи на обслуговування, призначення механіка

---

## Email-нотифікації

	•	Для надсилання листів використовується SMTP. Приклад налаштування див. у .env.
	•	Відправка підтвердження після створення запису відбувається асинхронно.

---

## Вимоги

	•	Python 3.11+
	•	Poetry (для управління залежностями)
	•	SQLite (за замовчуванням, підтримка MySQL через PyMySQL)

---

## Додатково

	•	Всі ендпоінти повертають JSON.
	•	Документація генерується автоматично через Swagger/OpenAPI.
	•	Продумана обробка помилок з відповідними HTTP-кодами.

---

## Тестування

PYTHONPATH=src poetry run pytest


Тести перевіряють:
	•	Головний роут
	•	Реєстрацію та логін користувача
	•	Отримання JWT та доступ до /users/me
    
---

## Автор

Shulika Volodymyr