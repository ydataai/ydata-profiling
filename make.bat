@echo off
setlocal enabledelayedexpansion

IF "%1%" == "docs" (
    pdoc3 --html  --force --output-dir docs pandas_profiling
    robocopy .\docs\pandas_profiling .\docs /E /MOVE
    ECHO "Docs updated!"
    GOTO end
)

IF "%1" == "test" (
    pytest --nbval --cov=./ --sanitize-with tests/sanitize-notebook.cfg
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
    python setup.py sdist
    twine upload dist/*
    ECHO "PyPi package completed"
    GOTO end
)

IF "%1" == "lint" (
    black .
    GOTO end
)

IF "%1%" == "all" (
    make lint
    make examples
    make docs
    make test
    GOTO end
)

ECHO "No command matched"
:end