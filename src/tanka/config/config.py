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
    # TODO:保守性が悪いため、stop_symbolを変えたら自動で短歌を囲む記号を変える。
    stop_symbol: str = None
    """LLMの出力内で、prompt内の例文や生成した出力文の中で短歌を囲む記号"""
    excuse_message: str = None
    """LLMがうまく短歌を読めなかった時の文章"""
    trial_count: int = 3
    """LLMの出力を試みる試行回数"""

    def __init__(self):
        self.settings_path = Path(__file__).parent.joinpath("settings.jsonc")
        self.post_init()
    
    def post_init(self):
        json_open = open(self.settings_path, 'r')
        settings = json.load(json_open)
        for name, value in settings.items():
            if hasattr(self, name):
                setattr(self, name, value)