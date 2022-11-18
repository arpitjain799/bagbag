import hashlib
    

def Md5sum(data:str|bytes) -> str:
    if type(data) == str:
        data = data.encode('utf-8')
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    print(Md5sum("abc"))
