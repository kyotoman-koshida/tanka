import re
from google.cloud import secretmanager
from src.tanka.config.config import GCPConfig

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

def get_secret_value_from_GCP() -> str:
    """ Google CloudのSecret Managerで管理しているOpen AIの認証情報を取得する。
    """
    gcp_config = GCPConfig()
    PROJECT_ID, SECRET_ID, VERSION = gcp_config.PROJECT_ID, gcp_config.SECRET_ID, gcp_config.VERSION

    key_path = './src/tanka/config/secret.json'
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(key_path)
    path = client.secret_version_path(PROJECT_ID, SECRET_ID, VERSION)
    response = client.access_secret_version(name=path)
    secret_value = response.payload.data.decode('UTF-8')

    return secret_value