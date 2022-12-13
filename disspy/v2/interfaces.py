from abc import ABC, abstractmethod

NI_label = 'This method is not implemented'

class IEvalable(ABC):
    '''
    IEvalable
    '''
    @abstractmethod
    def eval(self) -> dict:
        raise NotImplementedError(NI_label)

class IReplyable(ABC):
    '''
    IReplyable
    '''
    @abstractmethod
    async def reply(self, content=None, **kwargs):
        raise NotImplementedError(NI_label)

class IMessageable(ABC):
    '''
    IMessageable
    '''
    @abstractmethod
    async def send(self, content=None, **kwargs):
        raise NotImplementedError(NI_label)

class IApp(ABC):
    '''
    IApp
    '''
    @abstractmethod
    def command(self, name=None):
        raise NotImplementedError(NI_label)

    @abstractmethod
    def context_menu(self, name=None):
        raise NotImplementedError(NI_label)

class IClient(ABC):
    '''
    IClient
    '''
    @abstractmethod
    def run(self):
        raise NotImplementedError(NI_label)

    @abstractmethod
    def event(self, name=None):
        raise NotImplementedError(NI_label)
