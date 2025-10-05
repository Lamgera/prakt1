@echo off
echo Testing VFS with several files...
del /f /q "vfs.json" 2>nul
copy vfs_simple.json vfs.json
"C:\Users\Mary\AppData\Local\Programs\Python\Python310\python.exe" Shell.py
del /f /q "vfs.json" 2>nul
pause