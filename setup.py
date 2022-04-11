from setuptools import setup, find_packages
import dist.dispy

setup(
      name="dispy",
      version="0.1d",
      author='itttgg',
      author_email="aitiiigg1@gmail.com"
      python_requires='>=3.6.0',
      license="MIT",
      classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License"
      ],
      package_dir={"": "dispy"},
      packages=find_packages(where="ontology_processing")
)
