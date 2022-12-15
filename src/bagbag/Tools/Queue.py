from __future__ import annotations

try:
    from .Database import MySQL
    from .Database import SQLite
    from .Lock import Lock 
except:
    from Database import MySQL
    from Database import SQLite
    from Lock import Lock

import time
import typing
import pickle

try:
    from ..Base64 import Encode as b64encode
    from ..Base64 import Decode as b64decode
    from ..Hash import Md5sum as md5sum
    from .. import Time
except:
    import sys 
    sys.path.append("..")
    from Base64 import Encode as b64encode
    from Base64 import Decode as b64decode
    from Hash import Md5sum as md5sum
    import Time

class Queue():  
    def __init__(self, db:MySQL|SQLite):
        self.db = db 
    
    def New(self, size:int=None, queueName="_queue_empty_name_") -> namedQueue:
        queueName = ''.join(list(map(lambda x: x if x in "qazwsxedcrfvtgbyhnujmikolopQAZWSXEDCRFVTGBYHNUJMIKOLP0123456789" else "_", queueName)))
        
        if len(queueName) > 55:
            queueName = md5sum(queueName)

        if queueName != "_queue_empty_name_":
            queueName = "_queue_" + queueName
        
        if queueName not in self.db.Tables():
            self.db.Table(queueName).AddColumn("data", "text")
        
        return namedQueue(self.db, queueName, self, size)
    
    def NewConfirm(self, size:int=None, timeout:int=900, queueName:str="_queue_c_empty_name_") -> namedConfirmQueue:
        """
        这是一个需要调用Done方法来确认某个任务完成的队列
        如果不确认某个任务完成, 它就会留在队列当中等待timeout之后重新能被Get到
        优先Get到timeout的任务
        
        :param timeout: The time in seconds that the message will be available for processing, defaults
        to 900
        :type timeout: int (optional)
        :param queueName: The name of the queue, defaults to _queue_c_empty_name_
        :type queueName: str (optional)
        """
        queueName = ''.join(list(map(lambda x: x if x in "qazwsxedcrfvtgbyhnujmikolopQAZWSXEDCRFVTGBYHNUJMIKOLP0123456789" else "_", queueName)))
        
        if len(queueName) > 55:
            queueName = md5sum(queueName)

        if queueName != "_queue_empty_name_":
            queueName = "_queue_" + queueName
        
        if queueName not in self.db.Tables():
            (
                self.db.Table(queueName).
                    AddColumn("data", "text"). 
                    AddColumn("stime", "int"). 
                    AddIndex("stime")
            )
        
        return namedConfirmQueue(self.db, queueName, self, timeout, size)

class namedConfirmQueue():
    def __init__(self, db:MySQL|SQLite, name:str, tq:Queue, timeout:int, size:int) -> None:
        self.db = db 
        self.name = name 
        self.tq = tq 
        self.lock = Lock()
        self.timeout = timeout
        self.size = size
    
    def Size(self) -> int:
        """
        返回未曾开始过的新任务个数
        :return: The number of rows in the table.
        """
        return self.db.Table(self.name).Where("stime", "=", 0).Count()
    
    def SizeStarted(self) -> int:
        """
        返回正在执行的任务个数
        :return: The number of rows in the table where the stime column is not equal to 0.
        """
        return self.db.Table(self.name).Where("stime", "!=", 0).Count()
    
    def SizeTotal(self) -> int:
        """
        返回所有任务总数
        :return: The number of rows in the table.
        """
        return self.db.Table(self.name).Count()
    
    def Get(self, wait=True) -> typing.Tuple[int, typing.Any]:
        self.lock.Acquire()
        while True:
            r = self.db.Table(self.name).Where("stime", "<", int(Time.Now()) - self.timeout).OrderBy("id").First()

            if r == None:
                r = self.db.Table(self.name).Where("stime", "=", 0).OrderBy("id").First()

                if r == None:
                    if not wait:
                        self.lock.Release()
                        return -1, None 
                    else:
                        time.sleep(0.1)
                else:
                    break 
            else:
                break
        
        # self.db.Table(self.name).Where("id", "=", r["id"]).Delete()
        self.db.Table(self.name).Where("id", "=", r["id"]).Data({
            "stime": int(Time.Now()),
        }).Update()

        self.lock.Release()
        return r["id"], pickle.loads(b64decode(r["data"]))
    
    def Put(self, item:typing.Any):
        while self.size != None and self.Size() >= self.size:
            Time.Sleep(0.1)

        self.db.Table(self.name).Data({
            "data": b64encode(pickle.dumps(item)),
            # "stime": int(Time.Now()),
            "stime": 0,
        }).Insert()

    def Done(self, id:int):
        r = self.db.Table(self.name).Where("id", "=", id).First()
        if r == None:
            raise Exception("任务没找到")
        else:
            if r["stime"] == 0:
                raise Exception("任务未开始")
            else:
                self.db.Table(self.name).Where("id", "=", id).Delete()

class namedQueue():
    def __init__(self, db:MySQL|SQLite, name:str, tq:Queue, size:int) -> None:
        self.db = db 
        self.name = name 
        self.tq = tq 
        self.lock = Lock()
        self.size = size
    
    def Size(self) -> int:
        return self.db.Table(self.name).Count()
    
    def Get(self, wait=True) -> typing.Any:
        self.lock.Acquire()
        r = self.db.Table(self.name).OrderBy("id").First()
        if r == None:
            if not wait:
                self.lock.Release()
                return None 
            else:
                while r == None:
                    time.sleep(0.1)
                    r = self.db.Table(self.name).OrderBy("id").First()
        
        self.db.Table(self.name).Where("id", "=", r["id"]).Delete()

        self.lock.Release()
        return pickle.loads(b64decode(r["data"]))
    
    def Put(self, item:typing.Any):
        while self.size != None and self.Size() >= self.size:
            Time.Sleep(0.1)

        self.db.Table(self.name).Data({
            "data": b64encode(pickle.dumps(item)),
        }).Insert()

if __name__ == "__main__":
    db = MySQL("192.168.1.230")
    q = Queue(db)
    qn = q.New("queue_test")
    qn.Put(b'\x00\x00\x00\x1cftypisom\x00\x00\x02\x00isom')
    print(qn.Size())
    print(repr(qn.Get()))

    print("开启一个需要确认任务完成的队列, 3秒超时")
    qnc = q.NewConfirm(3)
    qnc.Put(b'\x00\x00\x00\x1cftypisom\x00\x00\x02\x00isom')

    print("获取任务内容")
    idx, data = qnc.Get()
    print(repr(data))

    print("等待5秒")
    Time.Sleep(5)

    print("再次获取任务")
    idx, data = qnc.Get()
    print(repr(data))

    print("确认任务完成")
    Time.Sleep(1)
    qnc.Done(idx)

    print("等待5秒")
    Time.Sleep(5)

    print("再次获取任务, 不等待")
    idx, data = qnc.Get(False)
    print(repr(data))