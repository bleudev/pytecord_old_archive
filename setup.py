from setuptools import setup
import disspy

with open("README.md", "r", encoding="utf-8") as mdf:
    long_description = mdf.read()

requires = ["aiohttp>=3.6.0,<4", "requests", "typing", "asyncio", "colorama"]


setup(
    name="disspy",
    version=disspy.__version__,
    author="itttgg",
    author_email="aitiiigg1@gmail.com",
    description="Dispy - package for creating bots",
    download_url=f"https://github.com/itttgg/dispy/tree/{disspy.__version__}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itttgg/dispy",
    packages=['disspy'],
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=requires
)
