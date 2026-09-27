@echo off
python tests\make_vfs.py
echo --- Minimal VFS ---
python src\main.py --vfs tests\generated_vfs\minimal.zip --script scripts\demo_script.txt
echo --- Multi-file VFS ---
python src\main.py --vfs tests\generated_vfs\multi_file.zip --script scripts\demo_script.txt
echo --- Deep VFS (3+ levels) ---
python src\main.py --vfs tests\generated_vfs\deep.zip --script scripts\demo_script.txt