from .parsers.json import Json

class Interface:
    VERSION_TO_CLASSES = {
        "json": Json
    }

    def __init__(self, version):
        self.version = version

    def parse_response(self, response):
        klass = Interface.VERSION_TO_CLASSES[self.version]
        return klass.parse_response(response)
    
    def prompt(self):
        klass = Interface.VERSION_TO_CLASSES[self.version]
        return klass.prompt()