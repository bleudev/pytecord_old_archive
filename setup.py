from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as mdf:
    long_description = mdf.read()

requires = ["aiohttp>=3.6.0,<4", "requests", "typing", "websocket-client", "asyncio"]


setup(
    name="disspy",
    version='0.1a2',
    author="itttgg",
    author_email="aitiiigg1@gmail.com",
    description="Dispy - package for creating bots",
    download_url="https://github.com/itttgg/dispy/tree/0.1a2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itttgg/dispy",
    packages=['disspy'],
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=requires
)
