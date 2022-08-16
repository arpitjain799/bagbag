import os
import sys 
from . import Path

def Exit(num:int=0):
    sys.exit(num)

System = os.system 

def Mkdir(path:str):
    os.makedirs(path, exist_ok=True)

def ListDir(path:str) -> list[str]:
    return os.listdir(path)

Args = sys.argv 

def Getenv(varname:str, defaultValue:str=None) -> str | None:
    v = os.environ.get(varname)
    if not v:
        return defaultValue
    else:
        return v