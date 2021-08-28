class VaccCenter():
    def __init__(self, name, region, link):
        self.name = name
        self.region = region
        self.link = link

    def __repr__(self):
        return f"VaccCenter({self.name})"