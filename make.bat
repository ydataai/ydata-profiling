@echo off
setlocal enabledelayedexpansion

IF "%1%" == "docs" (
    mkdir docs/
    :: sphinx
    cd docsrc/ && make github
    ECHO "Docs updated!"
    GOTO end
)

IF "%1" == "test" (
    pytest tests/unit/
    pytest tests/issues/
    pytest --nbval tests/notebooks/
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
