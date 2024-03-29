import os
import time
import typing
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
    
    def AppendLine(self, data:str|bytes):
        if os.path.dirname(self.path) != "":
            if not os.path.exists(os.path.dirname(self.path)):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if type(data) == str:
            fd = open(self.path, "a")
            data = data + "\n"
        else:
            fd = open(self.path, "ab")
            data = data + b"\n"

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
    
    def Tailf(self, fromBegin:bool=False, separator:str='\n', interval:int|float=1) -> typing.Iterable[str]:
        """
        It reads the file in chunks of 4096 bytes, and yields the lines as they are read.
        Waiting for new lines come when reach the end of the file.
        Will read from the beginning of the file if the file gets truncate.
        
        :param fromBegin: If True, the tail will start from the beginning of the file, defaults to False
        :type fromBegin: bool (optional)
        :param separator: The separator to use when splitting the file, defaults to \n
        :type separator: str (optional)
        :param interval: The time to wait between checking the file for new lines, defaults to 1 second
        :type interval: int|float (optional)
        """
        lfsize = self.Size()

        stream = open(self.path)
        if not fromBegin:
            stream.seek(0, os.SEEK_END)

        buffer = ''
        while True:
            fsize = self.Size()
            #print(lfsize, fsize)
            if lfsize > fsize:
                buffer = ''
                stream.close()
                stream = open(self.path)
            
            lfsize = fsize 

            chunk = stream.read(4096)
            if not chunk:
                time.sleep(interval)
                continue
            buffer += chunk
            while True:
                try:
                    part, buffer = buffer.split(separator, 1)
                except ValueError:
                    break
                else:
                    yield part
