class Command:
    def __init__(self, data: dict) -> None:
        self.data = data
    def eval(self) -> dict:
        return self.data

class AppClient:
    def __init__(self) -> None:
        self.commands = []

    def add_command(self, command: Command):
        self.commands.append(command)

def describe(**options):
    def wrapper(func):
        try:
            return options, func[1], 'describe'
        except TypeError:
            return options, func, 'describe'
    return wrapper
