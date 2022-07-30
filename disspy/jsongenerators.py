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


class _EmbedGenerator:
    def __new__(cls, obj):
        fields_jsons = []

        for f in obj.fields:
            fields_jsons.append(_FieldGenerator(f))

        return {
            "title": obj.title,
            "description": obj.description,
            "footer": obj.footer,
            "color": obj.color,
            "fields": fields_jsons,
            "author": obj.author
        }


class _FieldGenerator:
    def __new__(cls, obj):
        return {
            "name": obj.name,
            "value": obj.value,
            "inline": obj.inline
        }


class _OptionGenerator:
    def __new__(cls, obj):
        if obj.option_type == 3 or obj.option_type == 4 or obj.option_type == 10 and obj.choices:
            return {
                "name": obj.name,
                "description": obj.description,
                "type": obj.option_type,
                "choices": obj.choices,
                "required": obj.required
            }
        else:
            return {
                "name": obj.name,
                "description": obj.description,
                "type": obj.option_type,
                "required": obj.required
            }
