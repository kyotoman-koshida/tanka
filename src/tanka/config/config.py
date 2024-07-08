from pathlib import Path
import json
from typing import Dict

class TankaConfig:
    """設定ファイルの情報をまとめたクラス"""

    model_path: Dict[str, str] = None
    """LLMモデルへのパス
    
    key: LLMモデルの名前
    value: LLMモデルのパス
    """
    prompt: str = None
    """LLMに投げるプロンプト"""
    excuse_message: str = None
    """LLMがうまく短歌を読めなかった時の文章"""

    def __init__(self):
        self.settings_path = Path(__file__).parent.joinpath("settings.jsonc")
        self.post_init()
    
    def post_init(self):
        json_open = open(self.settings_path, 'r')
        settings = json.load(json_open)
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)

class GCPConfig:
    """GCPの情報をまとめたクラス"""
    
    PROJECT_ID: str = None
    """GCPで使っているプロジェクトID"""
    SECRET_ID: str = None
    """秘密鍵の名前"""
    VERSION: str = None
    """秘密鍵のバージョン"""

    def __init__(self):
        self.settings_path = Path(__file__).parent.joinpath("gcp_settings.jsonc")
        self.post_init()

    def post_init(self):
        json_open = open(self.settings_path, 'r')
        settings = json.load(json_open)
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)