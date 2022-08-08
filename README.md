# bagbag

An all in one python library

# Install 

```bash
pip3 install bagbag --upgrade
```

# Docker 

```bash
docker run --rm --name bagbag -v /path/to/file/run.py:/app/run.py darren2046/bagbag:latest
```

# Library

* Lg 日志模块
  * Lg.SetLevel(level:日志级别:str)
  * Lg.SetFile(path:日志路径:str, size:文件大小，MB:int, during:日志保留时间，天:int, color:是否带ANSI颜色:bool=True, json:是否格式化为json:bool=False):
  * Lg.Debug(message:str)
  * Lg.Trace(message:str)
  * Lg.Info(message:str)
  * Lg.Warn(message:str)
  * Lg.Error(message:str)
* String(string:str) 一些字符串处理函数
  * HasChinese() -> bool 是否包含中文
  * Language() -> str 语言
  * Repr() -> str
  * SimplifiedChineseToTraditional() -> str
  * TraditionalChineseToSimplified() -> str
* Time 时间
  * Strftime(format:str, timestamp:float|int) -> str
  * Strptime(format:str, timestring:str) -> int
* Re 正则
  * FindAll(pattern: str | Pattern[str], string: str, flags: _FlagsType = ...) -> list
* Base64
  * Encode(s:str) -> str
  * Decode(s:str) -> str
* Json
  * Dumps(obj, indent=4, ensure_ascii=False) -> str
  * Loads(s:str) -> list | dict
* Hash
  * Md5sum(string:str) -> str
* Os
  * Exit(num:int=0)
  * Mkdir(path:str)
* Http
  * Head(url:str, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * Get(url:str, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None,  TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * PostRaw(url:str, Data:str, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * PostJson(url:str, Json:dict,Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * PostForm(url:str, Data:dict, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * Delete(url:str, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * PutForm(url:str, Data:dict,Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
  * PutRaw(url:str, Data:str, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False, Debug:bool=False)
  * PutJson(url:str, Json:dict, Timeout:str=None, ReadBodySize:int=None, FollowRedirect:bool=True, HttpProxy:str=None, TimeoutRetryTimes:int=0, InsecureSkipVerify:int=False,Debug:bool=False)
* Socket
  * TCP
    * Listen(host:str, port:int, waitQueue:int=5)
      * Accept() -> Chan[StreamConnection]
      * AcceptOne() -> StreamConnection
    * Connect(host:str, port:int) -> StreamConnection
      * PeerAddress() -> TCPPeerAddress
      * Send(data:str)
      * SendBytes(data:bytes)
      * Recv(length:int) -> str
      * RecvBytes(length:int) -> bytes
      * Close()
* Random
  * Int(min:int, max:int) -> int
  * Choice(obj:list|str) -> Any
  * String(length:int, charset:str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> str
* Funcs
  * Wget(url:str, dest:str=None, override=True)
  * IP2Int(ip:str) -> int
  * Int2IP(intip:int) -> str
  * ResizeImage(src:str, dst:str, width:int, quality:int=95)
* Tools 一些工具
  * WebServer(name:str=\_\_name\_\_) # 例子见源码文件Web.py的后半部分
    * Run(host:str, port:int, block:bool=True) # 监听HTTP服务
    * Route: (path:str, methods:list=["GET", "HEAD", "OPTIONS"]) # 例子见Web.py文件, 是一个装饰器
    * Request()
      * Method() -> str # 请求的HTTP方法
      * Json() -> dict | list # 格式化请求的post内容为json
      * Data() -> str # post的http的body
      * Form()
        * Get(name:str, default:str="") -> str | None # 获取表单的数据
      * Args()
        * Get(name:str, default:str="") -> str | None # 获取URL的参数
  * Chan() 内存队列, 跟go的chan一样
  * RateLimit(rate:str) rate可以是 次数/时间区间, 时间可以是s, m, h, d, 即秒,分,时,天. 例如一分钟限制五次: 5/m. 在低速率的时候能限制准确, 例如低于1秒10次. 高速率例如每秒50次以上, 实际速率会降低, 速率越高降低越多. 
    * Take(sleep:bool=True) sleep=True的时候会添加一个sleep, 可以把请求平均在时间段内. 在低速率的时候能限制准确. 高速率例如每秒50次以上, 实际速率会降低, 速率越高降低越多. sleep=False的时候没有sleep, 会全在一开始扔出去, 然后block住, 等下一个周期, 在需要速率很高的时候可以这样, 例如发包的时候, 一秒限制2000个包这样.
  * URL(url:str)
    * Parse() -> URLParseResult
    * Encode() -> str
    * Decode() -> str
  * PrometheusMetricServer(listen:str="0.0.0.0", port:int=9105)
    * NewCounter(name:str, help:str) -> prometheusCounter
      * Add(num:int|float=1)
    * NewCounterWithLabel(name:str, labels:list[str], help:str) -> prometheusCounterVec
      * Add(labels:dict|list, num:int|float=1)
    * NewGauge(name:str, help:str) -> prometheusGauge
      * Set(num:int|float)
    * NewGaugeWithLabel(name:str, labels:list[str], help:str) -> prometheusGaugeVec
      * Set(labels:dict|list, num:int|float=1)
  * Queue(db:Tools.MySql|Tools.SQLite)
    * New(queueName="__queue__empty__name__") -> NamedQueue
      * Size() -> int
      * Get(waiting=True) -> str|None
      * Put(string:str)
  * Selenium(SeleniumServer:str=None)
    * ResizeWindow(width:int, height:int)
    * ScrollRight(pixel:int)
    * ScrollLeft(pixel:int)
    * ScrollUp(pixel:int)
    * ScrollDown(pixel:int)
    * Url() -> str
    * Cookie() -> List[dict]
    * SetCookie(cookie_dict:dict)
    * Refresh()
    * GetSession() -> str
    * Get(url:str)
    * PageSource() -> str
    * Title() -> str
    * Close()
    * Find(xpath:str, waiting=True) -> SeleniumElement
      * Clear() -> SeleniumElement
      * Click() -> SeleniumElement
      * Text() -> str
      * Attribute(name:str) -> str
      * Input(string:str) -> SeleniumElement
      * Submit() -> SeleniumElement
      * PressEnter() -> SeleniumElement
      * ScrollIntoElement() -> SeleniumElement
  * Telegram(appid:str, apphash:str, sessionString:str=None)
    * SessionString() -> str
    * ResolvePeerByUsername(username:str) -> TelegramPeer
      * History(limit:int=100, offset:int=0) -> list
      * Resolve() # 如果手动根据ID初始化一个TelegramPeer实例, 调用这个函数可以补全这个ID对应的Peer的信息
  * ProgressBar(iterable_obj, total=None, title=None, leave=False)
  * Redis(host: str, port: int = 6379, database: int = 0, password: str = "")
    * Set(key:str, value:str, ttl:int=None) -> (bool | None)
    * Get(key:str) -> (str | None)
    * Del(key:str) -> int
    * Lock(key:str) -> RedisLock
      * Acquire()
      * Release()
  * MySQL(host: str, port: int, user: str, password: str, database: str, prefix:str = "") # 跟5.7兼容. 因为orator跟5.7兼容, 跟8.0会有小问题, 作者很久不更新, 有空换掉这个orm. **注意, Python的MySQL操作不支持多线程, 需要每个线程连接一次MySQL, 不过这个是自动的, 在Get, Update等操作的时候如果链接异常就重连**
  * SQLite(path: str, prefix:str = "") **由于SQLite每次只能一个线程进行操作, 所以这里默认会有一个锁, 线程安全**
    * Execute(sql: str) -> (bool | int | list)
    * Tables() -> list
    * Table(tbname: str) -> MySQLSQLiteTable
      * AddColumn(colname: str, coltype: str, default=None, nullable:bool = True) -> MySQLSQLiteTable
      * AddIndex(*cols: str) -> MySQLSQLiteTable
      * Fields(*cols: str) -> MySQLSQLiteTable
      * Where(key:str, opera:str, value:str) -> MySQLSQLiteTable
      * WhereIn(key:str, value: list) -> MySQLSQLiteTable
      * WhereNotIn(key:str, value: list) -> MySQLSQLiteTable
      * WhereNull(key:str) -> MySQLSQLiteTable
      * WhereNotNull_WillNotImplement(key:str)
      * OrWhere(key:str, opera:str, value:str) -> MySQLSQLiteTable
      * OrWhereIn_WillNotImplement(key:str, value: list)
      * OrderBy(*key:str) -> MySQLSQLiteTable
      * Limit(num:int) -> MySQLSQLiteTable
      * Paginate(size:int, page:int) -> MySQLSQLiteTable
      * Data(value:map) -> MySQLSQLiteTable
      * Offset(num:int) -> MySQLSQLiteTable
      * Insert()
      * Update()
      * Delete()
      * InsertGetID() -> int
      * Exists() -> bool
      * Count() -> int
      * Find(id:int) -> map
      * First() -> map
      * Get() -> list
      * Columns() -> list[map]

其它的

* Thread(func, *args:Any) -> threading.Thread # 启动线程, daemon=True
* Process(func, *args:Any) -> multiprocessing.Process # 启动进程, daemon=True