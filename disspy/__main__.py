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
import colorama
from . import __version__

colorama.init()

__cli_version__ = "1.0"

_helpcommand = f"""
            {colorama.Fore.GREEN}Commands:
                {colorama.Fore.YELLOW}-help, -H ->{colorama.Fore.RESET} Command with information about other commands
                {colorama.Fore.YELLOW}-version, -V ->{colorama.Fore.RESET} Version of package
            {colorama.Fore.GREEN}Params for commands (example, python -m disspy -help -no-color):
                {colorama.Fore.YELLOW}-[command] ->{colorama.Fore.RESET} (for -help) Get info about command (example, python -m disspy -help -version)
                {colorama.Fore.YELLOW}-no-color, -NC ->{colorama.Fore.RESET} Print info without colorama
                """

_helpcommand_no_color = """
            Commands:
                -help, -H -> Command with information about other commands
                -version, -V -> Version of package
            Params for commands (example, python -m disspy -help -no-color):
                -[command] -> (for -help) Get info about command (example, python -m disspy -help -version)
                -no-color, -NC -> Print info without colorama
                """

try:
    _op = argv[1]

    if _op in ['-help', '-H']:
        try:
            _param = argv[2]

            if _param in ['-version', '-V', '-help', '-H']:
                try:
                    _secparam = argv[3]

                    if _secparam in ['-no-color', '-NC']:
                        # -[command]
                        if _param in ['-version', '-V']:
                            print("""
                        -version, -V
                            Show disspy version
                                """)
                        elif _param in ['-help', '-H']:
                            print("""
                        -help, -H
                            Information about commands and params
                                """)
                except IndexError:
                    # -[command]
                    if _param in ['-version', '-V']:
                        print(f"""
                    {colorama.Fore.GREEN}-version, -V
                        {colorama.Fore.RESET}Show disspy version
                            """)
                    elif _param in ['-help', '-H']:
                        print(f"""
                    {colorama.Fore.GREEN}-help, -H
                        {colorama.Fore.RESET}Information about commands and params
                            """)
            # -no-color
            elif _param in ['-no-color', '-NC']:
                print(_helpcommand_no_color)
            else:
                print(_helpcommand)
        except IndexError:
            print(_helpcommand)

    elif _op in ['-version', '-V']:
        try:
            _param = argv[2]
            if _param in ['-no-color', '-NC']:
                print(f"""
                Dispy version -> {__version__}
                CLI version   -> {__cli_version__}
                """)

        except IndexError:
            print(f"""
                {colorama.Fore.YELLOW}Dispy version -> {colorama.Fore.RESET}{__version__}
                {colorama.Fore.YELLOW}CLI version   -> {colorama.Fore.RESET}{__cli_version__}
                """)

    else:
        print(f"""
                              {colorama.Back.RED}Error!{colorama.Back.RESET}{colorama.Fore.YELLOW} Invalid command!
        {colorama.Fore.RESET}If you don't know commands type `python -m disspy -H` or `python -m disspy -help`
                                                                                Error code: 1101
              """)

except IndexError:
    print(f"""
                        {colorama.Back.RED}Error!{colorama.Back.RESET}{colorama.Fore.YELLOW} Please type any command!
        {colorama.Fore.RESET}If you don't know commands type `python -m disspy -H` or `python -m disspy -help` 
                                                                                Error code: 1100
          """)
