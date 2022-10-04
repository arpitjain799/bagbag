

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