class VaccCenter():
    def __init__(self, name, region, link, no_registration):
        self.name = name
        self.region = region
        self.link = link
        self.no_registration = no_registration
        self.info = {}
        self.open_hours = {}

    def add_info(self, info):
        self.info = info

    def add_open_hours(self, open_hours):
        self.open_hours = open_hours

    def __repr__(self):
        return f"VaccCenter({self.name})"