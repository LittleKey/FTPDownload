@echo off
cd /d "%~dp0"
src/FTPDownload.py ".*" -n -i ftpinfo.json -p lib
pause