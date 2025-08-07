# Math Microservice

## Description

A lightweight FastAPI-based microservice for mathematical operations, featuring:
- REST API, responsive Bootstrap frontend, and CLI
- Smart background processing for heavy computations
- Persistent SQLite storage for requests and background tasks
- Dark mode, animated UI, and mobile responsiveness
- Session-based browser login and API key authentication

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
- **Docker** – containerization
- **Makefile** – developer automation
- **itsdangerous** – secure session cookies
- **dotenv** – environment variable management

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
- Docker and Docker Compose support for easy deployment
- Session-based login for browser users
- API key authentication for CLI, curl, and external clients
- Protected `/docs`, `/history`, `/tasks` routes (redirects to `/login` if not authenticated)

---

## How to Run

### 1. Install dependencies

You can install dependencies using either `pip` or the build system:

```bash
pip install -e .
```
or
```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI service

```bash
uvicorn main:app --reload
```

### 3. Use the app

- Web UI: [http://localhost:8000](http://localhost:8000)
- API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs) (requires login)
- History UI: [http://localhost:8000/history](http://localhost:8000/history) (requires login)
- Tasks Dashboard: [http://localhost:8000/tasks](http://localhost:8000/tasks) (requires login)
- Login: [http://localhost:8000/login](http://localhost:8000/login)

### 4. Run from the command line (CLI)

The CLI is implemented in the `cli/` package and registered as `mathcli` via `setup.py`.  
You can run it with:

```bash
python -m cli.main pow --base 2 --exp 10
python -m cli.main fibonacci --n 1000
python -m cli.main factorial --n 2000
python -m cli.main export --operation all
python -m cli.main status --task-id <task_id>
```

Or, if installed as a package:

```bash
mathcli pow --base 2 --exp 10
```

---

## Authentication

- **Browser:** Login at `/login` (session cookie required for protected pages)  
  For testing purposes, use the following credentials:  
  - **Username:** `admin`  
  - **Password:** `admin`

- **API/CLI/curl:** Use `X-API-Key` header (see `.env` for value, default: `secret123`)

**Example curl:**

```bash
curl -X POST "http://localhost:8000/pow" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: secret123" \
     -d '{"base": 2, "exponent": 3}'
```

---

## Makefile

A `Makefile` is provided for common developer tasks:

```makefile
run:        # Start FastAPI with reload
cli:        # Run the CLI
test:       # Run all tests
lint:       # Run flake8 linter
docker:     # Build Docker image
compose:    # Run docker-compose up --build
clean:      # Remove .pyc and __pycache__ files
```

Example usage:

```bash
make run
make cli
make test
make lint
make docker
make compose
make clean
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
- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs) (requires login)

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

## Running with Docker Compose

For persistent storage and easier management, use Docker Compose:

### 1. Start the app with Docker Compose

```bash
docker-compose up --build
```

- This will build the image and start the service.
- The `storage/` directory is mounted as a volume, so your SQLite database files persist across restarts.

### 2. Stop the app

```bash
docker-compose down
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

## Notes

- Built as part of a technical assignment. Background tasks were implemented using FastAPI’s `BackgroundTasks` with SQLite persistence for tracking. Large number safety (Python 3.11 digit limits) is handled gracefully.
- The CLI allows you to run operations and export history directly from the terminal.
- All sensitive endpoints are protected by session or API key authentication.

---

## Project Structure

```text
.
├── main.py                         # FastAPI app entry point
├── cli/
│   ├── __init__.py
│   ├── main.py                     # CLI entry point
│   └── commands/                   # CLI commands (pow_cmd.py, fibonacci_cmd.py, etc.)
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # PEP 517/518 build config
├── setup.py                        # setuptools config and CLI entry point
├── Makefile                        # Developer automation
├── Dockerfile                      # Docker build instructions
├── docker-compose.yml              # Docker Compose config
├── .dockerignore                   # Docker ignore rules
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
│   ├── background_tasks.py         # Background task logic
│   └── auth.py                     # Session and API key authentication
├── storage/
│   ├── __init__.py
│   ├── memory_store.py             # (Legacy) in-memory store
│   ├── sqlite_store.py             # SQLite-based persistent store
│   └── task_store.py               # Background task tracking (SQLite)
├── templates/
│   ├── index.html                  # Web form UI
│   ├── history.html                # Request history UI
│   ├── tasks.html                  # Background tasks dashboard
│   └── login.html                  # Login page
├── tests/
│   ├── test_math_ops.py            # Unit tests for math functions
│   ├── test_cli.py                 # CLI command tests
│   └── test_api.py                 # API endpoint
```
