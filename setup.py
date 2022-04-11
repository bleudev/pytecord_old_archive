from setuptools import setup, find_packages

setup(
    name="dispy",
    version="0.1.0",
    description="Dispy - package for creating bots for Discord",
    license="MIT",
    author="itttgg",
    packages=[find_packages(where="dispy", include=["https"])]
)
