.PHONY: test

test:
	pytest -vx --cov=timelimiter --cov-config=.coveragerc --cov-report=term-missing --no-cov-on-fail tests
