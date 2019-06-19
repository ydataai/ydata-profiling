@echo off

IF "%1%" == "docs" (
    pdoc3 --html  --force --output-dir docs pandas_profiling
    robocopy .\docs\pandas_profiling .\docs /E /MOVE
    ECHO "Docs updated!"
)


IF "%1%" NEQ "docs" (
    ECHO "No command matched"
)