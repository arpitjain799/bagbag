import re
import langid
import opencc
import ipaddress

class String():
    def __init__(self, string:str):
        self.string = string 
    
        """
        > If there are any Chinese characters in the string, return `True`. Otherwise, return `False`
        :return: A boolean value.
        """
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

if __name__ == "__main__":
    print(1, String("ABC").HasChinese())
    print(2, String("ddddd中kkkkkkk").HasChinese())
    print(3, String("\"wef\t测\b试....\n\tffef'").Repr())
    print(4, String("这是一段用鼠标写的简体中文").SimplifiedChineseToTraditional())
