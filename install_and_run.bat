@echo off
REM ==============================
REM AI Traffic Demo - Safe Menu Version
REM ==============================
set LOGFILE=traffic_demo.log

:MENU
cls
echo ==============================
echo      AI Traffic Demo
echo ==============================
echo 1. Install dependencies
echo 2. Download YOLOv8 model
echo 3. Run sample video
echo 4. Run camera demo
echo 5. Exit
echo ==============================
set /p choice=Select option (1-5): 

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto DOWNLOAD
if "%choice%"=="3" goto RUN_VIDEO
if "%choice%"=="4" goto RUN_CAMERA
if "%choice%"=="5" exit
echo Invalid choice, press any key to return...
pause
goto MENU

:INSTALL
echo === Installing dependencies ===
pip install -r requirements.txt >> %LOGFILE% 2>&1
if %errorlevel% neq 0 (
    echo Error during installation! Check %LOGFILE%
) else (
    echo Dependencies installed successfully >> %LOGFILE%
)
pause
goto MENU

:DOWNLOAD
echo === Downloading YOLOv8 model ===
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')" >> %LOGFILE% 2>&1
if %errorlevel% neq 0 (
    echo Error during model download! Check %LOGFILE%
) else (
    echo YOLOv8 model downloaded successfully >> %LOGFILE%
)
pause
goto MENU

:RUN_VIDEO
echo === Running sample video ===
python demo_live.py --video sample_video.mp4 >> %LOGFILE% 2>&1
if %errorlevel% neq 0 (
    echo Error during demo run! Check %LOGFILE%
) else (
    echo Sample video demo finished >> %LOGFILE%
)
pause
goto MENU

:RUN_CAMERA
echo === Running camera demo ===
python demo_live.py --camera 0 >> %LOGFILE% 2>&1
if %errorlevel% neq 0 (
    echo Error during camera demo! Check %LOGFILE%
) else (
    echo Camera demo finished >> %LOGFILE%
)
pause
goto MENU
