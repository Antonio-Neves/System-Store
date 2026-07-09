@echo off
REM Script to be use for NSSM

REM Need complete path
call "D:\devdj\store_managementChanged \.venv\Scripts\activate.bat"

REM Waitress start
waitress-serve --port=8000 store_management.wsgi:application
