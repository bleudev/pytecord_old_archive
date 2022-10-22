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

from typing import List


def dict_to_tuples(__dict: dict) -> List[tuple]:
    """dict_to_tuples
    Dict to lists of tuples in format (key, value)

    Args:
        __dict (dict): Original dict

    Returns:
        List[tuple]: List of tuples (key, value)
    """
    keys = list(__dict.keys())
    values = list(__dict.values())

    result = [(key, values[keys.index(key)]) for key in keys]

    return result

def _type_check(__v: object, __t: type) -> bool:
    check = isinstance(__v, __t)

    if not check:
        raise TypeError('Expected %s: Got %s' % (__t, type(__v)))

    return check
