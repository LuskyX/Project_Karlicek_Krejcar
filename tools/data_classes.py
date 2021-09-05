class VaccCenter:
    """
    class for storing data about vaccination center
    """
    def __init__(self, name: str, region: str, link: str):
        self.name = name
        self.region = region
        self.link = link
        self.vacc_id = link[39:]
        self.center_type = {}
        self.info = {}
        self.open_hours = {}
        self.vaccines = {}
        self.gps = tuple()

    def add_center_type(self, center_type: dict):
        self.center_type = center_type

    def add_info(self, info: dict):
        self.info = info

    def add_open_hours(self, open_hours: dict):
        self.open_hours = open_hours

    def add_vaccines(self, vaccines: dict):
        self.vaccines = vaccines

    def add_gps(self, gps: tuple):
        self.gps = gps

    def __repr__(self):
        return f"VaccCenter({self.name})"


class Location:
    """
    class for storing data about location
    """
    def __init__(self, name: str, gps: tuple):
        self.name = name
        self.gps = gps

    def __repr__(self):
        return f"Location({self.name})"
