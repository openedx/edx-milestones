all: install quality test

install-test:
	pip install -q -r test_requirements.txt

install: install-test
	pip install -q -r requirements.txt

quality:
	tox -e quality

test: ## run tests on every supported Python version
	tox
