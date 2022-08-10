@echo off
python.exe -m pip install --upgrade pip
pip install setuptools twine
python setup.py sdist

twine upload dist\*

del disspy.egg-info\*
rmdir disspy.egg-info

del dist\*
rmdir dist

del build\lib\disspy\*
rmdir build\lib\disspy
del build\lib\*
rmdir build\lib
del build\*
rmdir build

pause