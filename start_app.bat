@echo off
echo Starting AI Text Detector Application...
echo.

echo Starting FastAPI Backend Server...
start "FastAPI Server" cmd /k "python fastapi_server.py"

timeout /t 3 /nobreak >nul

echo Starting React Native Frontend...
start "React Native App" cmd /k "npm run web"

echo.
echo Both servers are starting...
echo FastAPI Server: http://localhost:8000
echo React Native App: http://localhost:8081 (or check terminal for actual port)
echo.
echo Press any key to close this window...
pause >nul
