import os

def is_relative(self, path):
    return not os.path.isabs(path) and '..' not in path