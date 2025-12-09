# 🌿 Nourish by Kerry

### A Smart Recipe, Meal Planning & Nutrition Web App

Nourish by Kerry is a modern, user-friendly recipe and meal-planning web application built with Python, Django, and Bootstrap. It helps users discover recipes, build personal collections, plan meals, track ingredients, and auto-generate grocery lists.

Designed for clarity and speed, Nourish focuses on a clean responsive UI and practical features that make home cooking easier.

---

## ✨ Core Features

- Smart Recipe Search: search by ingredients, name, or category; filter by time, difficulty, diet, or cost.
- Personal Recipe Manager: add, edit, and delete recipes; upload images; add ingredients and step-by-step instructions.
- Diet Filters: vegetarian, vegan, high-protein, keto, low-cost options.
- Meal Planner: assign recipes to days and create weekly plans.
- Auto-Generated Grocery Lists: combine ingredient quantities from selected recipes and download or view on mobile.
- Responsive UI (Bootstrap): fast and mobile-friendly.

---

## 🛠️ Tech Stack

- Backend: Python 3 + Django
- Frontend: HTML, CSS, Bootstrap
- Templates: Django templates
- Database: SQLite for development (PostgreSQL recommended for production)

---

## 🚀 Quick Install (Linux / Ubuntu)

1. Clone the repo:

```bash
git clone https://github.com/KerryNK/Nourish-Recipe-App.git
cd nourish-by-kerry
```

2. Create & activate a virtualenv:

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations and start the dev server:

```bash
python manage.py migrate
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

## 📦 Future Roadmap

- User accounts & profiles (done)
- Enhanced meal planner & nutrition breakdown
- Shopping list export (CSV/print)
- Premium features and AI recipe suggestions

---

## 👩‍💻 Author

Kerry Koech — student & developer passionate about food tech and digital wellness.

---

## 📄 License

MIT License

---
