@echo off
title TechWatch AI - Local Worker
echo ==========================================
echo   Starting TechWatch AI Python Worker
echo ==========================================
echo.

start "Ollama server" ollama serve
timeout /t 3 /nobreak > NUL


"D:\Developpement\techwatchAI\code\backend-python\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause