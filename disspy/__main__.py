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

from sys import argv
from . import __version__
import colorama

try:
    _op = argv[1]

    if _op in ['-help', '-H']:
        print(f"""
            {colorama.Fore.YELLOW}-help, -H ->{colorama.Fore.RESET} Command with information about other commands
            -version, -V -> Version of package
            """)

    elif _op in ['-version', '-V']:
        print(f"{colorama.Fore.YELLOW}Dispy version -> {colorama.Fore.RESET}{__version__}")
    
    else:
        print(f"""
              {colorama.Fore.RED}                Error!{colorama.Fore.YELLOW} Invalid param!
        {colorama.Fore.RESET}If you don't know params type `python -m disspy -H` or `python -m disspy -help`
                                                                                Error code: 1101
              """)
except IndexError:
    print(f"""
        {colorama.Fore.RED}                Error!{colorama.Fore.YELLOW} Please type any param!
        {colorama.Fore.RESET}If you don't know params type `python -m disspy -H` or `python -m disspy -help` 
                                                                                Error code: 1100
          """)
