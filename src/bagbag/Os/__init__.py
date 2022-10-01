try:
    from . import Path
except:
    import Path

# 以上是作为包给其它程序调用的时候要的, 例如Os.Path.Exists()

import os
import sys 
import shutil

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

def Unlink(path:str):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

def Move(src:str, dst:str, force:bool=True):
    if os.path.exists(dst):
        if not os.path.isdir(dst):
            if not force:
                raise Exception("目标已存在")
            else:
                os.unlink(dst)
        else:
            dst = os.path.join(dst, os.path.basename(src))

    ddir = os.path.dirname(dst)
    if ddir != "":
        if not os.path.exists(ddir):
            Mkdir(ddir)
    
    shutil.move(src, dst)

def Copy(src:str, dst:str, force:bool=True):
    if os.path.exists(dst):
        if not os.path.isdir(dst):
            if not force:
                raise Exception("目标已存在")
            else:
                os.unlink(dst)
        else:
            dst = os.path.join(dst, os.path.basename(src))
    
    ddir = os.path.dirname(dst)
    if ddir != "":
        if not os.path.exists(ddir):
            Mkdir(ddir)
    
    shutil.copy2(src, dst)

if __name__ == "__main__":
    # Move("a", "b") # 移动当前目录的a到b
    # Move("b", "c/d/e") # 移动b到c/d/e, 会先递归创建目录c/d
    Move("c/d/e", "d") # 移动c/d/e文件到d目录, 没有指定文件名就自动使用原来的文件名