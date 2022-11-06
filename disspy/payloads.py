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

from disspy.jsongenerators import _EmbedGenerator

# Utils
def _get_embeds(embeds: list) -> list:
    embeds_json = []
    for i in embeds:
        embeds_json.append(_EmbedGenerator(i))
    return embeds_json

def message_payload(content=None, embeds=None, action_row=None) -> dict:
    """message_payload
    Get message payload

    Args:
        content (str): Message content
        embeds (List[Embed]): Message embeds
        action_row (ActionRow): Message action row

    Returns:
        dict: Message payload
    """
    _payload = {"content": None, "embeds": None, "components": None}

    # Utils
    def _del_field(key: str):
        del _payload[key]

    if embeds:
        _payload["embeds"] = _get_embeds(embeds)
    else:
        _del_field("embeds")

    if content:
        _payload["content"] = content
    else:
        _del_field("content")

    if action_row:
        if action_row.json["components"]:
            _payload["components"] = action_row.json
        else:
            _del_field("components")
    else:
        _del_field("components")

    return _payload
