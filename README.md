# TouchCraft AI 🚀

**TouchCraft AI** — це SaaS-платформа для автоматизованої генерації та розгортання вебдодатків за допомогою технологій штучного інтелекту. Система використовує моделі Google Gemini для створення багатомовних сайтів, автоматичної генерації контенту, SEO-структури та візуальних активів із подальшим контейнеризованим розгортанням.

---

# 🏗️ Архітектура проєкту

Платформа побудована за клієнт-серверною архітектурою та складається з двох основних підсистем:

## FrontendBuilder

Клієнтська SPA-підсистема, реалізована на базі:

- Vue 3
- Vite
- Tailwind CSS
- Auth0
- Axios
- Lucide Vue

FrontendBuilder відповідає за:

- візуальне редагування сайтів;
- динамічний рендеринг SDUI-конфігурацій;
- управління проєктами;
- SEO та бізнес-налаштування;
- інтеграцію аналітики та CRM.

---

## AIBuilderEngine

Серверне ядро, реалізоване на базі FastAPI.

Основні функції:

- AI-генерація структури сайтів через Google Gemini;
- Pydantic-валідація JSON-контрактів;
- генерація медіа-активів;
- збірка Vue/Vite-проєктів;
- контейнеризація та автоматичний деплой;
- інтеграція з S3-сховищем;
- управління доменами та SSL.

---

## Інфраструктура

Інфраструктура платформи побудована на:

- Docker Compose
- Nginx Proxy Manager
- PostgreSQL / SQLite
- MinIO (S3-compatible storage)

---

# ✨ Основні можливості

- 🤖 AI-генерація сайтів через Google Gemini
- 🌍 Багатомовна локалізація (i18n)
- 🎨 Генерація логотипів, фавіконів та hero-зображень
- 🐳 Автоматичне Docker-розгортання
- 🔒 Автоматичний SSL через Let's Encrypt
- 🌐 Прив'язка власних доменів
- 📊 Інтеграція Google Analytics 4
- 🧾 Вбудована CRM-система для лідів
- 💳 Інтеграція Stripe для білінгу
- 📧 SMTP-сповіщення про нові заявки
- ⚡ Live Preview та візуальний редактор

---

# 🛠️ Використані технології

## Backend (FastAPI / Python)

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- google-genai
- Boto3
- Stripe
- PyJWT
- aiosmtplib

---

## Frontend (Vue.js)

- Vue 3 (Composition API)
- Vite
- Tailwind CSS
- Vue Router
- Axios

---

## Інфраструктура

- Docker
- Docker Compose
- Nginx Proxy Manager
- MinIO
- Let's Encrypt

---

# 🚀 Встановлення та запуск

## Попередні вимоги

Перед запуском необхідно встановити:

- Docker
- Docker Compose
- Google Gemini API Key

---

# ⚙️ Налаштування середовища

Створіть `.env` файл у корені проєкту:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-pro

S3_ACCESS_KEY=minio_user
S3_SECRET_KEY=minio_password
S3_BUCKET=websites

NPM_EMAIL=admin@example.com
NPM_PASSWORD=secure_password
````

---

# 🐳 Запуск платформи

```bash
docker-compose up -d --build
```

---

# 🌐 Доступ до сервісів

| Сервіс              | Опис                         |
| ------------------- | ---------------------------- |
| FrontendBuilder     | Основний інтерфейс платформи |
| AIBuilderEngine     | Backend API                  |
| MinIO Console       | S3-консоль управління        |
| Nginx Proxy Manager | Reverse Proxy та SSL         |

---

# 🛠️ Локальна розробка

## Backend

```bash
cd AIBuilderEngine

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend

```bash
cd FrontendBuilder

npm install

npm run dev
```

---

# 🧠 Архітектурні особливості

## Server-Driven UI (SDUI)

TouchCraft AI використовує декларативний підхід до генерації інтерфейсів. Замість прямої генерації HTML/CSS, система створює структурований JSON-опис, який інтерпретується клієнтським рендерером.

---

## Захист від AI-"галюцинацій"

Усі відповіді LLM проходять сувору валідацію через Pydantic-схеми перед збереженням або рендерингом.

---

## Контейнеризація

Кожен згенерований сайт запускається в окремому Docker-контейнері з повною ізоляцією інфраструктури.

---

## Dynamic Reverse Proxy

Маршрутизація сайтів реалізована через Nginx Proxy Manager без використання динамічного Port Binding.

---

# 📄 Ліцензія

Проєкт є власністю **TouchCraft AI**.

Усі права захищені.
