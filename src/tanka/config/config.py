from pathlib import Path
import json

class TankaConfig:
    """設定ファイルの情報をまとめたクラス"""

    model_path: str = None
    """LLMモデルへのパス"""
    prompt: str = None
    """LLMに投げるプロンプト"""

    def __init__(self):
        self.settings_path = Path(__file__).parent.joinpath("settings.jsonc")
        self.post_init()
    
    def post_init(self):
        json_open = open(self.settings_path, 'r')
        settings = json.load(json_open)
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)