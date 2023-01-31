@echo off
setlocal enabledelayedexpansion

IF "%1" == "lint" (
    pre-commit run --all-files
    GOTO end
)

IF "%1" == "install" (
	pip install -e .[notebook]
	GOTO end
)

IF "%1%" == "clean" (
	ECHO "Not implemented yet"
	GOTO end
)

IF "%1%" == "all" (
    make lint
    make install
    make examples
    make docs
    make test
    GOTO end
)

ECHO "No command matched"
:end
