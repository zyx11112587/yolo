@echo off
echo === 启动 YOLO 自动开火脚本 ===

:: 可选：激活 Anaconda（如果你使用了 conda 虚拟环境，可取消注释下面两行）
:: call C:\ProgramData\anaconda3\Scripts\activate.bat base

:: 切换到脚本目录
cd /d Your\yolo

:: 运行你的 Python 脚本
python.exe run.py

pause
