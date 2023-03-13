@echo off
py -3 -m pip install --upgrade pip
pip install setuptools twine
py -3 setup.py sdist

twine upload dist\*

rd /s /q pytecord.egg-info
rd /s /q dist
rd /s /q build

pause