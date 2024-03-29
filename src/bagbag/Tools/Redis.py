from __future__ import annotations

import redis 
import pickle
import typing
import time
import shortuuid

try:
    from .. import Lg
    from .. import Base64
    from ..Process import Process
except:
    import sys
    sys.path.append("..")
    import Lg
    import Base64
    from Process import Process

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
                Lg.Trace(str(e))
                if True in map(lambda x: x in str(e), [
                    'Connection closed by server', 
                    'Error 61 connecting to ', 
                    'Connection refused',
                    'timed out'
                ]):
                    time.sleep(3)
                else:
                    raise e

        return res
    
    return ware

class redisQueue():
    def __init__(self, rdb:redis.Redis, name:str, length:int=0):
        self.rdb = rdb
        self.basename = 'rq'
        self.name = name
        self.key = '%s:%s' % (self.basename, self.name)
        self.closed = False
        self.length = length

    @RetryOnNetworkError
    def Size(self) -> int:
        """Return the approximate size of the queue."""
        return self.rdb.llen(self.key)

    @RetryOnNetworkError
    def Put(self, item:typing.Any, force:bool=False):
        """Put item into the queue."""
        if force == False:
            while self.length > 0 and self.Size() >= self.length:
                time.sleep(0.3)

        self.rdb.rpush(self.key, pickle.dumps(item, protocol=2))

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
    
    @RetryOnNetworkError
    def CheckNext(self, block:bool=True, timeout:int=None) -> typing.Any:
        """
        If the queue is empty, wait until it's not empty, then return the first item in the queue, will NOT pop out the item. 
        
        :param block: If True, the method will block until an item is available. If False, it will
        return immediately, defaults to True
        :type block: bool (optional)
        :param timeout: The maximum time to wait for an item to be available
        :type timeout: int
        """
        if block:
            stime = time.time()
            while True:
                item = self.rdb.lindex(self.key, 0)
                if item == None:
                    time.sleep(0.2)
                else:
                    break 
                if timeout != None:
                    if time.time() - timeout > stime:
                        return None
        else:
            item = self.rdb.lindex(self.key, 0)
        
        if item != None:
            return pickle.loads(item)
        else:
            return None 
    
    def Close(self):
        self.closed = True

    def __iter__(self):
        return self 
    
    def __next__(self):
        try:
            return self.Get()
        except RedisQueueClosed:
            raise StopIteration

class redisQueueConfirm():
    def __init__(self, rdb:redis.Redis, name:str, length:int=0, timeout:int=300):
        self.rdb = rdb
        self.basename = 'rq'
        self.name = name 
        self.key = '%s:%s' % (self.basename, self.name)
        self.closed = False
        self.length = length
        self.timeout = timeout
        self.collectorLock = self.rdb.lock("redis_lock:redisQueueConfirmdCollectorLock", timeout=120)
        self.queueOperaLock = self.rdb.lock("redis_lock:%s:queueConfirmdOperaLock" % name, timeout=5)

        self.rdb.config_set("notify-keyspace-events", "KEA")
        self.RunExpireCollector()
    
    @RetryOnNetworkError
    def RunExpireCollector(self):
        def event_handler(msg):
            self.collectorLock.acquire()
            try:
                key = str(msg["data"].decode("utf-8"))
                if key.startswith(self.key + ":doing:shadow:"):
                    tid = key.replace(self.key + ":doing:shadow:", "")

                    if self.rdb.exists(self.key + ":doing:" + tid) == True:
                        # Lg.Trace("重新发布任务:", msg["data"])
                        value = self.rdb.get(self.key + ":doing:" + tid)
                        self.rdb.rpush(self.key, value)

                        self.rdb.delete(self.key + ":doing:" + tid)
            except Exception as exp:
                pass
            self.collectorLock.release()

        pubsub = self.rdb.pubsub()
        pubsub.psubscribe(**{"__keyevent@0__:expired": event_handler})
        pubsub.run_in_thread(sleep_time=1, daemon=True)

    @RetryOnNetworkError
    def Size(self) -> int:
        """Return the approximate size of the queue."""
        return self.rdb.llen(self.key)

    @RetryOnNetworkError
    def Put(self, item:typing.Any, block:bool=True, force:bool=False) -> bool:
        """Put item into the queue."""
        if force == False:
            if block:
                while self.length > 0 and self.Size() >= self.length:
                    time.sleep(0.3)
            else:
                if self.length > 0 and self.Size() >= self.length:
                    return False

        self.rdb.rpush(self.key, pickle.dumps(item, protocol=2))
        return True

    @RetryOnNetworkError
    def Get(self, block:bool=True, timeout:int=None) -> typing.Tuple[str, typing.Any]:
        """Remove and return an item from the queue. 

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""

        self.queueOperaLock.acquire()

        if block:
            count = 0
            while True:
                item = self.rdb.lpop(self.key)
                if item != None:
                    break 
                else:
                    self.queueOperaLock.release()

                    count += 1
                    if timeout != None and count > timeout:
                        break 
  
                    time.sleep(1)
                    self.queueOperaLock.acquire()
        else:
            item = self.rdb.lpop(self.key)

        # Lg.Trace(item)
        if item != None:
            tid = shortuuid.uuid()

            self.rdb.set(self.key + ":doing:" + tid, item)
            self.rdb.set(self.key + ":doing:shadow:" + tid, "", ex=self.timeout)

            self.queueOperaLock.release()
            return tid, pickle.loads(item)
        else:
            self.queueOperaLock.release()
            return None, None
    
    @RetryOnNetworkError
    def CheckNext(self, block:bool=True, timeout:int=None) -> typing.Any:
        """
        If the queue is empty, wait until it's not empty, then return the first item in the queue, will NOT pop out the item. 
        
        :param block: If True, the method will block until an item is available. If False, it will
        return immediately, defaults to True
        :type block: bool (optional)
        :param timeout: The maximum time to wait for an item to be available
        :type timeout: int
        """
        if block:
            stime = time.time()
            while True:
                item = self.rdb.lindex(self.key, 0)
                if item == None:
                    time.sleep(0.2)
                else:
                    break 
                if timeout != None:
                    if time.time() - timeout > stime:
                        return None
        else:
            item = self.rdb.lindex(self.key, 0)
        
        if item != None:
            return pickle.loads(item)
        else:
            return None 
    
    @RetryOnNetworkError
    def Done(self, tid:str):
        self.rdb.delete(self.key + ":doing:" + tid)
        self.rdb.delete(self.key + ":doing:shadow:" + tid)
    
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

class redisHashMap():
    def __init__(self, rdb:redis.Redis, key:str, ttl:int=None) -> None:
        self.rdb = rdb
        self.key = key 
        self.ttl = ttl

        self.hlen = self.rdb.hlen(key)
    
    @RetryOnNetworkError
    def Set(self, key:str, value:typing.Any=None):
        if type(value) == int:
            value = "i " + str(value)
        elif type(value) == str:
            value = "s " + str(value)
        elif type(value) == float:
            value = "f " + str(value)
        else:
            value = "p " + Base64.Encode(pickle.dumps(value, protocol=2))
        
        self.rdb.hset(self.key, key, value)
        if self.hlen == 0 and self.ttl != None:
            # Lg.Trace("set expire:", self.ttl)
            self.rdb.expire(name=self.key, time=self.ttl)
        
        self.hlen = self.rdb.hlen(self.key)
    
    @RetryOnNetworkError
    def Get(self, key:str, default:typing.Any=None) -> typing.Any:
        res = self.rdb.hget(self.key, key)

        if res != None:
            if res[:2] == b"i ":
                res = int(res[2:])
            elif res[:2] == b"s ":
                res = res[2:]
            elif res[:2] == b"f ":
                res = float(res[2:])
            elif res[:2] == b"p ":
                res = pickle.loads(Base64.Decode(res[2:])) 
            else:
                res = pickle.loads(Base64.Decode(res)) 
        else:
            res = default 
        
        return res
    
    @RetryOnNetworkError
    def Exists(self, key:str) -> bool:
        return self.rdb.hexists(self.key, key)

    @RetryOnNetworkError
    def Delete(self, key:str):
        # self.rdb.delete(self.key)
        self.rdb.hdel(self.key, key)

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
        self.namespace = []

    def __key(self, key:str) -> str:
        if len(self.namespace) == 0:
            return key 
        else:
            return ':'.join(self.namespace) + ":" + key
        
    def HashMap(self, key:str, ttl:int=None) -> redisHashMap:
        """
        It returns a redisHashMap object.
        如果hashmap不存且ttl不为None在则在设置第一个元素的时候设置这个map的ttl.
        如果hashmap已存在则不设置ttl.
        
        :param key: The key to use for the hashmap
        :type key: str
        :param ttl: Time to live in seconds for the hashmap object since it created. If not specified, the key will never expire
        :type ttl: int
        :return: A redisHashMap object
        """
        return redisHashMap(self.rdb, self.__key(key), ttl)
    
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
    def Set(self, key:str, value:typing.Any, ttl:int=None) -> (bool | None):
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
        if type(value) == int:
            value = "i " + str(value)
        elif type(value) == str:
            value = "s " + str(value)
        elif type(value) == float:
            value = "f " + str(value)
        else:
            value = "p " + Base64.Encode(pickle.dumps(value, protocol=2))

        return self.rdb.set(self.__key(key), value, ex=ttl)
    
    # https://redis.readthedocs.io/en/v4.3.4/commands.html#redis.commands.core.CoreCommands.get
    @RetryOnNetworkError
    def Get(self, key:str, default:typing.Any=None) -> typing.Any:
        """
        It gets the value of a key from the redis database.
        
        :param key: The key to get the value of
        :type key: str
        :return: A string or None
        """
        res = self.rdb.get(self.__key(key))

        if res != None:
            # res = res.decode()
            if res[:2] == b"i ":
                res = int(res[2:])
            elif res[:2] == b"s ":
                res = res[2:]
            elif res[:2] == b"f ":
                res = float(res[2:])
            elif res[:2] == b"p ":
                res = pickle.loads(Base64.Decode(res[2:])) 
            else:
                # 为了兼容之前的代码
                try:
                    res = pickle.loads(Base64.Decode(res)) 
                except:
                    res = pickle.loads(res)
        else:
            res = default 

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
        return self.rdb.delete(self.__key(key)) == 1
    
    @RetryOnNetworkError
    def Exists(self, key:str) -> bool:
        """
        It returns True if the key exists in the database, and False if it doesn't
        
        :param key: The key to check for existence
        :type key: str
        :return: A boolean value.
        """
        return self.rdb.exists(self.__key(key)) == True
    
    @RetryOnNetworkError
    def NotExists(self, key:str) -> bool:
        return self.rdb.exists(self.__key(key)) == False
    
    # https://redis.readthedocs.io/en/latest/connections.html?highlight=lock#redis.Redis.lock
    @RetryOnNetworkError
    def Lock(self, key:str, timeout:int=300) -> RedisLock:
        """
        It returns a RedisLock object.
        
        :param key: The key to lock
        :type key: str
        :return: A RedisLock object.
        """
        return RedisLock(self.rdb.lock("redis_lock:" + self.__key(key), timeout=300))
    
    @RetryOnNetworkError
    def Queue(self, name:str, length:int=0) -> redisQueue:
        """
        It creates a redisQueue object.
        
        :param key: The key of the queue
        :type key: str
        :return: redisQueue
        """
        return redisQueue(self.rdb, self.__key(name), length)

    def QueueConfirm(self, name:str, length:int=0, timeout:int=300) -> redisQueueConfirm:
        """
        It creates a new redisQueueConfirm object.
        
        :param name: The name of the queue
        :type name: str
        :param length: The maximum length of the queue. If the queue is full, the oldest item will be
        removed, defaults to 0
        :type length: int (optional)
        :return: A redisQueueConfirm object.
        """
        return redisQueueConfirm(self.rdb, self.__key(name), length, timeout)
    
    def Key(self, key:str) -> redisKey: 
        return redisKey(self, key) # 之后会调用self的set, 会设置ns, 所以这里不用配置

    def Namespace(self, namespace:str) -> redisNamespaced:
        return redisNamespaced(self.rdb, namespace)

class redisNamespaced(Redis):
    def __init__(self, rdb:Redis, namespace:str) -> None:
        self.rdb = rdb
        self.namespace = [namespace]
    
    def Namespace(self, namespace: str) -> redisNamespaced:
        self.namespace.append(namespace)
        return self

class redisKey():
    def __init__(self, kv:Redis, key:str) -> None:
        self.key = key 
        self.kv = kv
        self.lock = self.kv.Lock("redis_key_lock:%s" % key)
    
    def Set(self, value:typing.Any):
        self.kv.Set(self.key, value)
    
    def Get(self, default:typing.Any=None):
        return self.kv.Get(self.key, default)
    
    def Add(self, num:int|float=1) -> redisKey:
        self.lock.Acquire()
        n = self.kv.Get(self.key, 0)
        self.kv.Set(self.key, n + num)
        self.lock.Release()

        return self
    
    def __add__(self, num:int|float) -> redisKey:
        return self.Add(num)
    
    def __iadd__(self, num:int|float) -> redisKey:
        return self.Add(num)

if __name__ == "__main__":
    # r = Redis("192.168.1.224")
    # r.Ping()
    # print(1, r.Get("key"))
    # print(2, r.Set("key", "value"))
    # print(3, r.Get("key"))
    # print(4, r.Del("key"))
    # print(5, r.Get("key"))
    # l = r.Lock("lock_key")
    # l.Acquire()
    # l.Release()

    # q = r.Queue('queue')
    # q.Put('1')
    # q.Put('2')

    # for v in q:
    #     print("value: ", v)

    # r = Redis("192.168.168.21")
    # rns = r.Namespace("ns1")
    # rnsk = rns.Key("key1")
    # rnsk += 1

    # r = Redis("10.129.129.224")
    # k = r.Key("testkey")
    # k.Set(1)
    # k.Get()
    pass
    