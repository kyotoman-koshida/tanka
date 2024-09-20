import MeCab
import ipadic
import re

def count_mora(text: str) -> int:
    """ 与えられたテキストのモーラ数をカウントする。

    Parameters:
    ----------
    text: str
        与えられたテキスト(想定では短歌のテキストが渡される)

    Return:
    ----------
    mora_count: モーラ数
    """
    # MeCabのTaggerの初期化
    CHASEN_ARGS = r' -F "%m\t%f[7]\t%f[6]\t%F-[0,1,2,3]\t%f[4]\t%f[5]\n"'
    CHASEN_ARGS += r' -U "%m\t%m\t%m\t%F-[0,1,2,3]\t\t\n"'
    tagger = MeCab.Tagger(ipadic.MECAB_ARGS + CHASEN_ARGS)

    # 形態素解析の実行
    node = tagger.parseToNode(text)

    # モーラ数をカウントするための変数
    mora_count = 0

    while node:
        # ノードの品詞情報を取得
        features = node.feature.split(",")

        if features[0] == "BOS/EOS":
          # 次のノードへ移動
          node = node.next
          continue

        # ノードが読みを持っている場合
        if len(features) > 7:
            # 読みを取得
            reading = features[7]

            # 読みの長さをモーラ数として加算
            mora_count += len(reading)

        # 次のノードへ移動
        node = node.next

    return mora_count

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