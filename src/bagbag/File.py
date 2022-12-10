import os

class File():
    def __init__(self, path:str):
        self.path = path 
    
    def Append(self, data:str|bytes):
        if type(data) == str:
            fd = open(self.path, "a")
        else:
            fd = open(self.path, "ab")
        fd.write(data)
        fd.close()
    
    def Write(self, data:str|bytes):
        if type(data) == str:
            fd = open(self.path, "w")
        else:
            fd = open(self.path, "wb")
        fd.write(data)
        fd.close()
    
    def Size(self) -> int:
        file_stats = os.stat(self.path)
        return file_stats.st_size
    
    def Read(self) -> str:
        return open(self.path).read()
    
    def ReadByte(self) -> bytes:
        return open(self.path, "rb").read()
    
    def __iter__(self):
        fd = open(self.path)
        while True:
            try:
                yield next(fd)
            except StopIteration:
                return 