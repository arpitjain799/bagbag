from __future__ import annotations

import argparse

class Argparse():
    def __init__(self, description:str=None) -> None:
        self.parser = argparse.ArgumentParser(description=description)

    def Add(self, arg:str, default:str=None, help:str=None) -> Argparse:
        return self.AddString(arg, default, help)
    
    def AddString(self, arg:str, default:str=None, help:str=None) -> Argparse:
        self.parser.add_argument(arg, default=default, help=help, type=str)
        return self
    
    def AddBool(self, arg:str, default:bool=False, help:str=None) -> Argparse:
        self.parser.add_argument(arg, default=default, help=help, action='store_true')
        return self
    
    def AddInt(self, arg:str, default:bool=None, help:str=None) -> Argparse:
        self.parser.add_argument(arg, default=default, help=help, type=int)
        return self
    
    def AddFloat(self, arg:str, default:bool=None, help:str=None) -> Argparse:
        self.parser.add_argument(arg, default=default, help=help, type=float)
        return self
    
    def Get(self):
        return self.parser.parse_args()

if __name__ == "__main__":
    args = (
        Argparse().
        AddBool("--arg1").
        AddString("arg2"). 
        Add("arg3", "help string 3"). 
        Add("--optionArgs4"). 
        Add("--optionArgs5", "defaultValue5").
        Add("--optionArgs6", "defaultValue6", "help string 6"). 
        AddInt("intKey"). 
        AddFloat("--floatKey").
        Get()
    )
    print(args.arg3)
    print(args.floatKey)
    print(args)
