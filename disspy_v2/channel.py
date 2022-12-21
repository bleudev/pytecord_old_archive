class Message:
    def __init__(self, session, **data) -> None:
        self.id = data['id']
