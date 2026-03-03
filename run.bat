@echo off
echo.
echo ════════════════════════════════════════════
echo   📊 时序数据分析工作站 - 快速启动
echo ════════════════════════════════════════════
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Python
    echo 请先安装 Python 3.8+，并将其添加到系统 PATH
    echo.
    pause
    exit /b 1
)

echo ✓ Python 已检测
echo.

REM 检查是否需要安装依赖
if not exist "venv" (
    echo 📦 正在创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ⬇️  正在安装依赖包（第一次运行，可能需要 2-3 分钟）...
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✓ 依赖安装完成
) else (
    call venv\Scripts\activate.bat
)

echo.
echo 🚀 正在启动应用...
echo.
echo 📌 应用启动后，请在浏览器打开：
echo    http://localhost:8501
echo.
echo 💡 提示：按 Ctrl+C 可停止应用
echo.
echo ════════════════════════════════════════════
echo.

streamlit run app.py

pause
