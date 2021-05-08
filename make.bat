@echo off
setlocal enabledelayedexpansion

IF "%1%" == "docs" (
    mkdir docs/
    :: pdoc3
    robocopy .\docsrc\assets\ .\docs\assets\
    pdoc3 --html  --force --output-dir docs pandas_profiling
    robocopy .\docs\pandas_profiling .\docs /E /MOVE
    :: sphinx
    cd docsrc/ && make github
    ECHO "Docs updated!"
    GOTO end
)

IF "%1" == "test" (
    pytest tests/unit/
    pytest tests/issues/
    pytest --nbval tests/notebooks/
    flake8 . --select=E9,F63,F7,F82 --show-source --statistics
    ECHO "Tests completed!"
    GOTO end
)

IF "%1" == "examples" (
    FOR /R /D %%d in ("examples\*") do (
        SET B=%%d
        FOR /R %%f in ("!B:%CD%\=!\*.py") DO (
            SET C=%%f
            ECHO "Running !C:%%d\=! (in %%d)"
            CD %%d && python "!C:%%d\=!"
            CD %CD%
        )
    )

    ECHO "Example runs completed!"
    GOTO end
)

IF "%1" == "pypi_package" (
    make install
    check-manifest
    python setup.py sdist bdist_wheel
    twine check dist/*
    twine upload --skip-existing dist/*
    ECHO "PyPi package completed"
    GOTO end
)

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
