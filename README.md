# Task Manager

A full-featured task management web application built with **Python** and **Django 5**.

Built as a hands-on learning project to understand the Django framework end-to-end — models, views, forms, the ORM, URL routing, the admin interface, and automated testing.

---

## Features

- **Full CRUD** — create, view, edit, and delete tasks
- **Toggle status** — mark tasks as done or pending with one click
- **Priority levels** — High, Medium, Low with colour-coded badges
- **Categories** — assign tasks to custom colour-coded categories
- **Due dates** — set deadlines and see them at a glance in the task list
- **Filtering** — filter the task list by status, priority, or category
- **Dashboard** — home page shows live counts of total, pending, and done tasks
- **Flash messages** — user feedback after every create, update, or delete action
- **Django Admin** — full admin interface with search, filters, and batch actions (mark done / mark pending)
- **Automated tests** — 25+ tests covering models, views, CRUD flows, filtering, and edge cases

---

## Tech Stack

| Layer      | Technology                   |
|------------|------------------------------|
| Backend    | Python 3, Django 5.2         |
| Database   | SQLite (development)         |
| Templates  | Django Template Language     |
| Styling    | Plain CSS (no external framework) |

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. (Optional) Create an admin user
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

The Django admin interface is available at `http://127.0.0.1:8000/admin/`.

---

## Running Tests

```bash
python manage.py test tasks
```

---

## Project Structure

```
task-manager/
├── core/                  # Django project settings and root URL config
├── tasks/                 # Main app
│   ├── migrations/        # Database migrations
│   ├── templates/tasks/   # HTML templates
│   ├── models.py          # Task and Category models
│   ├── views.py           # View functions
│   ├── forms.py           # ModelForm with validation
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   └── tests.py           # Automated tests
├── manage.py
└── requirements.txt
```

---

## Data Model

```
Category
  name        CharField
  color       CharField (hex, e.g. #ff5733)

Task
  title       CharField
  description TextField (optional)
  priority    CharField  low | medium | high
  due_date    DateField  (optional)
  done        BooleanField
  category    ForeignKey → Category (nullable)
  created_at  DateTimeField (auto)
  updated_at  DateTimeField (auto)
```

---

## Screenshots

> _Coming soon_

---

## Author

Vyshnav K B
