import re

def extract_text_between_symbols(text: str, symbol:str) -> str:
    """ textの中の、指定されたsymbolで囲まれた文章を抜き出す。

    Parameters:
    ----------
    text: str
        抽出元の文章
    symbol: str
        抽出したい文章を囲むシンボル

    Return:
    ----------
    str: 抽出した文章
    """
    pattern = re.escape(symbol) + '(.*?)' + re.escape(symbol)
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0]