import os
import magic
import mimetypes

class File():
    def __init__(self, path:str):
        self.path = path 
    
    def Append(self, data:str|bytes):
        if os.path.dirname(self.path) != "":
            if not os.path.exists(os.path.dirname(self.path)):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if type(data) == str:
            fd = open(self.path, "a")
        else:
            fd = open(self.path, "ab")
        fd.write(data)
        fd.close()
    
    def Write(self, data:str|bytes):
        if os.path.dirname(self.path) != "":
            if not os.path.exists(os.path.dirname(self.path)):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)

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
    
    def TypeDescription(self) -> str:
        """
        根据文件内容生成描述
        Example: PDF document, version 1.2
        """
        if not os.path.exists(self.path) or not os.path.isfile(self.path):
            raise Exception("文件不存在:", self.path)
        
        return magic.from_file(self.path)
    
    def MimeType(self) -> str:
        """
        根据文件内容生存mime类型
        """
        if not os.path.exists(self.path) or not os.path.isfile(self.path):
            raise Exception("文件不存在:", self.path)
        
        mime = magic.Magic(mime=True)
        return mime.from_file(self.path)
    
    def GuessSuffix(self) -> str:
        """
        根据文件内容生成扩展名
        返回值包括前置"."
        例如: .jpg
        :return: The file extension of the file.
        """
        return mimetypes.guess_extension(self.MimeType())