@echo off
cd /d %~dp0
python -m pip install -r requirements.txt
pytest tests\ --html=report.html
