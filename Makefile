.PHONY: docs examples

docs:
	rm -rf docs/
	mkdir docs/
	# sphinx
	cd docsrc/ && make github

test:
	pytest tests/unit/
	pytest tests/issues/
	pytest --nbval tests/notebooks/
	pandas_profiling -h

test_cov:
	pytest --cov=. tests/unit/
	pytest --cov=. --cov-append tests/issues/
	pytest --cov=. --cov-append --nbval tests/notebooks/
	pandas_profiling -h

examples:
	find ./examples -maxdepth 2 -type f -name "*.py" -execdir python {} \;

package:
	rm -rf build dist
	echo "$(version)" > VERSION
	python setup.py sdist bdist_wheel
	twine check dist/*

install:
	pip install -e .[notebook]

lint:
	pre-commit run --all-files

clean:
	git rm --cached `git ls-files -i --exclude-from=.gitignore`

all:
	make lint
	make install
	make examples
	make docs
	make test
