import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# タイトル
st.title("結婚式の挨拶生成アプリ")

# モデル選択
model = st.selectbox("モデルを選択してください", ["claude-3-5-sonnet-20240620", "gemini-1.5-pro-latest", "gpt-4o-2024-08-06"])

# 挨拶の時間
time = st.slider("挨拶の時間（分）", 1, 10, 5)

# 内容の面白さ
humor = st.slider("内容の面白さ", 1, 10, 5)

# 盛り込むエピソード
episode1 = st.text_input("エピソード1")
episode2 = st.text_input("エピソード2")
episode3 = st.text_input("エピソード3")


# 挨拶生成ボタン
if st.button("挨拶を生成"):
    # モデルに応じたAPIキーを取得
    if model == "claude-3-5-sonnet-20240620":
        api_key = os.getenv("ANTHROPIC_API_KEY")
    elif model == "gemini-1.5-pro-latest":
        api_key = os.getenv("GEMINI_API_KEY")
    elif model == "gpt-4o-2024-08-06":
        api_key = os.getenv("OPENAI_API_KEY")
    
    # 挨拶のプロンプトを作成
    prompt = f"""
    結婚する娘の父親として、以下の条件で挨拶を作成してください。父親は千葉県旭市の大きな会社鈴木安太郎商店の社長です。父親は豪快な性格で破天荒な人です。娘の名前は萌でパリピです。友達も多く、おしゃべりが大好きです。娘婿は兵庫県出身で名前は政樹で、関西学院大学出身の優秀な男です。将来は二人で会社を支えていくことを目指しています。

    - 挨拶の時間: {time}分
    - 内容の面白さ: {humor}
    - 盛り込むエピソード: {episode1}, {episode2}, {episode3}
    """
    
    # 挨拶を生成
    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_key=api_key
    )
    
    # 挨拶を表示
    st.write(response['choices'][0]['message']['content'])