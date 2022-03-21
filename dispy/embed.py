class DisField:
    def __init__(self, title: str, value: str):
        self.title = title
        self.value = value


class DisEmbed:
    def __init__(self, title: str, description: str = None, color=0xffffff, footer: str = None):
        self.title = title
        self.description = description
        self.color = color
        self.footer = footer

        self.fields = []

    def add_field(self, title: str, value: str):
        self.fields.append(DisField(title, value))

    def add_field(self, field: DisField):
        self.fields.append(field)
