import hashlib
    

def Md5sum(data:str|bytes) -> str:
    if type(data) == str:
        data = data.encode('utf-8')
    return hashlib.md5(data).hexdigest()

def Md5sumFile(fpath:str, block_size=2**20) -> str:
    md5 = hashlib.md5()
    with open(fpath, "rb" ) as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

if __name__ == "__main__":
    print(Md5sum("abc"))
