#!/usr/bin/env python

"""Tests for `tanka` package."""

import pytest
from pathlib import Path
from src.tanka.config.config import TankaConfig
from src.tanka import tanka


@pytest.fixture
def tanka_config(monkeypatch):
    """TankaGeneratorのインスタンス化で必要な設定クラスを用意する。"""

    # NOTE:TankaConfigは内部でLLMモデルの格納しているパスを参照しているためファイルのパスを合わせ流。
    test_dir = Path(__file__).parent.parent
    monkeypatch.chdir(test_dir)

    tanka_config = TankaConfig()
    return tanka_config

def test_TankaGenerater_chechtype_1(tanka_config):
    """Phi3を使ってTankaGeneraterで短歌を生成した時に、生成した出力がstr型になっているか確認"""

    tanka_generater = tanka.TankaGenerater(tanka_config)
    scene = "夏より冬の方が好きだ"
    model_name = "Phi-3"
    generated_text = tanka_generater.generate_tanka(scene_text=scene, model_name=model_name)
    assert type(generated_text) == str

def test_TankaGenerater_chechtype_2(tanka_config):
    """ELYZAを使ってTankaGeneraterで短歌を生成した時に、生成した出力がstr型になっているか確認"""

    tanka_generater = tanka.TankaGenerater(tanka_config)
    scene = "夏より冬の方が好きだ"
    model_name = "ELYZA"
    generated_text = tanka_generater.generate_tanka(scene_text=scene, model_name=model_name)
    assert type(generated_text) == str
