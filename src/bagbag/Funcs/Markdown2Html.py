import markdown 

def Markdown2Html(text:str) -> str:
    return markdown.markdown(text)