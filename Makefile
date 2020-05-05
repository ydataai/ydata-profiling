docs:
	mkdir docs/
	# pdoc3
	cp -a ./docsrc/assets/ ./docs/assets/
	pdoc3 --html --force --output-dir docs pandas_profiling
	mv docs/pandas_profiling/* docs
	rmdir docs/pandas_profiling
	# sphinx
        cd docsrc/ && make github

test:
	pytest --black tests/unit/
	pytest --black tests/issues/
	pytest --nbval tests/notebooks/
	flake8 . --select=E9,F63,F7,F82 --show-source --statistics

pypi_package:
	make install
	check-manifest
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --skip-existing dist/*

install:
	pip install -e .[notebook,app]

lint:
	isort --apply
	black .

typing:
	pytest --mypy -m mypy .

all:
	make lint
	make install
	make examples
	make docs
	make test
	make typing
