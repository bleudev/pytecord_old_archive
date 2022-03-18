class DisEmbed:
    def __new__(self, title=None, embed_type=None, description=None, url=None, timestamp=None, color=None, footer_text=None, footer_icon_url=None, image_url=None, image_height=None, image_width=None,
                thumbnail_url=None, thumbnail_height=None, thumbnail_width=None, video_url=None, video_height=None, video_width=None):
        self.title: str = title
        self.type: str = embed_type
        self.description: str = description
        self.url: str = url
        self.timestamp: str = timestamp
        self.color: int = color
        self.footer_text: str = footer_text
        self.footer_icon_url: str = footer_icon_url
        self.image_url: str = image_url
        self.image_height: int = image_height
        self.image_width: int = image_width
        self.thumbnail_url: str = thumbnail_url
        self.thumbnail_height: int = thumbnail_height
        self.thumbnail_width: int = thumbnail_width
        self.video_url: str = video_url
        self.video_height: int = video_height
        self.video_width: int = video_width
        # self.video = video
        # self.provider = provider
        # self.author = author
        # self.fields = fields
        return {"title": self.title, "type": self.type, "description": self.description, "url": self.url, "timestamp": self.timestamp, "color": self.color,
                "footer": {"text": self.footer_text, "icon_url": self.footer_icon_url}, "image": {"url": self.image_url, "height": self.image_height, "width": self.image_width},
                "thumbnail": {"url": self.thumbnail_url, "height": self.thumbnail_height, "width": self.thumbnail_width}, "video": {"url": self.video_url, "height": self.video_height, "width": self.video_width}}

    def set_title(self, title):
        self.title = title

    def set_type(self, type):
        self.type = type

    def set_description(self, description):
        self.description = description

    def set_url(self, url):
        self.url = url

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def set_color(self, color):
        self.color = color