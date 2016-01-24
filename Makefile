all: install quality test

install-test:
	pip install -q -r test_requirements.txt

install: install-test

quality:
	./bin/quality.sh

test:
	./bin/test.sh
