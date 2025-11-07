@echo off
REM TMDB Pipeline Helper - Check DAG Status and Data

setlocal

echo ==========================================
echo   TMDB Movie ROI Pipeline - Helper
echo ==========================================
echo.

if "%1"=="" goto menu
if /I "%1"=="status" goto status
if /I "%1"=="list" goto list
if /I "%1"=="trigger" goto trigger
if /I "%1"=="unpause" goto unpause
if /I "%1"=="data" goto data
if /I "%1"=="indian" goto indian
if /I "%1"=="dashboard" goto dashboard
if /I "%1"=="logs" goto logs
goto menu

:menu
echo Available Commands:
echo.
echo   check-pipeline.bat status    - Check if DAG is visible
echo   check-pipeline.bat list      - List all DAGs
echo   check-pipeline.bat unpause   - Unpause the TMDB pipeline
echo   check-pipeline.bat trigger   - Trigger the pipeline to run
echo   check-pipeline.bat data      - View the data in database
echo   check-pipeline.bat indian    - View Indian movies data
echo   check-pipeline.bat dashboard - Generate and open visual dashboard
echo   check-pipeline.bat logs      - View recent logs
echo.
goto end

:status
echo Checking TMDB pipeline status...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && airflow dags list | grep tmdb"
echo.
echo If you see 'tmdb_movie_roi_pipeline' above, your DAG is loaded!
goto end

:list
echo Listing all DAGs...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && airflow dags list"
goto end

:unpause
echo Un-pausing TMDB pipeline...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && airflow dags unpause tmdb_movie_roi_pipeline"
echo.
echo Pipeline un-paused! Now trigger it from the UI or run: check-pipeline.bat trigger
goto end

:trigger
echo Triggering TMDB pipeline...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && airflow dags trigger tmdb_movie_roi_pipeline"
echo.
echo Pipeline triggered! Check the UI at http://localhost:8080
goto end

:data
echo Checking database for movie data...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && python3 '/mnt/c/Users/jagad/Downloads/New folder (8)/check_db.py'"
goto end

:indian
echo Checking Indian movies database...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && python3 '/mnt/c/Users/jagad/Downloads/New folder (8)/check_indian_movies.py'"
goto end

:dashboard
echo Generating interactive dashboard...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && airflow tasks test movie_dashboard_generator generate_dashboard 2024-01-01 2>&1 | grep -E '(Generating|generated|Location|movies:)'"
echo.
echo Copying to Windows...
wsl bash -c "cp /tmp/movie_dashboard.html '/mnt/c/Users/jagad/Downloads/New folder (8)/movie_dashboard.html'"
echo.
echo Opening dashboard in browser...
start "" "c:\Users\jagad\Downloads\New folder (8)\movie_dashboard.html"
echo.
echo Dashboard opened! Check your browser.
goto end

:logs
echo Viewing recent scheduler logs...
echo.
wsl bash -c "tail -20 ~/airflow_project/logs/scheduler/latest/*.log 2>/dev/null || echo 'No logs found'"
goto end

:end
endlocal
