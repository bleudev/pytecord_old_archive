from typing import (TYPE_CHECKING, Callable, Generic, Iterable, TypeAlias,
                    TypeVar)

from pytecord.enums import ComponentType, TextInputStyle

if TYPE_CHECKING:
    from pytecord.app import Context

T = TypeVar('T', bound=str)

TextInputStyleKO: TypeAlias = int

__all__ = (
    'TextInput',
    'Modal',
)

class TextInput(Generic[T]):
    def _check_len(self, value: str | int, min: int, max: int) -> bool: # pylint: disable=redefined-builtin
        if isinstance(value, str):
            return len(value) <= max and min <= len(value)
        elif isinstance(value, int):
            return value <= max and min <= value
    def _check_for(self, value: Iterable, min: int, max: int) -> bool: # pylint: disable=redefined-builtin
        for i in value:
            b = self._check_len(i, min, max)
            if not b:
                return False
        return True
    def _check_return(
        self, value: str | int | Iterable, l: tuple[int, int],
        func: Callable[[str | int | Iterable, int, int], bool]):
        min, max = l # pylint: disable=redefined-builtin

        if value is None:
            return value

        if func(value, min, max):
            return value
        else:
            raise ValueError(
                f'This literal {value} is too long or fewer! Maximun is {max}, minimun is {min}'
            )

    def __init__(self,
                 custom_id: str,
                 label: str,
                 style: TextInputStyleKO = TextInputStyle.short,
                 length: tuple[int, int] = (0, 4000), # (min, max)
                 required: bool = False,
                 value: T | None = None,
                 placeholder: str | None = None) -> None:
        self.custom_id = custom_id
        self.label = self._check_return(label, (1, 45), self._check_len)
        self.style = style if style in list(range(1, 3)) else TextInputStyle.short
        self.length = self._check_return(length, (0, 4000), self._check_for)
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
    '''
    Object for sending guis in discord
    
    ```
    class MyModal(Modal, custom_id='mymodal', title='My modal title'):
        inputs = [
            TextInput(
                custom_id='hello',
                label='Hello',
                style=TextInputStyle.short,
                length=(1,10),
                required=True,
                value='Hello', # Default value
                placeholder='Please type any text...'
            )
        ]
    ```
    '''
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

        return {
            'custom_id': self.custom_id,
            'title': self.title,
            'components': rows_json
        }

    async def submit(self, ctx: 'Context', **inputs: dict[str, str]):
        '''
        Modal submit event.
        This event is executing when user click to 'Submit' button.

        ```
        # In your modal object
        async def submit(self, ctx: Context, **inputs):
            hello = inputs['hello'] # 'hello' is a custom id
            await ctx.send_message('Your value:', hello)
        # the code below is equivalent to the code above
        async def submit(self, ctx: Context, hello: str):
            await ctx.send_message('Your value': hello)
        ```
        '''
        raise NotImplementedError('You must implement this method!')
