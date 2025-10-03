@echo off
echo Testing VFS with 3+ levels...
copy vfs_complex.json vfs.json
"C:\Users\Mary\AppData\Local\Programs\Python\Python310\python.exe" Shell.py
pause