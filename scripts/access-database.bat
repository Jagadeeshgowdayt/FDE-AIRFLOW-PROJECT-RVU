@echo off
REM Database Access Tool

:menu
cls
echo ==========================================
echo   Movie Analytics - Database Access
echo ==========================================
echo.
echo 1. Copy database to Windows (for DB Browser)
echo 2. Export to CSV files (for Excel/Power BI)
echo 3. Show database statistics
echo 4. View top Hollywood movies
echo 5. View top Indian movies
echo 6. Open database location in Explorer
echo 7. Create backup
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto copy_db
if "%choice%"=="2" goto export_csv
if "%choice%"=="3" goto stats
if "%choice%"=="4" goto view_hollywood
if "%choice%"=="5" goto view_indian
if "%choice%"=="6" goto open_explorer
if "%choice%"=="7" goto backup
if "%choice%"=="8" goto end
goto menu

:copy_db
echo.
echo Copying database to Windows...
wsl bash -c "cp /tmp/movies.db '/mnt/c/Users/jagad/Downloads/New folder (8)/movies.db'"
echo.
echo ✓ Database copied to: movies.db
echo.
echo Download DB Browser for SQLite:
echo https://sqlitebrowser.org/dl/
echo.
echo Then open: movies.db
echo.
pause
goto menu

:export_csv
echo.
echo Exporting to CSV files...
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && python3 '/mnt/c/Users/jagad/Downloads/New folder (8)/export_to_csv.py'"
echo.
pause
goto menu

:stats
echo.
wsl bash -c "cd ~/airflow_project && source activate_airflow.sh && python3 '/mnt/c/Users/jagad/Downloads/New folder (8)/show_db_stats.py'"
echo.
pause
goto menu

:view_hollywood
echo.
echo Top 10 Hollywood Movies by ROI:
echo.
wsl bash -c "sqlite3 /tmp/movies.db -header -column 'SELECT title, ROUND(roi,0) as \"ROI%%\", ROUND(revenue/1000000.0,1)||\"M\" as Revenue FROM movie_roi_analytics ORDER BY roi DESC LIMIT 10;'"
echo.
pause
goto menu

:view_indian
echo.
echo Top 15 Indian Movies by ROI:
echo.
wsl bash -c "sqlite3 /tmp/movies.db -header -column 'SELECT title, language, ROUND(roi,0) as \"ROI%%\", release_date FROM indian_movies_roi ORDER BY roi DESC LIMIT 15;'"
echo.
pause
goto menu

:open_explorer
echo.
echo Opening current folder...
start .
goto menu

:backup
echo.
echo Creating backup...
wsl bash -c "cp /tmp/movies.db '/mnt/c/Users/jagad/Downloads/New folder (8)/movies_backup.db'"
echo.
echo ✓ Backup created: movies_backup.db
echo.
pause
goto menu

:end
echo.
echo Goodbye!
timeout /t 2 /nobreak >nul
