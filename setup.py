"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as mdf:
    long_description = mdf.read()

requires = ['aiohttp>=3.6.0,<4', 'requests', 'asyncio', 'colorama']


__version__ = "0.5.3.3"


setup(
    name="disspy",
    version=__version__,
    author="itttgg",
    author_email="aitiiigg1@gmail.com",
    description="Dispy - package for creating bots",
    download_url=f"https://github.com/itttgg/dispy/tree/{__version__}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itttgg/dispy",
    packages=['disspy'],
    classifiers = [
        "Programming Language :: Python :: 3"
    ],
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=requires
)
