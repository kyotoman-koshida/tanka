import streamlit as st
from src.tanka.tanka import TankaGenerater
from src.tanka.config.config import TankaConfig

st.title("短歌ゴーストライター")
st.write("")
st.write("""
    このアプリは思い浮かんだ情景を入力することで、それを元にして短歌を詠んでくれるアプリです。
""")
st.write("")

tanka_config = TankaConfig()
LLMs = tanka_config.model_path

model_name = st.selectbox(
    label='詠み手を選んでください。',
    options=LLMs.keys()
)
st.write('選択した詠み手:', model_name)

#メインフォームの設定
with st.form(key = "Letter Form", clear_on_submit = False):
    st.title("情景 入力欄")
    body = st.empty()
    if ("letter_body" in st.session_state.keys()): 
        ret = body.text_area(
            label = "短歌に詠み込みたい情景を入力してください。",
            value = st.session_state["letter_body"]
        )
    else:
        ret = body.text_area(
            label = "短歌に詠み込みたい情景を入力してください。",
            value = ""
        )
    sub = st.form_submit_button("一首詠む")

# TODO: 一首詠んだ後のボタンを、「もう一度詠む」ボタンに変更させる

if sub:
    tanka_generater = TankaGenerater(tanka_config)
    #LLMによる推論を実行。
    with st.spinner(text = "作歌アンド推敲中..."):
        text  = tanka_generater.generate_tanka(scene_text=ret, model_name=model_name)
        st.session_state["letter_body"] = text
        st.experimental_rerun()