run:
	uvicorn main:app --reload

cli:
	python -m cli.main

test:
	PYTHONPATH=. pytest

lint:
	flake8 .

docker:
	docker build -t math-microservice .

compose:
	docker-compose up --build

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
