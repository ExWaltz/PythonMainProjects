import os
from pathlib import Path


def getCwd():
    return os.getcwd()


def getDir(path="c:/"):
    strPath = path.replace("\\", "/")
    return [f'{strPath}{f}' for f in os.listdir(path)]


def getName(file):
    return Path(str(file)).name
