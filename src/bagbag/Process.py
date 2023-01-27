import multiprocessing 
from typing import Any

def Process(func, *args:Any, daemon:bool=True) -> multiprocessing.Process:
    """
    注意调用这个函数的时候要放到if __name__ == "__main__"里面, 否则可能会报错
    
    `Process` is a function that takes a function and its arguments, and returns a
    `multiprocessing.Process` object that runs the function in a separate process. 
    
    :param func: The function to be executed
    :param : func: The function to be executed
    :type : Any
    :param daemon: If True, the process’s daemon flag will be set, defaults to True
    :type daemon: bool (optional)
    :return: A multiprocessing.Process object.
    """
    p = multiprocessing.Process(target=func, args=args)
    p.daemon = daemon 
    p.start()

    return p 

# import time 
# 
# def p(s:str, ss:str):
#     while True:
#         time.sleep(1)
#         print(s, ss, time.time())

if __name__ == "__main__":
    p = Process(p, "oo", "kk")

    while True:
        time.sleep(1)



