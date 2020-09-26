import os
from pathlib import Path


def getCwd():
    cwd = os.getcwd()
    cwd = cwd.replace("\\", "/")
    return cwd


def getDir(path="c:/"):
    strPath = path.replace("\\", "/")
    rLists = [f'{strPath}/{f}' for f in os.listdir(path)]
    return rLists


def dirList(dirs):
    if not isinstance(dirs, list):
        dirs = (dirs,)
    dirL = [e for e in dirs if os.path.isdir(e)]
    return dirL


def isFile(path):
    return os.path.isfile(str(path))


def isDir(path):
    return os.path.isdir(str(path))


def fileList(dirs):
    if not isinstance(dirs, list):
        dirs = (dirs,)
    fileL = [e for e in dirs if os.path.isfile(e)]
    return fileL


def getName(file):
    return Path(str(file)).name
