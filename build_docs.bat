@echo off
REM Check if the Sphinx documentation directory exists
IF EXIST "C:\thinkalike-project\docs\sphinx" (
    echo Directory exists. Changing directory to documentation.
    REM Change directory to the Sphinx docs folder (using /d to handle drive change)
    cd /d "C:\thinkalike-project\docs\sphinx"
    REM Now run Sphinx build to generate HTML documentation
    make html
) ELSE (
    echo Error: Directory "C:\thinkalike-project\docs\sphinx" does not exist.
    exit /b 1
)
pause