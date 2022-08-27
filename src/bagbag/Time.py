import time
import datetime
import tqdm

Now = time.time 

def Sleep(num:int, bar:bool=None):
    """
    Sleep(num:int, bar:bool=None)
    
    The first argument is an integer, and the second argument is a boolean. The second argument is
    optional, and if it is not provided, it will be set to True if the first argument is greater than 5,
    and False otherwise
    
    :param num: The number of seconds to sleep
    :type num: int
    :param bar: If True, a progress bar will be displayed. If False, no progress bar will be displayed.
    If None, a progress bar will be displayed if the number of seconds is greater than 5
    :type bar: bool
    """
    if bar == None:
        if num > 5:
            bar = True 
        else:
            bar = False

    if bar:
        num = int(num)
        for _ in tqdm.tqdm(range(num), total=num, leave=False):
            time.sleep(1)
    else:
        time.sleep(num)

def Strftime(format:str, timestamp:float|int) -> str:
    """
    It converts a timestamp to a string.
    
    :param format: The format string to use
    :type format: str
    :param timestamp: The timestamp to format
    :type timestamp: float|int
    :return: A string
    """
    dobj = datetime.datetime.fromtimestamp(timestamp)
    return dobj.strftime(format)

def Strptime(format:str, timestring:str) -> int:
    """
    It takes a string of a date and time, and a format string, and returns the Unix timestamp of that
    date and time
    
    :param format: The format of the timestring
    :type format: str
    :param timestring: The string to be converted to a timestamp
    :type timestring: str
    :return: The timestamp of the datetime object.
    """
    dtime = datetime.datetime.strptime(timestring, format)
    dtimestamp = dtime.timestamp()
    return int(round(dtimestamp))

if __name__ == "__main__":
    print(Strptime("%Y-%m-%d %H:%M:%S", "2022-05-02 23:34:10"))
    print(Strftime("%Y-%m-%d %H:%M:%S", 1651520050))
    print(Strftime("%Y-%m-%d %H:%M:%S", Now()))