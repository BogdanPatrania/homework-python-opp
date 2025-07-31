# Math Microservice

## Description

This project is a lightweight FastAPI-based microservice that performs mathematical operations through a REST API, a responsive Bootstrap-based frontend, and a command-line interface (CLI).

### Supported operations:
- `pow(base, exponent)` – exponentiation
- `fibonacci(n)` – nth Fibonacci number
- `factorial(n)` – factorial of n

The app includes:
- A dark-mode-enabled frontend
- SQLite-backed request logging
- Real-time filtering of request history
- Input/output validation using **Pydantic**
- Smart background processing for heavy inputs (fibonacci, factorial, pow)
- `/status/{task_id}` endpoint to track async computations
- `/tasks` dashboard to view all background jobs
- CLI interface using `click` (run operations or export history via terminal)

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
- **Click** – CLI interface
- **Separate SQLite database for tracking background task metadata and results**

---

## Features

- REST API: `/pow`, `/fibonacci`, `/factorial`
- Web UI with animated results and mobile responsiveness
- SQLite request storage (operation, input, result, timestamp)
- `/history` page:
  - View all / last 10 / filter by operation
  - Dynamic dropdown appears when needed
- `/status/{task_id}` endpoint to track async computations
- `/tasks` dashboard to view all background jobs and their status/results
- Smart background processing for heavy computations (offloads large jobs to background tasks)
- CLI interface for running operations and exporting history
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
- Tasks Dashboard: http://localhost:8000/tasks

### 4. Run from the command line

```bash
python cli.py pow --base 2 --exp 10
python cli.py fibonacci --n 1000
python cli.py factorial --n 2000
python cli.py export --operation all
```

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
│   ├── sqlite_store.py             # SQLite-based persistent store
│   └── task_store.py               # Background task tracking (SQLite)
├── templates/
│   ├── index.html                  # Web form UI
│   ├── history.html                # Request history UI
│   └── tasks.html                  # Background tasks dashboard
├── cli.py                          # Command-line interface
├── requirements.txt                # Python dependencies
├── .flake8                         # Linter configuration
├── README.md                       # This file
```

---

## Notes

- Built as part of a technical assignment. Background tasks were implemented using FastAPI’s `BackgroundTasks` with SQLite persistence for tracking. Large number safety (Python 3.11 digit limits) is handled gracefully.
- The CLI allows you to run operations and export history directly from the terminal.


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
- Tasks Dashboard: http://localhost:8000/tasks

### 4. Run from the command line

```bash
python cli.py pow --base 2 --exp 10
python cli.py fibonacci --n 1000
python cli.py factorial --n 2000
python cli.py export --operation all
```

---

## Running Tests

Automated tests are provided for the core math logic, CLI, and API endpoints.

### Run all tests

```bash
./test.sh
```
or
```bash
PYTHONPATH=. pytest
```

### Test coverage

- `tests/test_math_ops.py`: Unit tests for math functions
- `tests/test_cli.py`: CLI command tests
- `tests/test_api.py`: API endpoint tests using FastAPI's TestClient

---

## Example API Usage