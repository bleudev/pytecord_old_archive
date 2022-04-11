from setuptools import setup
import dist.dispy

setup(
      name="Dispy",
      version="0.1a",
      download_url=dist.dispy.__stablever__,
      author='itttgg',
      python_requires='>=3.6.0',
      license="MIT"
)
