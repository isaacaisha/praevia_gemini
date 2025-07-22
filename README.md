# 🚀 Praevia Gemini API

A scalable Django REST API backend for managing audits, dossiers, contentieux, users, dashboards, and documents. Built with Django, Django REST Framework, and PostgreSQL.

---

## 📁 Project Structure

```
praevia_gemini/
├── praevia_api/            # Main Django app
│   ├── views.py            # Core API views
│   ├── auth_views.py       # Authentication views
│   ├── urls.py             # API routes
│   └── ...
├── praevia_core/           # Django core settings
│   ├── urls.py             # Main URL dispatcher
│   └── settings.py         # Settings (dev/prod)
├── static/                 # Static files (e.g. favicon)
├── media/                  # Uploaded media files
├── manage.py
└── Docker & Environment Files
    ├── Dockerfile
    ├── docker-compose.dev.yml
    └── .env
```

---

## 🧩 API Endpoints

### 🔐 Authentication

* `POST /praevia/gemini/api/login/` – Login
* `POST /praevia/gemini/api/logout/` – Logout

### 🗂️ Core Resources

* `GET /praevia/gemini/api/users/`
* `POST /praevia/gemini/api/dossiers/`
* `POST /praevia/gemini/api/contentieux/`
* `POST /praevia/gemini/api/audits/`
* `POST /praevia/gemini/api/documents/`

### 📊 Dashboards

* `/dashboard/juridique/`
* `/dashboard/rh/`
* `/dashboard/qse/`
* `/dashboard/direction/`

### 📌 File Handling

* `POST /documents/upload/` – Upload document
* `GET /documents/<id>/download/` – Download document

---

## 🌐 Favicon

A favicon is served at:

```
/favicon.ico → /static/favicon.ico
```

Make sure your icon is in `static/favicon.ico`.

---

## ⚙️ Environment Setup

### 1. Clone the project

```bash
git clone https://github.com/isaacaisha/praevia_gemini.git
cd praevia_gemini
```

### 2. Setup virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file or export manually:

```bash
export DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/praevi_aistudio_db
```

### 4. Create the database manually (if needed)

```bash
sudo -u postgres createdb praevi_aistudio_db
```

### 5. Migrate & run

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8079
```

---

## 🐳 Docker (optional)

To build and run with Docker:

```bash
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev up -d --build --remove-orphans
```

---

## 📌 License

MIT License

---

## 🧑‍💻 Maintainer

* **Name:** Lesane Byby
* **Email:** [medusadbt@gmail.com](mailto:medusadbt@gmail.com)
* **Project:** \[·SìįSí·Dbt· / Praevia Gemini]
