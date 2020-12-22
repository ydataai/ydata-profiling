.PHONY: docs examples

docs:
	rm -rf docs/
	mkdir docs/
	# pdoc3
	cp -a ./docsrc/assets/ ./docs/assets/
	pdoc3 --html --force --output-dir docs pandas_profiling
	mv docs/pandas_profiling/* docs
	rmdir docs/pandas_profiling
	# sphinx
	cd docsrc/ && make github

test:
	pytest -m "not sparktest" --black tests/unit/
	pytest -m "not sparktest" --black tests/issues/
	pytest -m "not sparktest" --nbval tests/notebooks/
	flake8 . --select=E9,F63,F7,F82 --show-source --statistics

test_cov:
	pytest -m "not sparktest" --cov=. tests/unit/
	pytest -m "not sparktest" --cov=. --cov-append tests/issues/
	pytest -m "not sparktest" --cov=. --cov-append --nbval tests/notebooks/
	pandas_profiling -h
	make typing

test-spark:
	pytest -m sparktest --black tests/unit/

examples:
	find ./examples -maxdepth 2 -type f -name "*.py" -execdir python {} \;

pypi_package:
	make install
	check-manifest
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --skip-existing dist/*

install:
	pip install -e .[notebook,app]

install-spark-ci:
	sudo apt-get -y install openjdk-8-jdk
	curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
	--output ${TRAVIS_BUILD_DIR}/spark.tgz
	tar -xvzf ${TRAVIS_BUILD_DIR}/spark.tgz && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

lint:
	isort --profile black .
	black .

typing:
	pytest --mypy -m mypy .

clean:
	git rm --cached `git ls-files -i --exclude-from=.gitignore`

all:
	make lint
	make install
	make examples
	make docs
	make test
	make typing
