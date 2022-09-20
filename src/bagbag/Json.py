import json

def Dumps(obj, indent=4, ensure_ascii=False) -> str:
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii)

def Loads(s:str) -> list | dict:
    return json.loads(s)

def ExtraValueByKey(obj:list|dict, key:str) -> list:
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
                    
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

if __name__ == "__main__":
    j = Dumps({1: 3, 4: 5})
    print(j)

    d = Loads(j)
    print(d)

    print(type(d))