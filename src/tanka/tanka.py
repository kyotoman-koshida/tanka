"""Main module."""
from llama_cpp import Llama

class TankaGenerater:
    """ 短歌を作ってくれるクラス """
    
    def __init__(self, model_path, n_gpu_layers=0):
        self.model_path: str = model_path
        """LLMモデルへのパス"""
        self.n_gpu_layers: int = n_gpu_layers
        """オフロードするためのGPUの個数"""

    def generate_tanka(self, scene_text: str) -> str:
        """ 短歌を生成するメソッド
        
        Parameters:
        ----------
        scene_text: str
            短歌に読み込みたい情景

        Return:
        ----------
        str: 生成した短歌一首
        """
        content = f"以下に短歌に読み込みたい情景を提示しますので、それを踏まえて短歌を一首読んでください。情景:{scene_text}"
        prompt= [
            {"role": "system", "content": content}
        ]

        llm = Llama(
            model_path=self.model_path,
            n_gpu_layers=self.n_gpu_layers,
        )

        output = llm(
        f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
        max_tokens=512,
        stop=["<|end|>"],
        echo=True,
        )

        # LLMの出力から、生成した短歌の部分だけを抽出する。
        generated_text = output['choices'][0]['text'].split("<|assistant|>")[-1]

        return generated_text