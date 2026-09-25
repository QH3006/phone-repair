@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
set PYTHONUNBUFFERED=1
title PhoneCare AI - Cloud Demo Launcher

echo ========================================================
echo   PhoneCare AI - KHOI TAO CLOUD DEMO CONG KHAI
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python scripts\run_cloud_demo.py
    goto finish
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py scripts\run_cloud_demo.py
    goto finish
)

echo [LOI] Khong tim thay Python tren may tinh!
echo Vui long cai dat Python hoac them Python vao bien moi truong PATH.
pause

:finish
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [THONG BAO] Tien trinh da dung. Nhan phim bat ky de thoat...
    pause >nul
)