import re

class String():
    def __init__(self, string:str):
        self.string = string 
    
        """
        > If there are any Chinese characters in the string, return `True`. Otherwise, return `False`
        :return: A boolean value.
        """
    def HasChinese(self) -> bool:
        return len(re.findall(r'[\u4e00-\u9fff]+', self.string)) != 0

if __name__ == "__main__":
    print(1, String("ABC").HasChinese())
    print(2, String("ddddd中kkkkkkk").HasChinese())



