from disspy.enums import ComponentType, TextInputStyle
from typing import Iterable, Callable

class TextInput:
    def _check_len(self, value: str | int, min: int, max: int):
        if isinstance(value, str):
            return len(value) <= max and min <= len(value)
        elif isinstance(value, int):
            return value <= max and min <= value
    def _check_for(self, value: Iterable, min: int, max: int):
        for i in value:
            b = self._check_len(i, min, max)
            if not b:
                return False
        return True
    def _check_return(self, value: str | Iterable, l: tuple[int, int], func: Callable[[str | Iterable, int, int], bool]):
        if value is None:
            return value
        
        b: bool = func(value, l[0], l[1])
        
        if b:
            return value
        else:
            raise ValueError('This string %s is too long or fewer! Maximun is %d, minimun is %d' % (
                value,
                l[0],
                l[1]
            ))

    def __init__(self,
                 custom_id: str,
                 label: str,
                 style: TextInputStyle = TextInputStyle.short,
                 length: tuple[int, int] = (None, None), # (min, max)
                 required: bool = False,
                 value: str = None,
                 placeholder: str = None) -> None:
        self.custom_id = custom_id
        self.label = self._check_return(label, (1, 45), self._check_len)
        self.style = style if style in list(range(1, 3)) else TextInputStyle.short
        self.length = self._check_return(length, (1, 4000), self._check_for)
        self.required = required
        self.value = self._check_return(value, (1, 4000), self._check_len)
        self.placeholder = self._check_return(placeholder, (1, 100), self._check_len)

    def eval(self) -> dict:
        return {
            'type': ComponentType.text_input,
            'custom_id': self.custom_id,
            'style': self.style,
            'label': self.label,
            'min_length': self.length[0],
            'max_length': self.length[1],
            'required': self.required,
            'value': self.value,
            'placeholder': self.placeholder
        }


class Modal:
    title: str
    custom_id: str
    inputs: list[TextInput]

    def __init_subclass__(cls, *, custom_id: str, title: str) -> None:
        cls.custom_id = custom_id
        cls.title = title

    def eval(self) -> dict:
        rows_json = []
        for i in self.inputs:
            rows_json.append({
                'type': ComponentType.action_row,
                'components': [i.eval()]
            })

        return dict(
            custom_id=self.custom_id,
            title=self.title,
            components=rows_json
        )

    async def submit(self, ctx, **inputs):
        '''
        Modal submit event
        '''
        raise NotImplementedError('You must implement this method!')
