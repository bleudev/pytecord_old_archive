@echo off
pip install setuptools twine
python setup.py sdist
twine upload dist\*
pause