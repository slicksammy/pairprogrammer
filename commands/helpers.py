import os

def is_relative(path):
    return not os.path.isabs(path) and '..' not in path