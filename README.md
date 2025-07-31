# Math Microservice

## Description

A lightweight FastAPI-based microservice for mathematical operations, featuring:
- REST API, responsive Bootstrap frontend, and CLI
- Smart background processing for heavy computations
- Persistent SQLite storage for requests and background tasks
- Dark mode, animated UI, and mobile responsiveness

### Supported Operations
- `pow(base, exponent)` – exponentiation
- `fibonacci(n)` – nth Fibonacci number
- `factorial(n)` – factorial of n

---

## Technologies Used

- **FastAPI** – web API framework
- **Pydantic** – validation and serialization
- **Jinja2** – HTML templates
- **SQLite** – persistent request storage
- **Bootstrap 5** – modern, responsive UI
- **flake8** – code style checker
- **Click** – CLI interface
- **pytest** – automated testing
- **Python 3.11+**

---

## Features

- REST API: `/pow`, `/fibonacci`, `/factorial`
- Web UI with dark mode and animations
- SQLite request storage (operation, input, result, timestamp)
- `/history` page: view all, last 10, or filter by operation
- `/status/{task_id}` endpoint to track async computations
- `/tasks` dashboard to view all background jobs and their status/results
- CLI interface for running operations and exporting history
- Flake8 linted and readable code

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

- Web UI: [http://localhost:8000](http://localhost:8000)
- API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
- History UI: [http://localhost:8000/history](http://localhost:8000/history)
- Tasks Dashboard: [http://localhost:8000/tasks](http://localhost:8000/tasks)

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

## Running with Docker

You can run this app in a container using Docker or Rancher Desktop.

### 1. Build the Docker image

```bash
docker build -t math-microservice .
```

### 2. Run the container

```bash
docker run -d -p 8000:8000 --name math-api math-microservice
```

- The app will be available at [http://localhost:8000](http://localhost:8000)
- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. (Optional) Clean up

To stop and remove the container:

```bash
docker stop math-api
docker rm math-api
```

### 4. Development tips

- The `.dockerignore` file is set up to keep your images small and clean.
- For persistent SQLite storage or development with live code reload, consider using Docker volumes or `docker-compose`.

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

## Notes

- Built as part of a technical assignment. Background tasks were implemented using FastAPI’s `BackgroundTasks` with SQLite persistence for tracking. Large number safety (Python 3.11 digit limits) is handled gracefully.
- The CLI allows you to run operations and export history directly from the terminal.

---

## Project Structure

```text
.
├── main.py                         # FastAPI app entry point
├── cli.py                          # Command-line interface
├── requirements.txt                # Python dependencies
├── .flake8                         # Linter configuration
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── test.sh                         # Shell script to run all tests
├── api/
│   ├── __init__.py
│   └── routes.py                   # API + /history route
├── models/
│   ├── __init__.py
│   ├── request_models.py           # Pydantic input schemas
│   └── response_models.py          # Pydantic output schemas
├── services/
│   ├── __init__.py
│   ├── math_ops.py                 # Core calculation logic
│   └── background_tasks.py         # Background task logic
├── storage/
│   ├── __init__.py
│   ├── memory_store.py             # (Legacy) in-memory store
│   ├── sqlite_store.py             # SQLite-based persistent store
│   └── task_store.py               # Background task tracking (SQLite)
├── templates/
│   ├── index.html                  # Web form UI
│   ├── history.html                # Request history UI
│   └── tasks.html                  # Background tasks dashboard
├── tests/
│   ├── test_math_ops.py            # Unit tests for math functions
│   ├── test_cli.py                 # CLI command tests
│   └── test_api.py                 # API
```