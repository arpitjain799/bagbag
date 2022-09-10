import jieba 

def CutChinese(chinese:str) -> list[str]:
    return jieba.cut(chinese, cut_all=False)

