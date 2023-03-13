from setuptools import setup
from pytecord import __version__

with open('README.md', 'r', encoding='utf-8') as mdf:
    long_description = mdf.read()

with open('requirements.txt', 'r', encoding='utf-8') as rqf:
    install_requires = rqf.readlines()

setup(
    name='pytecord',
    version=__version__,
    author='pixeldeee',
    author_email='aitiiigg1@gmail.com',
    description='Pytecord - library for creating bots in discord written in Python',
    download_url=f'https://github.com/pixeldeee/pytecord/releases/tag/{__version__}',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pixeldeee/pytecord',
    packages=['pytecord'],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=install_requires
)
