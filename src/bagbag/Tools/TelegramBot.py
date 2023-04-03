from __future__ import annotations
from bagbag import Http, Lg, Time, Base64

# 配合这个镜像使用
# 
# version: '3'
# services:
#   telegram_bot:
#     image: darren2046/telegram-bot
#     #ports:
#     #   - "7767:7767" 
#     environment:
#       API_PASS: password_string
#       TELEGRAM_BOT_TOKEN: token_string
    
#     volumes:
#       - /data/cr-volumes/telegram-bot/:/data/

class TelegramBot():
    def __init__(self, apiserver:str, apipass:str) -> None:
        self.server = apiserver.rstrip("/")
        self.password = apipass
        self.chat = None 

        if not self.server.startswith("http"):
            self.server = 'https://' + self.server

    def SetChat(self, chat:str) -> TelegramBot:
        self.chat = chat 
        return self

    def Send(self, message:str, mode:str="text", webPreview:bool=True):
        while True:
            try:
                resp = Http.PostJson(self.server + "/telegram-bot/send/text", {"chat": self.chat, "message": message, "password": self.password, "mode": mode, "webPreview": webPreview})
                if resp.StatusCode != 200:
                    Lg.Warn("发送消息出错:", resp)
                else:
                    return 
            except Exception as e:
                Lg.Warn("发送消息出错:", e)

            Time.Sleep(30, title="等待重试发送消息")
    
    def SendImage(self, path:str):
        while True:
            try:
                resp = Http.PostJson(self.server + "/telegram-bot/send/image", {"chat": self.chat, "image": Base64.Encode(open(path, 'rb').read()), "password": self.password})
                if resp.StatusCode != 200:
                    Lg.Warn("发送消息出错:", resp)
                else:
                    return 
            except Exception as e:
                Lg.Warn("发送消息出错:", e)

            Time.Sleep(30, title="等待重试发送消息")