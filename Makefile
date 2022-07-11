.PHONY: test

test:
	pytest -vx --cov=timelimiter --cov-config=.coveragerc --cov-report=term-missing --no-cov-on-fail tests


build:
	python -m build


publish_test:
	python -m twine upload --repository testpypi dist/* --verbose


publish:
	python -m twine upload dist/* --verbose
