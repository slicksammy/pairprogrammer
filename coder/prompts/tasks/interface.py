from .tasks.new_line import Newline

class Interface:
    CLASSES = {
        "newline": Newline
    }

    def __init__(self, version):
        self.klass = Interface.CLASSES[version]

    def prompt(self, tasks):
       return self.klass.prompt(tasks)