# Math Microservice

## Description

This project is a lightweight Python-based microservice that performs common mathematical operations via a RESTful API and a responsive frontend:

- `pow(base, exponent)` – computes base raised to the exponent
- `fibonacci(n)` – computes the nth Fibonacci number
- `factorial(n)` – computes the factorial of n

The service includes both an API and a Bootstrap-powered web UI. All incoming requests and computed results are stored in memory (dictionary-based), and inputs/outputs are validated with **Pydantic**.

---

## Technologies Used

- **FastAPI** – web microframework
- **Pydantic** – input/output validation
- **Jinja2** – for HTML templates
- **Bootstrap 5** – modern, responsive UI styling
- **flake8** – for clean, PEP8-compliant code
- **HTML/CSS/JS** – with gradient theming and dark mode
- **Python 3.11+**

---

## Features

- REST API endpoints (`/pow`, `/fibonacci`, `/factorial`)
- Simple in-memory database (Python list/dict)
- Responsive **web frontend** with form input
- Toggleable **Dark Mode** with gradient backgrounds
- Clean, animated result display
- Input validation with Pydantic
- Code linted with flake8
- Modern UI using Google Fonts (`Inter`)

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
### 2. Start the Service

```bash
uvicorn main:app --reload
```

### 3. Open the Web UI

Visit: http://localhost:8000
Or try the interactive API docs at: http://localhost:8000/docs

## Example API Calls

### POST /pow
```json
{
    "base": 2,
    "exponent": 5
}
```
### Response /pow
```json
{
    "result": 32.0
}
```

### GET /fibonacci?n=10
```json
{
    "result": 55
}
```

### GET /factorial?n=5
```json
{
    "result": 120
}
```

## Project Structure

```text
math_microservice/
├── main.py                         # Entry point – FastAPI app with routing
├── api/
│   └── routes.py                   # API endpoints for pow, fibonacci, factorial
├── models/
│   ├── request_models.py           # Pydantic input models
│   └── response_models.py          # Pydantic response models
├── services/
│   └── math_ops.py                 # Core math logic
├── storage/
│   └── memory_store.py             # In-memory request/result storage
├── templates/
│   └── index.html                  # Jinja2 template for web UI
├── requirements.txt                # Project dependencies
├── .flake8                         # Flake8 config for linting
├── README.md                       # Project documentation