from __future__ import annotations

try:
    from .. import Http
    from .. import Lg
    from .. import Random
    from .. import Hash
    from .. import Json
    from ..Http import useragents 
except:
    import sys 
    sys.path.append("..")
    import Http
    import Lg
    import Random
    import Hash
    import Json
    from Http import useragents 

import pygtrans

class Baidu():
    def __init__(self, appid:str, secretkey:str) -> None:
        self.appid = appid 
        self.secretkey = secretkey 
        self.apiurl = "http://api.fanyi.baidu.com/api/trans/vip/translate"
        self.to = "zh"
        self.From = "auto"

    def SetLang(self, To:str="zh", From:str="auto") -> Baidu:
        self.ffrom = From 
        self.to = To 
        return self 
    
    def Translate(self, text:str) -> dict:
        if "\n" in text:
            raise Exception("不允许换行符哦")

        salt = str(Random.Int(32768, 65536))
        preSign = self.appid + text + salt + self.secretkey
        sign = Hash.Md5sum(preSign)
        params = {
            "q":     text,
            "from":  self.ffrom,
            "to":    self.to,
            "appid": self.appid,
            "salt":  salt,
            "sign":  sign,
        }
        resp = Http.Get(self.apiurl, params)
        if resp.StatusCode != 200:
            raise Exception(f"翻译出错, 状态码: {resp.StatusCode}, 返回内容: {resp.Content}")
        
        rj = Json.Loads(resp.Content)

        return rj 

class Google():
    def __init__(self, httpProxy:str=None) -> None:
        self.httpProxy = httpProxy
        self.to = "zh-CN"
        self.From = "auto"

    def SetLang(self, To:str="zh-CN", From:str="auto") -> Google:
        self.From = From 
        self.to = To 
        return self 
    
    def Translate(self, text:str, format:str="html") -> str:
        """
        It translates the text from one language to another.
        
        :param text: The text to be translated
        :type text: str
        :param format: The format of the text to be translated, defaults to html. 可选html或者text
        :type format: str (optional)
        """
        client = pygtrans.Translate(
            target=self.to,
            source=self.From,
            fmt='html',
            user_agent=Random.Choice(useragents)['user_agent'],
            domain='com', # cn或者com
            proxies={"http": self.httpProxy},
        )
        return client.translate(text).translatedText

if __name__ == "__main__":
    # appid, secretkey = open("baidu.ident").read().strip().split(',')
    # b = Baidu(appid, secretkey).SetLang("zh", "auto")
    # b.Translate("This is a test")

    g = Google("http://192.168.1.186:8899").SetLang("zh-CN")
    text = g.Translate("This is a test")
    Lg.Trace(text)