@echo off
echo Testing VFS with 3+ levels...
del /f /q "vfs.json" 2>nul
copy vfs_complex.json vfs.json
"C:\Users\Mary\AppData\Local\Programs\Python\Python310\python.exe" Shell.py
del /f /q "vfs.json" 2>nul
pause