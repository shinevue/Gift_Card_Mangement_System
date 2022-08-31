build:
	black . --check --verbose --diff --color
	isort . --check --diff
	mypy
	flake8 .
	bandit -r gcmanager --verbose
	docker-compose -f mongo-for-testing.yml up -d
	coverage erase
	coverage run -mp unittest discover tests/unit --verbose
	coverage run -mp unittest discover tests/integration --verbose
	docker-compose -f mongo-for-testing.yml down
	coverage combine
	coverage report
