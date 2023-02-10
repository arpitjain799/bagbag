import tweepy
import typing 

class twitterUser():
    def __init__(self) -> None:
        self.ID:int = None 
        self.Name:str = None 
        self.ScreenName:str = None 
        self.Location:str = None 
        self.RegisterTime:int = None 
        self.Description:str = None 
        self.URL:str = None
        
    def __repr__(self) -> str:
        return f"twitterUser(ID={self.ID} Name={self.Name} ScreenName={self.ScreenName} Location={self.Location} RegisterTime={self.RegisterTime} URL={self.URL} Description={self.Description})"

    def __str__(self) -> str:
        return f"twitterUser(ID={self.ID} Name={self.Name} ScreenName={self.ScreenName} Location={self.Location} RegisterTime={self.RegisterTime} URL={self.URL} Description={self.Description})"

class twitterTweet():
    def __init__(self) -> None:
        self.ID:int = None
        self.User:twitterUser = None 
        self.Time:int = None 
        self.Text:str = None 
        self.Language:str = None 
    
    def __repr__(self) -> str:
        return f"twitterTweet(ID={self.ID} Time={self.Time} Language={self.Language} Text={self.Text} User={self.User})"
    
    def __str__(self) -> str:
        return f"twitterTweet(ID={self.ID} Time={self.Time} Language={self.Language} Text={self.Text} User={self.User})"

class Elevated():
    def __init__(self, consumer_key:str, consumer_secret:str) -> None:
        auth = tweepy.OAuth2AppHandler(consumer_key, consumer_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True)
    
    def _wrapUser(self, author) -> twitterUser:
        u = twitterUser()
        u.ID = author.id
        u.Name = author.name
        u.ScreenName = author.screen_name
        u.Location = author.location
        u.Description = author.description
        u.URL = author.url
        u.RegisterTime = int(author.created_at.timestamp())

        return u
    
    def _wrapStatus(self, status) -> twitterTweet:
        u = self._wrapUser(status.author)

        t = twitterTweet()
        t.User = u 

        t.ID = status.id # https://twitter.com/saepudin1991/status/1613434061741260803
        t.Time = int(status.created_at.timestamp())

        if hasattr(status, 'retweeted_status'):
            # 由于如果是转推, 那么status.full_text会被截断到140个字符, 而完整的推文在status.retweeted_status.full_text
            # 所以拼接一下
            sidx = 0
            foundsidx = False 
            while True:
                if sidx > 140 or status.full_text[sidx:-1] == "":
                    break 

                if status.full_text[sidx:-1] in status.retweeted_status.full_text:
                    foundsidx = True 
                    break 

                sidx += 1
            if foundsidx:
                text = status.full_text[:sidx] + status.retweeted_status.full_text
            else:
                text = status.full_text
        # 如果不是转推
        else:
            text = status.full_text
        t.Text = text

        t.Language = status.lang

        return t
    
    def Search(self, keyword:str, excludeRetweet:bool=True, days:int=7, countPerRequest:int=40, sinceID:int=None) -> typing.Iterable[twitterTweet]:
        """
        It takes a keyword, and returns an iterator of tweets that contain that keyword. 
        tweet的ID是从大到小, 也就是数据的时间是从近到远
        
        :param keyword: The keyword to search for
        :type keyword: str
        :param days: How many days back to search, defaults to 7
        :type days: int (optional)
        :param countPerRequest: The number of tweets to return per request. The maximum is 100, defaults
        to 40
        :type countPerRequest: int (optional)
        :param sinceID: The ID of the tweet to start from. If you want to start from the beginning, set
        this to None
        :type sinceID: int
        """
        if excludeRetweet:
            keyword = keyword + " -filter:retweets"
            
        for status in tweepy.Cursor(self.api.search_tweets, q=keyword, tweet_mode='extended', count=countPerRequest, since_id=sinceID).items():
            yield self._wrapStatus(status)
    
    def Timeline(self, screename:str, countPerRequest:int=40, sinceID:int=None) -> typing.Iterable[twitterTweet]:
        """
        tweet from the timeline of the user with the given screen name
        tweet的ID是从大到小, 也就是数据的时间是从近到远
        
        :param screename: The screen name of the user
        :type screename: str
        :param countPerRequest: The number of tweets to return per request. The maximum is 200, defaults
        to 40
        :type countPerRequest: int (optional)
        :param sinceID: If you want to get tweets since a certain ID, you can use this
        :type sinceID: int
        """
        for status in tweepy.Cursor(self.api.user_timeline, screen_name=screename, tweet_mode='extended', count=countPerRequest, since_id=sinceID).items():
            yield self._wrapStatus(status)
    
    def Followers(self, screename:str, countPerRequest:int=40) -> typing.Iterable[twitterUser]:
        for user in tweepy.Cursor(self.api.get_followers, screen_name=screename, count=countPerRequest).items():
            yield self._wrapUser(user)

if __name__ == "__main__":
    import json 

    cfg = json.loads(open('twitter.ident').read())

    twitter = Elevated(cfg['consumer_key'], cfg['consumer_secret'])
    
    print("search")
    for i in twitter.Search("coinsbee"):
        print(i)
        break 

    print('timeline')
    for i in twitter.Timeline("asiwaju_wa"):
        print(i)
        break 
    
    print("followers")
    for i in twitter.Followers("asiwaju_wa"):
        print(i)
        break 

    