@echo off
python tests\make_vfs.py
python src\main.py --vfs tests\generated_vfs\deep.zip --script scripts\stage4_script.txt