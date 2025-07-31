# Math Microservice

## Description

This project is a lightweight FastAPI-based microservice that performs mathematical operations through a REST API and a responsive Bootstrap-based frontend.

### Supported operations:
- `pow(base, exponent)` – exponentiation
- `fibonacci(n)` – nth Fibonacci number
- `factorial(n)` – factorial of n

The app includes:
- A dark-mode-enabled frontend
- SQLite-backed request logging
- Real-time filtering of request history
- Input/output validation using **Pydantic**

---

## Technologies Used

- **FastAPI** – web API framework
- **Pydantic** – validation and serialization
- **Jinja2** – HTML templates
- **SQLite** – persistent request storage
- **Bootstrap 5** – modern, responsive UI
- **flake8** – code style checker
- **HTML/CSS/JS** – with dark mode support
- **Python 3.11+**

---

## Features

- REST API: `/pow`, `/fibonacci`, `/factorial`
- Web UI with animated results and mobile responsiveness
- SQLite request storage (operation, input, result, timestamp)
- `/history` page:
  - View all / last 10 / filter by operation
  - Dynamic dropdown appears when needed
- Dark mode toggle (persistent across pages)
- Flake8 linted and readable code
- Google Fonts (`Inter`) and animated UI elements

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI service

```bash
uvicorn main:app --reload
```

### 3. Use the app

- Web UI: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- History UI: http://localhost:8000/history

---

## Example API Usage

### POST /pow

Request:
```json
{
  "base": 2,
  "exponent": 3
}
```
Response:
```json
{
  "result": 8.0
}
```

### GET /fibonacci?n=10

Response:
```json
{
  "result": 55
}
```

### GET /factorial?n=5

Response:
```json
{
  "result": 120
}
```

---

## Project Structure

```text
math_microservice/
├── main.py                         # FastAPI app entry point
├── api/
│   └── routes.py                   # API + /history route
├── models/
│   ├── request_models.py           # Pydantic input schemas
│   └── response_models.py          # Pydantic output schemas
├── services/
│   └── math_ops.py                 # Core calculation logic
├── storage/
│   ├── memory_store.py             # (Legacy) in-memory store
│   └── sqlite_store.py             # SQLite-based persistent store
├── templates/
│   ├── index.html                  # Web form UI
│   └── history.html                # Request history UI
├── requirements.txt                # Python dependencies
├── .flake8                         # Linter configuration
├── README.md                       # This file
```