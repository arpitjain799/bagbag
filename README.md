# allinone_py_lib

An all in one python library

# Install 

```bash
pip3 install allinone_py_lib --upgrade
```

# Library

* Lg 日志模块
  * Lg.SetLevel(level:日志级别:str)
  * Lg.SetFile(path:日志路径:str, size:文件大小，MB:int, during:日志保留时间，天:int, color:是否带ANSI颜色:bool=True, json:是否格式化为json:bool=False):
  * Lg.Debug(message:日志内容)
  * Lg.Trace(message:日志内容)
  * Lg.Info(message:日志内容)
  * Lg.Warn(message:日志内容)
  * Lg.Error(message:日志内容)
* String(string:str) 一些字符串处理函数
  * HasChinese() -> bool 是否包含中文
* Time 时间
  * Strftime(format:str, timestamp:float|int) -> str
  * Strptime(format:str, timestring:str) -> int
* Re 正则
  * FindAll(pattern: str | Pattern[str], string: str, flags: _FlagsType = ...) -> list
* Tools 一些工具
  * ProgressBar(iterable_obj, startfrom=0, total=None, title=None, leave=False)
  * Redis(host: str, port: int = 6379, database: int = 0, password: str = "")
    * Set(key:str, value:str, ttl:int=None) -> (bool | None)
    * Get(key:str) -> (str | None)
    * Del(key:str) -> int
    * Lock(key:str) -> RedisLock
      * Acquire()
      * Release()
  * MySQL(host: str, port: int, user: str, password: str, database: str, prefix:str = "")
  * SQLite(path: str, prefix:str = "")
    * Execute(self, sql: str) -> (bool | int | list)
    * Table(self, tbname: str) -> MySQLSQLiteTable
      * AddColumn(self, colname: str, coltype: str, default=None, nullable:bool = True) -> MySQLSQLiteTable
      * AddIndex(self, *cols: str) -> MySQLSQLiteTable
      * Fields(self, *cols: str) -> MySQLSQLiteTable
      * Where(self, key:str, opera:str, value:str) -> MySQLSQLiteTable
      * WhereIn(self, key:str, value: list) -> MySQLSQLiteTable
      * WhereNotIn(self, key:str, value: list) -> MySQLSQLiteTable
      * WhereNull(self, key:str) -> MySQLSQLiteTable
      * WhereNotNull_WillNotImplement(self, key:str)
      * OrWhere(self, key:str, opera:str, value:str) -> MySQLSQLiteTable
      * OrWhereIn_WillNotImplement(self, key:str, value: list)
      * OrderBy(self, *key:str) -> MySQLSQLiteTable
      * Limit(self, num:int) -> MySQLSQLiteTable
      * Paginate(self, size:int, page:int) -> MySQLSQLiteTable
      * Data(self, value:map) -> MySQLSQLiteTable
      * Offset(self, num:int) -> MySQLSQLiteTable
      * Insert(self)
      * Update(self)
      * Delete(self)
      * InsertGetID(self) -> int
      * Exists(self) -> bool
      * Count(self) -> int
      * Find(self, id:int) -> map
      * First(self) -> map
      * Get(self) -> list
