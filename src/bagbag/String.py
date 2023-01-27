import re
import langid
import opencc
import ipaddress
import pypinyin
from urllib.parse import quote_plus, unquote
from . import Re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import OrderedDict

sentimentAnalyzer = SentimentIntensityAnalyzer()

addrPattern = OrderedDict({
    "xmr":      "4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}",
    "bech32":   "bc(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87})",
    "eth":      "(0x)[a-zA-Z0-9]{40}",
    "btc":      "(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}",
    "zec":      "(t)[a-zA-Z0-9]{34}",
    "btg":      "([GA])[a-zA-HJ-NP-Z0-9]{24,34}",
    "dash":     "X[1-9A-HJ-NP-Za-km-z]{33}",
    "dgb":      "(D)[a-zA-Z0-9]{24,33}",
    "smart":    "(S)[a-zA-Z0-9]{33}",
    "xrp":      "(r)[a-zA-Z0-9]{33}",
    "zcr":      "(Z)[a-zA-Z0-9]{33}",
    "trx":      "T[A-Za-z1-9]{33}",
    "litecoin": "[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}",
})

class cryptoAddress():
    def __init__(self, ctype:str, address:str) -> None:
        self.Type = ctype 
        self.Address = address
    
    def __repr__(self) -> str:
        return f"cryptoAddress(Type={self.Type} Address={self.Address})"

    def __str__(self) -> str:
        return f"cryptoAddress(Type={self.Type} Address={self.Address})"

class sentimentResult():
    def __init__(self) -> None:
        self.Negative:float = 0 # 消极的
        self.Neutral:float = 0 # 中性的
        self.Positive:float = 0 # 积极的
        self.Compound:float = 0 # 复合情绪
    
    def __repr__(self) -> str:
        return f"sentimentResult(Negative={self.Negative} Neutral={self.Neutral} Positive={self.Positive} Compound={self.Compound})"

    def __str__(self) -> str:
        return f"sentimentResult(Negative={self.Negative} Neutral={self.Neutral} Positive={self.Positive} Compound={self.Compound})"

class String():
    def __init__(self, string:str):
        self.string = string 
    
        """
        > If there are any Chinese characters in the string, return `True`. Otherwise, return `False`
        :return: A boolean value.
        """
    
    def Sentiment(self) -> sentimentResult:
        res = sentimentAnalyzer.polarity_scores(self.string)
        # {'neg': 0.189, 'neu': 0.811, 'pos': 0.0, 'compound': -0.8331}

        resr = sentimentResult()
        resr.Negative = res['neg']
        resr.Neutral = res['neu']
        resr.Positive = res['pos']
        resr.Compound = res['compound']

        return resr
    
    def CryptoAddress(self) -> list[cryptoAddress]:
        resca = []

        for ctype in addrPattern:
            pattern = addrPattern[ctype]
            text = self.string

            res = Re.FindAll(pattern, text)
            if len(res) != 0:
                for r in res:
                    address = r[0]

                    if len(Re.FindAll("[@_/#A-Za-z0-9]" + address, text)) != 0 or len(Re.FindAll(address + "[_/#A-Za-z0-9]", text)) != 0:
                        continue 

                    if len(Re.FindAll("[0-9]", address)) == 0:
                        continue 

                    if len(Re.FindAll("[A-Z]", address)) == 0:
                        continue 

                    if len(Re.FindAll("[a-z]", address)) == 0:
                        continue 

                    if len(Re.FindAll('https{0,1}://.+?' + address, text)) != 0:
                        continue 

                    if len(Re.FindAll("[a-z]{"+str(int(len(address)/3))+",}", address)) != 0:
                        continue 

                    if len(Re.FindAll("[A-Z]{"+str(int(len(address)/3))+",}", address)) != 0:
                        continue 
                    
                    resca.append(cryptoAddress(ctype, address))
        
        return resca

    def HasChinese(self) -> bool:
        return len(re.findall(r'[\u4e00-\u9fff]+', self.string)) != 0
    
    def Language(self) -> str:
        """
        The function takes a string as input and returns the language of the string
        :return: The language of the string.
        """
        return langid.classify(self.string)[0]

    def Repr(self) -> str:
        return str(repr(self.string).encode("ASCII", "backslashreplace"), "ASCII")[1:-1]
    
    def SimplifiedChineseToTraditional(self) -> str:
        return opencc.OpenCC('s2t.json').convert(self.string)
    
    def TraditionalChineseToSimplified(self) -> str:
        return opencc.OpenCC('t2s.json').convert(self.string)
    
    def Ommit(self, length:int) -> str:
        """
        If the length of the string is greater than the length of the argument, return the string up to
        the length of the argument and add "..." to the end. Otherwise, return the string
        
        :param length: The length of the string you want to return
        :type length: int
        :return: The string is being returned.
        """
        if len(self.string) > length:
            return self.string[:length] + "..."
        else:
            return self.string
        
    def Filter(self, chars:str="1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM") -> str:
        res = []
        for i in self.string:
            if i in chars:
                res.append(i)
        
        return ''.join(res)
    
    def Len(self) -> int:
        return len(self.string)

    def IsIPAddress(self) -> bool:
        try:
            ipaddress.ip_address(self.string)
            return True 
        except ValueError:
            return False 
    
    def PinYin(self) -> str:
        res = pypinyin.lazy_pinyin(self.string, style=pypinyin.Style.TONE3)
        py = String(('-'.join(res)).replace(" ", "-")).Filter('1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM -').replace('--', '-')
        return py
    
    def RemoveNonUTF8Characters(self) -> str:
        return self.string.encode('utf-8', errors='ignore').decode('utf-8')

    def URLEncode(self) -> str:
        return quote_plus(self.string)
    
    def URLDecode(self) -> str:
        return unquote(self.string)

if __name__ == "__main__":
    print(1, String("ABC").HasChinese())
    print(2, String("ddddd中kkkkkkk").HasChinese())
    print(3, String("\"wef\t测\b试....\n\tffef'").Repr())
    print(4, String("这是一段用鼠标写的简体中文").SimplifiedChineseToTraditional())
    print(5, String("這是一段用鍵盤點擊出來的軌跡").TraditionalChineseToSimplified())
    print(6, String("This is a 用鼠标写的简体中文").SimplifiedChineseToTraditional())
    print(7, String("This is a 用鼠标写的盤點擊出來的軌跡").PinYin())