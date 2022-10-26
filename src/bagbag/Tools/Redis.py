from __future__ import annotations

import redis 
import pickle
import typing
import time

class RedisException(Exception):
    pass 

class RedisQueueClosed(RedisException):
    pass 

def RetryOnNetworkError(func): # func是被包装的函数
    def ware(self, *args, **kwargs): # self是类的实例
        while True:
            try:
                res = func(self, *args, **kwargs)
                break
            except Exception as e:
                if True in map(lambda x: e.args[0].startswith(x), ['Connection closed by server', 'Error 61 connecting to ']):
                    time.sleep(0.5)

        return res
    
    return ware

class RedisQueue():
    """Simple Queue with Redis Backend"""
    def __init__(self, rdb:redis.Redis, name:str, length:int=0):
        self.rdb = rdb
        self.key = '%s:%s' % ('redis_queue', name)
        self.closed = False
        self.length = length

    @RetryOnNetworkError
    def Size(self) -> int:
        """Return the approximate size of the queue."""
        return self.rdb.llen(self.key)

    @RetryOnNetworkError
    def Put(self, item:typing.Any):
        """Put item into the queue."""
        while self.length > 0 and self.Size() >= self.length:
            time.sleep(0.3)

        self.rdb.rpush(self.key, pickle.dumps(item))

    @RetryOnNetworkError
    def Get(self, block=True, timeout=None) -> typing.Any:
        """Remove and return an item from the queue. 

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.rdb.blpop(self.key, timeout=timeout)
        else:
            item = self.rdb.lpop(self.key)

        if item:
            item = item[1]

        return pickle.loads(item)
    
    def Close(self):
        self.closed = True

    def __iter__(self):
        return self 
    
    def __next__(self):
        try:
            return self.Get()
        except RedisQueueClosed:
            raise StopIteration

class RedisLock():
    def __init__(self, lock):
        self.lock = lock

    @RetryOnNetworkError
    def Acquire(self):
        """
        The function Acquire() is a method of the class Lock. It acquires the lock
        """
        self.lock.acquire()
    
    @RetryOnNetworkError
    def Release(self):
        """
        The function releases the lock
        """
        self.lock.release()

class Redis():
    def __init__(self, host: str, port: int = 6379, database: int = 0, password: str = ""):
        """
        It creates a Redis object.
        
        :param host: The hostname or IP address of the Redis server
        :type host: str
        :param port: The port number of the Redis server. The default is 6379, defaults to 6379
        :type port: int (optional)
        :param database: The database number to connect to, defaults to 0
        :type database: int (optional)
        :param password: The password to use to connect to the Redis server
        :type password: str
        """
        self.rdb = redis.Redis(host=host, port=port, db=database, password=password)
    
    def Ping(self) -> bool:
        """
        This function returns a boolean value that indicates whether the connection to the Redis server
        is still alive
        :return: A boolean value.
        """
        return self.rdb.ping()
    
    # https://redis.readthedocs.io/en/v4.3.4/commands.html#redis.commands.core.CoreCommands.set
    # ttl, second
    @RetryOnNetworkError
    def Set(self, key:str, value:str, ttl:int=None) -> (bool | None):
        """
        It sets the value of a key in the database.
        
        :param key: The key to set
        :type key: str
        :param value: The value to be stored in the key
        :type value: str
        :param ttl: Time to live in seconds
        :type ttl: int
        :return: The return value is a boolean value.
        """
        return self.rdb.set(key, value, ex=ttl)
    
    # https://redis.readthedocs.io/en/v4.3.4/commands.html#redis.commands.core.CoreCommands.get
    @RetryOnNetworkError
    def Get(self, key:str) -> (str | None):
        """
        It gets the value of a key from the redis database.
        
        :param key: The key to get the value of
        :type key: str
        :return: A string or None
        """
        res = self.rdb.get(key)
        if res:
            return res.decode('utf-8')
        else:
            return res

    # https://redis.readthedocs.io/en/v4.3.4/commands.html#redis.commands.core.CoreCommands.delete
    @RetryOnNetworkError
    def Del(self, key:str) -> bool:
        """
        It deletes the key from the database
        
        :param key: The key to delete
        :type key: str
        :return: The return value is a boolean value.
        """
        return self.rdb.delete(key) == 1
    
    # https://redis.readthedocs.io/en/latest/connections.html?highlight=lock#redis.Redis.lock
    @RetryOnNetworkError
    def Lock(self, key:str) -> RedisLock:
        """
        It returns a RedisLock object.
        
        :param key: The key to lock
        :type key: str
        :return: A RedisLock object.
        """
        return RedisLock(self.rdb.lock("redis_lock:" + key))
    
    @RetryOnNetworkError
    def Queue(self, key:str, length:int=0) -> RedisQueue:
        """
        It creates a RedisQueue object.
        
        :param key: The key of the queue
        :type key: str
        :return: RedisQueue
        """
        return RedisQueue(self.rdb, key, length)

if __name__ == "__main__":
    r = Redis("192.168.168.21")
    r.Ping()
    print(1, r.Get("key"))
    print(2, r.Set("key", "value"))
    print(3, r.Get("key"))
    print(4, r.Del("key"))
    print(5, r.Get("key"))
    l = r.Lock("lock_key")
    l.Acquire()
    l.Release()

    q = r.Queue('queue')
    q.Put('1')
    q.Put('2')

    for v in q:
        print("value: ", v)


