'''
All: Listener
'''

class Listener:
    '''
    bot listener
    '''
    def __init__(self):
        self.events = {
            'ready': None,
            'message': None,
            'message_delete': None
        }
    async def invoke_event(self, name: str, *args, **kwrgs):
        '''
        Invoke event function in listener
        '''
        func = self.events[name]

        if func is not None:
            await func(*args, **kwrgs)

    def add_event(self, name, func):
        '''
        Add event method
        '''
        self.events[name] = func
