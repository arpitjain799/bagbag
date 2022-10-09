from re import I
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import telethon
from telethon import utils
from telethon import types
import time

try:
    from .. import Os
    from .Database import SQLite
except:
    import sys 
    sys.path.append("..")
    import Os
    from Database import SQLite

class TelegramGeo():
    def __init__(self):
        self.Long = None
        self.Lat = None 
        self.AccessHash = None
    
    def __repr__(self):
        return f"TelegramGeo(Long={self.Long}, Lat={self.Lat}, AccessHash={self.AccessHash})"
        
    def __str__(self):
        return f"TelegramGeo(Long={self.Long}, Lat={self.Lat}, AccessHash={self.AccessHash})"
        
class TelegramPhoto():
    def __init__(self):
        self.ID = None
        self.AccessHash = 0
    
    def __repr__(self):
        return f"TelegramPhoto(ID={self.ID}, AccessHash={self.AccessHash})"
        
    def __str__(self):
        return f"TelegramPhoto(ID={self.ID}, AccessHash={self.AccessHash})"
        
# File and Audio
class TelegramFile():
    def __init__(self):
        self.Name = ""
        self.Size = 0
        self.ID = None 
        self.AccessHash = 0
    
    def __repr__(self):
        return f"TelegramFile(Name={self.Name}, Size={self.Size}, ID={self.ID}, AccessHash={self.AccessHash})"
        
    def __str__(self):
        return f"TelegramFile(Name={self.Name}, Size={self.Size}, ID={self.ID}, AccessHash={self.AccessHash})"
        
class TelegramMessage():
    def __init__(self, client:TelegramClient):
        self.client = client
        self.message = None
        self.PeerType:str = None 
        self.Chat = TelegramPeer(client=self.client)
        self.ID:int = None 
        self.Time:int = None 
        self.Action:str = None 
        self.File:TelegramFile = None
        self.Photo:TelegramPhoto = None
        self.Geo:TelegramGeo = None
        self.Message:str = None
        self.User:TelegramPeer = None
    
    def DownloadMedia(self, SavePath:str=None) -> str | None:
        if not SavePath:
            if self.File:
                SavePath = self.File.Name
            elif self.Photo:
                SavePath = "photo.jpg"
        
        SavePath = Os.Path.Uniquify(SavePath)

        if not Os.Path.Exists(Os.Path.Basedir(SavePath)):
            Os.Mkdir(Os.Path.Basedir(SavePath))

        self.client.download_media(self.message)
    
    def __repr__(self):
        return f"TelegramMessage(PeerType={self.PeerType}, Chat={self.Chat}, ID={self.ID}, Time={self.Time}, Action={self.Action}, File={self.File}, Photo={self.Photo}, Message={self.Message}, User={self.User})"
        
    def __str__(self):
        return f"TelegramMessage(PeerType={self.PeerType}, Chat={self.Chat}, ID={self.ID}, Time={self.Time}, Action={self.Action}, File={self.File}, Photo={self.Photo}, Message={self.Message}, User={self.User})"
        
class TelegramPeer():
    def __init__(self, Type:str=None, Name:str=None, Username:str=None, ID:int=None, AccessHash:int=None, PhoneNumber:int=None, LangCode:str=None, client:TelegramClient=None):
        """
        :param Type: The type of the entity. Can be either "user" or "channel" (group)
        :type Type: str
        :param Name: The name of the user or channel
        :type Name: str
        :param Username: The username of the user or channel
        :type Username: str
        :param ID: The ID of the user or chat
        :type ID: int
        :param AccessHash: This is a unique identifier for a user or group. It is used to identify a user
        or group in a secure way
        :type AccessHash: int
        :param PhoneNumber: The phone number of the user
        :type PhoneNumber: int
        :param LangCode: The language code of the user
        :type LangCode: str
        """
        self.Type = Type # channel(group), user
        self.Name = Name # 名字, First Name + Last Name 或者 Title 
        self.Username = Username 
        self.ID = ID
        self.AccessHash = AccessHash
        self.PhoneNumber = PhoneNumber 
        self.LangCode = LangCode 
        self.Resolved = False # 是否已解析. 只设置一个ID, 解析之后就补上其它的字段.
        self.client = client # telethon.sync.TelegramClient
    
    def Message(self, id:str) -> TelegramMessage:
        message = self.client.get_messages(self.ID, ids=id)
        return self.__wrapMsg(message)
    
    def __wrapMsg(self, message) -> TelegramMessage:
        msg = TelegramMessage(self.client)
        msg.message = message
        msg.PeerType = self.Type 
        msg.Chat = self 
        msg.ID = message.id 
        msg.Time = int(message.date.timestamp())
        if message.action:
            msg.Action = message.action.to_dict()["_"]
        if message.media:
            if message.document:
                msg.File = TelegramFile()
                msg.File.ID = message.document.id 
                msg.File.AccessHash = message.document.access_hash
                msg.File.Size = message.document.size 
                for attr in message.media.document.attributes:
                    if attr.to_dict()['_'] == "DocumentAttributeFilename":
                        msg.File.Name = attr.to_dict()['file_name']
            elif message.photo:
                msg.Photo = TelegramPhoto()
                msg.Photo.ID = message.photo.id
                msg.Photo.AccessHash = message.photo.access_hash
            elif message.geo:
                msg.Geo = TelegramGeo()
                msg.Geo.AccessHash = message.geo.access_hash
                msg.Geo.Lat = message.geo.lat 
                msg.Geo.Long = message.geo.long
            # else: 
            #     import ipdb 
            #     ipdb.set_trace()
            #     print(message)
        if message.message:
            msg.Message = message.message
        if message.from_id:
            msg.User = TelegramPeer(ID=message.from_id.user_id, client=self.client)

        return msg
    
    def Messages(self, limit:int=100, offset:int=0) -> list[TelegramMessage]:
        """
        It takes a chat object, and returns a list of messages in that chat.
        
        :param limit: The maximum number of messages to be returned, defaults to 100
        :type limit: int (optional)
        :param offset: The offset of the first message to be returned, defaults to 0
        :type offset: int (optional)
        :return: A list of TelegramMessage objects
        """
        res = []
        getmessage = self.client.get_messages(self.ID, limit=limit, offset_id=offset)
        for message in getmessage:
            msg = self.__wrapMsg(message)
            res.append(msg)
        return res

    def Resolve(self):
        """
        Resolve Peer, get information by peer id. 
        """
        if self.ID:
            obj = self.client.get_entity(self.ID)
            # import ipdb
            # ipdb.set_trace()
            if type(obj) == telethon.tl.types.Channel:
                self.Type = "channel"
                self.Name = obj.title
            elif type(obj) == telethon.tl.types.User:
                self.Type = "user"
                self.Name = " ".join([i for i in filter(lambda x: x != None, [obj.first_name, obj.last_name])])
            
            self.AccessHash = obj.access_hash
            self.Username = obj.username 
            self.ID = obj.id

    def __repr__(self):
        return f"TelegramPeer(Type={self.Type}, Name={self.Name}, Username={self.Username}, ID={self.ID}, AccessHash={self.AccessHash})"

    def __str__(self):
        return f"TelegramPeer(Type={self.Type}, Name={self.Name}, Username={self.Username}, ID={self.ID}, AccessHash={self.AccessHash})"

# It's a wrapper for the `telethon` library that allows you to use it in a more Pythonic way
class Telegram():
    def __init__(self, appid:str, apphash:str, sessionfile:str):
        self.client = TelegramClient(sessionfile, appid, apphash, device_model="Samsung S22 Ultra", system_version="Android 10.0.0", app_version="4.0.2") 
        # self.client = TelegramClient(StringSession(sessionString), appid, apphash)
        self.client.start()

        # me = self.client.get_me()
        # print(me.stringify())
        self.sessionfile = sessionfile + ".session"

    def SessionString(self) -> str:
        """
        It takes the session object from the client object and saves it to a string
        :return: The session string is being returned.
        """
        return self.client.session.save()
    
    def PeerByUsername(self, username:str) -> TelegramPeer:
        """
        根据Username解析一个Peer, 有速率限制
        
        :param username: The username of the user/channel you want to send the message to
        :type username: str
        """
        tp = TelegramPeer()

        tp.client = self.client

        try:
            obj = self.client.get_entity(username)
        except (ValueError, TypeError):
            time.sleep(1)
            obj = self.client.get_entity(username)
        if type(obj) == telethon.tl.types.Channel:
            tp.Type = "channel"
            tp.Name = obj.title
        elif type(obj) == telethon.tl.types.User:
            tp.Type = "user"
            tp.Name = " ".join(filter(lambda x: x != None, [obj.first_name, obj.last_name]))
        
        tp.AccessHash = obj.access_hash
        tp.Username = obj.username 
        tp.ID = obj.id

        self.client.session.save()

        return tp
    
    def PeerByIDAndHash(self, ID:int, Hash:int, Type:str="channel") -> TelegramPeer:
        """
        根据ID和Hash返回一个Peer
        
        :param ID: The ID of the user or group
        :type ID: int
        :param Hash: The hash value of the peer, which can be obtained by calling the GetPeerHash method
        of the TelegramPeer object
        :type Hash: int
        :param Type: The type of the peer, which can be "channel", "group", or "user", defaults to
        channel
        :type Type: str (optional)
        :return: TelegramPeer
        """
        if Type in ["channel", "group"]:
            tp = types.PeerChannel(ID)
        elif Type == "user":
            tp = types.PeerUser(ID)
        else:
            raise Exception(f"未知的类型:{Type}")
        peerid = utils.get_peer_id(tp)

        try:
            return self.PeerByUsername(peerid)
        except (ValueError, TypeError):
            self.client.session.save() # save all data to sqlite database session file to avlide database lock
            db = SQLite(self.sessionfile)
            (db.Table("entities").
                Data({
                    "id": peerid, 
                    "hash": Hash,
                }).Insert())
            db.Close()
            try:
                peer = self.PeerByUsername(peerid)
            except (ValueError, TypeError):
                time.sleep(1)
                peer = self.PeerByUsername(peerid)
            self.client.session.save() # save the entity we just resolved to the database

            return peer 

if __name__ == "__main__":
    import json 
    ident = json.loads(open("Telegram.ident").read())
    app_id = ident["appid"]
    app_hash = ident["apphash"]
    
    tg = Telegram(app_id, app_hash, "telegram-session")
    peer = tg.PeerByUsername(ident["username"])
    # peer = tg.PeerByIDAndHash(1234567678, -234567678678)
    print(peer)

    import ipdb
    ipdb.set_trace()

    for i in peer.History():
        if i.User:
            i.User.Resolve()
        print(i)



