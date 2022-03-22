class DisField:
    def __init__(self, name: str, value: str, inline: bool = True):
        self.name = name
        self.value = value
        self.inline = inline

    def tojson(self):
        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline
        }

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

    def tojson(self):
        fields_jsons = []

        for f in self.fields:
            fields_jsons.append(f.tojson())

        return {
            "title": self.title,
            "description": self.description,
            "footer": self.footer,
            "color": self.color,
            "fields": fields_jsons
        }
