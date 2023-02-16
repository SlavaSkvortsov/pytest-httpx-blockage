requirements:
	pip install -r requirements-dev.txt

test:
	python -m pytest

mypy:
	mypy .

flake8:
	flake8 .

isort:
	isort .

safety:
	safety check --bare -r requirements.txt -r requirements-dev.txt

check: isort flake8 mypy safety test
