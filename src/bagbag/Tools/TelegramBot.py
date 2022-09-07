from __future__ import annotations

import telebot # https://github.com/eternnoir/pyTelegramBotAPI

class TelegramBot():
    def __init__(self, token:str):
        self.token = token 
        self.tb = telebot.TeleBot(self.token)
        self.tags:list[str] = []
    
    def GetMe(self) -> telebot.types.User:
        return self.tb.get_me()
    
    def SetChatID(self, chatid:int) -> TelegramBot:
        self.chatid = chatid
        return self
    
    def SendFile(self, path:str):
        self.tb.send_document(self.chatid, open(path, 'rb')) 

    def SendImage(self, path:str):
        self.tb.send_photo(self.chatid, open(path, 'rb'))

    def SendVideo(self, path:str):
        self.tb.send_video(self.chatid, open(path, 'rb')) 

    def SendAudio(self, path:str):
        self.tb.send_audio(self.chatid, open(path, 'rb')) 

    def SendLocation(self, latitude:float, longitude:float):
        self.tb.send_location(self.chatid, latitude, longitude)
    
    def SetTags(self, *tags:str) -> TelegramBot:
        self.tags = tags
        return self 

    def SendMsg(self, msg:str, *tags:str):
        """
        It sends a message to a chat, and if there are tags, it adds them to the end of the message
        
        :param msg: The message to be sent
        :type msg: str
        :param : chatid: the chat id of the chat you want to send the message to
        :type : str
        """
        if len(tags) != 0:
            tag = '\n\n' + ' '.join(['#' + t for t in tags])
        else:
            if len(self.tags) != 0:
                tag = '\n\n' + ' '.join(['#' + t for t in self.tags])
            else:
                tag = ""
        
        if len(msg) <= 4096 - len(tag):
            self.tb.send_message(self.chatid, msg.strip() + tag) 
        else:
            for m in telebot.util.smart_split(msg, 4096 - len(tag)):
                self.tb.send_message(self.chatid, m.strip() + tag) 

if __name__ == "__main__":
    token, chatid = open("TelegramBot.ident").read().strip().split("\n")
    t = TelegramBot(token).SetChatID(int(chatid))
    # t.SendMsg(open("Telegram.py").read(), "tag1", "tag2")
    t.SendMsg("test")
    # t.SendFile("URL.py")