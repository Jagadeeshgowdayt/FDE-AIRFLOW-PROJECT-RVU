@echo off
REM Airflow Startup Script for Windows PowerShell/CMD
REM This script starts Airflow in WSL without requiring PowerShell execution policy changes

setlocal

echo ==========================================
echo    Apache Airflow Startup Helper (WSL)
echo ==========================================
echo.

if "%1"=="" goto help
if /I "%1"=="webserver" goto webserver
if /I "%1"=="web" goto webserver
if /I "%1"=="scheduler" goto scheduler
if /I "%1"=="sched" goto scheduler
if /I "%1"=="standalone" goto standalone
if /I "%1"=="all" goto standalone
goto help

:webserver
echo Starting Airflow Webserver in WSL...
echo.
echo Access the UI at: http://localhost:8080
echo Username: admin
echo Password: admin
echo.
echo Press Ctrl+C to stop
echo.
wsl bash -c "cd ~/airflow_project && ./start_airflow.sh webserver"
goto end

:scheduler
echo Starting Airflow Scheduler in WSL...
echo.
echo Press Ctrl+C to stop
echo.
wsl bash -c "cd ~/airflow_project && ./start_airflow.sh scheduler"
goto end

:standalone
echo Starting Airflow in Standalone mode (Webserver + Scheduler)...
echo.
echo Access the UI at: http://localhost:8080
echo Username: admin
echo Password: admin
echo.
echo Press Ctrl+C to stop
echo.
wsl bash -c "cd ~/airflow_project && ./start_airflow.sh standalone"
goto end

:help
echo ==========================================
echo              USAGE INSTRUCTIONS
echo ==========================================
echo.
echo Option 1: Start Webserver and Scheduler Separately (RECOMMENDED)
echo ----------------------------------------------------------------
echo.
echo   Terminal 1 - Start Webserver:
echo     start-airflow.bat webserver
echo.
echo   Terminal 2 - Start Scheduler:
echo     start-airflow.bat scheduler
echo.
echo ==========================================
echo.
echo Option 2: Start Everything Together (TESTING ONLY)
echo ---------------------------------------------------
echo.
echo   One Terminal - Start Both:
echo     start-airflow.bat standalone
echo.
echo ==========================================
echo.
echo Available Commands:
echo   start-airflow.bat webserver    - Start webserver only
echo   start-airflow.bat web          - Alias for webserver
echo   start-airflow.bat scheduler    - Start scheduler only
echo   start-airflow.bat sched        - Alias for scheduler
echo   start-airflow.bat standalone   - Start both (testing)
echo   start-airflow.bat all          - Alias for standalone
echo.
echo ==========================================
echo.
echo After Starting Airflow:
echo   Open browser: http://localhost:8080
echo   Username: admin
echo   Password: admin
echo.
echo ==========================================
goto end

:end
endlocal
