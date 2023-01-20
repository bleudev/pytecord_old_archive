from disspy_v2.enums import ComponentType, TextInputStyle
from typing import Iterable
class TextInput:
    def _check_len(self, value: str, min: int, max: int):
        return len(value) <= max and min <= len(value)
    def _check_for(self, value: Iterable, min: int, max: int):
        for i in value:
            b = self._check_len(i, min, max)
            if b == False: return False
        return True
        

    def __init__(self,
                 label: str, # max - 45
                 style: TextInputStyle = TextInputStyle.short,
                 length: tuple[int, int] = (None, None), # (min, max)
                 required: bool = False,
                 value: str[4000] = None,
                 placeholder: str[100] = None) -> None:
        self.label = self._check_len()
        self.style = style
        self.length = self._check_for(length, 1, 4000)
        self.required = required
        self.value = value
        self.placeholder = placeholder
    
    def eval(self) -> dict:
        return {
            'type': ComponentType.text_input,
            'custom_id': 'dev_input',
            'style': self.style,
            'label': self.label,
            'min_length': self.length[0],
            'max_length': self.length[1],
            'required': self.required,
            'value': self.value,
            'placeholder': self.placeholder
        }
