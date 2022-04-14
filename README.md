<p> <img src="logo.png" width="250" alt="logo"/></p>

# Dispy

![alt text](https://img.shields.io/badge/version-0.1a2-informational?style=flat) ![alt text](https://img.shields.io/badge/lang-python-informational) ![alt text](https://img.shields.io/badge/minimal_python_version-3.8-informational)

## Download stable version
```commandline
pip install disspy
```

## Links
https://pypi.org/project/disspy - Project site on PyPi
https://dispydocs.herokuapp.com - Site with docs for package

## Using

### Creating and running bot

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", prefix="!")

bot.run()
```

### bot.on("ready")

```python
import disspy

bot = disspy.DisBot(token="YOUR_TOKEN", prefix="!")


@bot.on("ready")
async def on_ready():
    print("Ready!")


bot.run()
```

# License
```
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
```
