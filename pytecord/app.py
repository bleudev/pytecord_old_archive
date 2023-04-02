from asyncio import get_event_loop
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

from pytecord import utils
from pytecord.enums import InteractionCallbackType, InteractionType, ApplicationCommandType
from pytecord.route import Route
from pytecord.ui import Modal
from pytecord.profiles import Member, User
from pytecord.channel import Channel, Message

if TYPE_CHECKING:
    from pytecord.annotations import Strable, Subclass, Snowflake
    from pytecord.payloads import (
        InteractionPayload,
        InteractionDataPayload,
        ApplicationCommandPayload,
        InteractionDataOptionPayload,
        ApplicationCommandOptionPayload,
        ApplicationCommandOptionChoicePayload
    )
    from pytecord.hook import Hook
    from aiohttp import ClientSession

__all__ = (
    'Context',
    'Modal',
)

class Choice:
    def __init__(self, data: 'ApplicationCommandOptionChoicePayload'):
        _ = data.get

        self.name: str = _('name')
        self.name_localizations: dict[str, str] | None = _('name_localizations')
        self.value: str | int | float = _('value')

class Option:
    def __init__(self, data: 'InteractionDataOptionPayload | ApplicationCommandOptionPayload') -> None:
        _ = data.get

        self.type: int = _('type')
        self.name: str = _('name')
        self.name_localizations: dict[str, str] | None = _('name_localizations')
        self.description: str = _('description')
        self.description_localizations: dict[str, str] | None = _('description_localizations')
        self.required: bool | None = _('required')
        self.choices: list[Choice] | None = [Choice(i) for i in _('choices', [])]
        self.options: list[Option] | None = [Option(i) for i in _('options', [])]
        self.channel_types: list[int] | None = _('channel_types')
        self.min_value: int | float | None = _('min_value')
        self.max_value: int | float | None = _('max_value')
        self.min_length: int | None = _('min_length')
        self.max_length: int | None = _('max_length')
        self.autocomplete: bool | None = _('autocomplete')
        self.value: str | int | float | bool | None = _('value')

class Command:
    def __init__(self, data: 'InteractionDataPayload | ApplicationCommandPayload') -> None:
        self._data = data

        _ = data.get

        self.id: Snowflake = int( _('id') )
        self.type: int | None = _('type')
        self.application_id: Snowflake | None = int( _('application_id') )
        self.guild_id: Snowflake | None = int( _('guild_id') )
        self.name: str = _('name')
        self.name_localizations: dict[str, str] | None = _('name_localizations')
        self.description: str | None = _('description')
        self.description_localizations: dict[str, str] | None = _('description_localizations')
        self.default_member_permissions: str | None = _('default_member_permissions')
        self.dm_permission: bool | None = _('dm_permission')
        self.default_permission: bool | None = _('default_permission')
        self.nsfw: bool | None = _('nsfw')
        self.version: int | None = _('version')
        self.resolved: dict[str, dict[str, Any]] | None = _('resolved')
        self.target_id: Snowflake | None = int( _('target_id') )

        self.options: list[Option] | None = [Option(i) for i in _('options', [])]

    def __getitem__(self, key: str):
        return self._data.get(key, None)

    def eval(self) -> dict:
        return self._data

class ContextMenu:
    def __init__(self, data: 'InteractionDataPayload | ApplicationCommandPayload') -> None:
        self._data = data
        
        _ = data.get

        self.id: Snowflake = int( _('id') )
        self.type: int | None = _('type')
        self.application_id: Snowflake | None = int( _('application_id') )
        self.guild_id: Snowflake | None = int( _('guild_id') )
        self.name: str = _('name')
        self.name_localizations: dict[str, str] | None = _('name_localizations')
        self.default_member_permissions: str | None = _('default_member_permissions')
        self.dm_permission: bool | None = _('dm_permission')
        self.default_permission: bool | None = _('default_permission')
        self.nsfw: bool | None = _('nsfw')
        self.version: int | None = _('version')
        self.resolved: dict[str, dict[str, Any]] | None = _('resolved')
        self.target_id: Snowflake | None = int( _('target_id') )

    def __getitem__(self, key: str):
        return self._data.get(key, None)

    def eval(self) -> dict:
        return self._data

if TYPE_CHECKING:
    CT = TypeVar('CT', Command, ContextMenu)
    MT = TypeVar('MT', bound=Modal)

class AppClient:
    def __init__(self) -> None:
        self.commands = []
        self.callbacks = {1: {}, 2: {}, 3: {}}
        self.component_callbacks = {'modals': {}}

    def add_command(self, command: 'CT', callback: Callable[..., Coroutine[Any, Any, Any]]) -> 'CT':
        self.commands.append(command)
        self.callbacks[command['type']].setdefault(command['name'], callback)
        return command

    def add_modal(self, modal: 'MT') -> 'MT':
        self.component_callbacks['modals'].setdefault(modal.custom_id, modal.submit)
        return modal

    async def invoke_command(self, name: str, type: int, *args, **kwrgs):
        await self.callbacks[type][name](*args, **kwrgs)

    async def invoke_modal_submit(self, custom_id: str, *args, **kwargs):
        await self.component_callbacks['modals'][custom_id](*args, **kwargs)

class Context:
    def __init__(
        self, data: 'InteractionPayload', token: str, session: 'ClientSession', hook: 'Hook'
    ) -> None:
        self._bot_token = token
        self._session = session
        self._hook = hook

        _ = data.get

        self.id: Snowflake = int( _('id') )
        self.application_id: Snowflake = int( _('application_id') )
        self.type: int = _('type')
        self.guild_id: Snowflake | None = int( _('guild_id') )
        self.channel_id: Snowflake | None = int( _('channel_id') )
        self.member: Member | None = Member(session, **_('member', {}))
        self.user: User | None = User(session, **_('user', {}))
        self.token: str = _('token')
        self.version: int = _('version')
        self.message: Message | None = Message(session, **_('message', {}))
        self.app_permissions: str | None = _('app_permissions')
        self.locale: str | None = _('locale')
        self.guild_locale: str | None = _('guild_locale')

        self.data: dict[str, Any] = _('data')

        _types = {
            ApplicationCommandType.chat_input: Command,
            ApplicationCommandType.message: ContextMenu,
            ApplicationCommandType.user: ContextMenu
        }
        self.command: Command | ContextMenu = _types[self.data.get('type', 1)](self.data)

    async def __respond_to_an_interaction(self, payload: dict):
        route = Route(
            '/interactions/%s/%s/callback', self.id, self.token,
            method='POST',
            token=self._bot_token,
            payload=payload
        )
        j, _ = await route.async_request(self._session, get_event_loop())
        return j

    async def send_message(
            self,
            *strings: list['Strable'],
            sep: str = ' ',
            tts: bool = False,
            ephemeral: bool = False
        ):
        await self.__respond_to_an_interaction({
            'type': InteractionCallbackType.channel_message_with_source,
            'data': utils.message_payload(
                *strings,
                sep=sep,
                ephemeral=ephemeral,
                tts=tts
            )
        })

    async def edit_message(
            self,
            *strings: list['Strable'],
            sep: str = ' ',
            tts: bool = False,
            ephemeral: bool = False
        ):
        await self.__respond_to_an_interaction({
            'type': InteractionCallbackType.update_message,
            'data': utils.message_payload(
                *strings,
                sep=sep,
                ephemeral=ephemeral,
                tts=tts
            )
        })

    async def send_modal(self, modal: 'Subclass[Modal]'):
        if self.interaction.type in [
            InteractionType.ping,
            InteractionType.modal_submit
        ]:
            return # not available in discord API
        await self.__respond_to_an_interaction({
            'type': InteractionCallbackType.modal,
            'data': modal.eval()
        })
        self._hook._app_client.add_modal(modal)
