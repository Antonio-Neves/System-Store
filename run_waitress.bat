@echo off
REM Script que será executado pelo NSSM

REM Ativação e arranque (mantenha o caminho completo, pois o NSSM pode não saber onde está)
call "D:\devdj\system-store\.venv\Scripts\activate.bat"

REM Arranque do Waitress
waitress-serve --port=8000 system_store.wsgi:application

REM Não coloque 'pause' ou 'deactivate' no final, pois o serviço deve correr até ser parado.
