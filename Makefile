.PHONY: lint lint-ci

lint:
	flake8 app/

lint-ci:
	flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app/ --count --exit-zero --max-complexity=15 --max-line-length=150 --statistics
