# import importlib
# importlib.enable_lazy_imports_in_module() 

import ipdb
import traceback
import sys
import selenium

from . import Lg
from . import Tools
from . import Time
from . import Base64
from . import Json
from . import Os
from . import Funcs
from . import Re
from . import Hash
from . import Http
from . import Socket 
from . import Random
from . import Math

# __all__ = ['Lg', 'Tools', 'Time', 'Base64', 'Json', 'Json', 'Os', 'Funcs', 'Re', 'Hash', 'Http', 'Socket', 'Random', 'Math']

# def __getattr__(name):
#   if name in __all__:
#     print("import " + name)
#     return importlib.import_module("." + name, __name__)
#   else:
#     raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# def __dir__():
#   return __all__

from . import Cryptoo as Crypto

from .File import File
from .Thread import Thread
from .Process import Process
from .Python import Range
from .String import String
from . import Cmd

# import re
# import forbiddenfruit

# def __hasChinese(self) -> bool:
#     return len(re.findall(r'[\u4e00-\u9fff]+', self)) != 0

# forbiddenfruit.curse(str, "HasChinese", __hasChinese)

