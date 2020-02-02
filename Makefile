docs:
	pdoc3 --html --force --output-dir docs pandas_profiling
	mv docs/pandas_profiling/* docs
	rmdir docs/pandas_profiling

test:
    pytest --black tests/unit/
    pytest --black tests/issues/
    pytest --nbval tests/notebooks/
    flake8 . --select=E9,F63,F7,F82 --show-source --statistics

install:
	pip install -e .

lint:
	black .