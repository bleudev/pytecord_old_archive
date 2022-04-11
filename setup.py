from setuptools import setup
import dist.dispy

url = dist.dispy.__stablever__

author = url
author = author.replace("//", "/")

author_list = author.split("/")
author = author_list[2]
print(author)

# setup(
#       name="Dispy",
#       version="0.1a",
#       download_url=dist.dispy.__stablever__,
#       author=
# )
