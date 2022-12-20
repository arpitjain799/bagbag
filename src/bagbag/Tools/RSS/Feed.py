import feedparser
import markdownify

class RSSPage():
    def __init__(self):
        self.Title:str = ""
        self.URL:str = "" 
        self.Description:str = "" 
        self.Content:str = "" 
    
    def __str__(self) -> str:
        content = str(repr(self.Content).encode("ASCII", "backslashreplace"), "ASCII")[1:-1]
        if len(content) > 80:
            content = content[:80] + "..."
        return f"RSSPage(Title={self.Title} URL={self.URL} Description={self.Description} Content={content})"

def Feed(feedurl:str) -> list[RSSPage]:
    feed = dict(feedparser.parse(feedurl))

    res = []
    for f in feed['entries']:
        r = RSSPage()
        r.Title = f['title']
        r.URL = f['link']
        if 'summary_detail' in f:
            if 'type' in f['summary_detail']:
                if f['summary_detail']['type'] == 'text/html':
                    if 'value' in f['summary_detail']:
                        r.Description = markdownify.markdownify(f['summary_detail']['value'])
                else:
                    if 'value' in f['summary_detail']:
                        r.Description = f['summary_detail']['value']
            else:
                if 'value' in f['summary_detail']:
                    r.Description = f['summary_detail']['value']
        
        if 'content' in f:
            if len(f['content']) > 0:
                c = f['content'][0]
                if 'type' in c:
                    if c['type'] == 'text/html':
                        if 'value' in c:
                            r.Content = markdownify.markdownify(c['value'])
                    else:
                        if 'value' in c:
                            r.Content = c['value']
                else:
                    if 'value' in c:
                        r.Content = c['value']
        res.append(r)
    
    return res

if __name__ == "__main__":
    for i in Feed("https://wilper.wordpress.com/feed/"):
        print(str(i))