"""Main module."""
import os
from google.cloud import secretmanager
from llama_cpp import Llama
from openai import OpenAI

from src.tanka.config.config import TankaConfig, GCPConfig
from utils.utils import extract_text_between_symbols

class TankaGenerater:
    """ 短歌を作ってくれるクラス """
    
    def __init__(self, config: TankaConfig = None, n_gpu_layers: int = 0):
        self.config = config
        """短歌の設定クラスのインスタンス"""
        self.n_gpu_layers: int = n_gpu_layers
        """オフロードするためのGPUの個数"""

    def generate_tanka(self, scene_text: str, model_name) -> str:
        """ 短歌を生成するメソッド
        
        Parameters:
        ----------
        scene_text: str
            短歌に読み込みたい情景

        Return:
        ----------
        str: 生成した短歌一首
        """
        # LLMに渡すことになるプロンプトを作成する。
        content = self.config.prompt+f"情景:{scene_text}"

        if os.path.isfile(self.config.model_path[model_name]):
            generated_text = self._use_llama_cpp(content=content, model_name=model_name)
        else:
            # 指定したLLMモデルが存在しない時、
            # またはChatGPTを使うことを希望する時。
            generated_text = self._use_openai_api(content=content)

        return generated_text
    
    def _use_openai_api(self, content: str) -> str:
        """OpenAIのAPIからChatGPTを呼び出して短歌を詠ませる。
        
        Parameters:
        ----------
        content: str
            LLMに渡すプロンプト
        """
        # Google CloudのSecret Managerで管理しているOpen AIの認証情報を取得する。
        gcp_config = GCPConfig()
        PROJECT_ID, SECRET_ID, VERSION = gcp_config.PROJECT_ID, gcp_config.SECRET_ID, gcp_config.VERSION

        key_path = './src/tanka/config/secret.json'
        client = secretmanager.SecretManagerServiceClient.from_service_account_json(key_path)
        path = client.secret_version_path(PROJECT_ID, SECRET_ID, VERSION)
        response = client.access_secret_version(name=path)
        secret_value = response.payload.data.decode('UTF-8')

        # ChatGPTのAPIから回答を得る。
        client = OpenAI(api_key=secret_value.split("=")[1])
        stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                generated_text = chunk.choices[0].delta.content
            else:
                generated_text = self.config.excuse_message

        return generated_text

    def _use_llama_cpp(self, content: str, model_name: str) -> str:
        """llama_cppを使って、用意しているLLMモデルをCPUでも動かせるようにして短歌を詠ませる。
        
        Parameters:
        ----------
        prompt: str
            LLMに渡すプロンプト
        model_name: str
            使いたいLLMの名前
        """
        prompt= [
            {"role": "system", "content": content}
        ]

        llm = Llama(
            model_path=self.config.model_path[model_name],
            n_gpu_layers=self.n_gpu_layers,
        )

        while True:
            # 指定した形式の出力が出るまでは試行を繰り返す。

            output = llm(
            f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
            max_tokens=512,
            stop=["<|end|>"],
            echo=True,
            )

            # LLMの出力から、生成した短歌の部分だけを抽出する。
            generated_text = output['choices'][0]['text'].split("<|assistant|>")[-1]
            if generated_text.count(self.config.stop_symbol) < 2:
                # generated_textの中に、短歌を囲むstop_symbolが2つない場合
                continue

            generated_text = extract_text_between_symbols(generated_text, self.config.stop_symbol)
            return generated_text

    