## DevOpsExam – Билет 17

**Тема:** приложение записи на прием к врачу.

### Запуск приложения локально

- **Установка зависимостей**

```bash
pip install -r requirements.txt
```

- **Запуск сервера**

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`. Документация Swagger: `http://127.0.0.1:8000/docs`.

### Схема БД

В БД создаются 2 таблицы:

- **doctors**: `id`, `full_name`, `reception_time`, `specialization`
- **appointments**: `id`, `phone_number`, `sms_code`, `doctor_id`, `appointment_time`

Данные из билета сидируются автоматически при старте приложения.

### Эндпоинты

- **POST** `/auth/login` – аутентификация пациента по номеру телефона и коду из СМС.  
  Тело запроса:

```json
{
  "phone_number": "+78986664502",
  "sms_code": "5500"
}
```

В ответе возвращается `access_token`, который используется в заголовке `Authorization: Bearer <token>`.

- **GET** `/doctors/schedule` – получение информации о расписании приема врачей **вместе с их специализацией**.
- **GET** `/appointments` – получение информации о записях пациента, **требует аутентификации** (заголовок `Authorization: Bearer <token>`).

### Docker

- **Сборка образа**

```bash
docker build -t devops-exam-ticket-17 .
```

- **Запуск контейнера**

```bash
docker run -p 8000:8000 devops-exam-ticket-17
```

### Подсказки для отчета и TeamCity

- Репозиторий должен быть публичным, название и имена конфигураций/шагов сборки – с вашей фамилией и инициалами.
- Для `main`-ветки в TeamCity:
  - сборка Docker-образа,
  - пуш в DockerHub,
  - деплой образа на prod-стенд.
- Для веток `feature/*` и `fix/*`:
  - только сборка Docker-образа.
- В пайплайн стоит добавить:
  - запуск `flake8`/`ruff` как линтера,
  - SAST-анализатор (например, `bandit`),
  - автотесты (юнит-тесты FastAPI/SQLAlchemy).

