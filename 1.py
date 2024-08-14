import streamlit as st
from litellm import completion, APIConnectionError
from dotenv import load_dotenv
import os
import json
import time

# .envファイルから環境変数を読み込む
load_dotenv()

# エピソードファイルのパス
EPISODE_FILE = "episode.json"
PROMPT_FILE = "prompt.json"

# エピソードを読み込む関数
def load_episodes():
    if os.path.exists(EPISODE_FILE):
        with open(EPISODE_FILE, "r") as file:
            return json.load(file)
    return {"daughter_episodes": [], "son_in_law_episodes": []}

# エピソードを保存する関数
def save_episodes(episodes):
    with open(EPISODE_FILE, "w") as file:
        json.dump(episodes, file, ensure_ascii=False, indent=4)

# プロンプトを読み込む関数
def load_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r") as file:
            return json.load(file)
    return {"default_prompt": "", "edited_prompt": ""}

# プロンプトを保存する関数
def save_prompt(prompt):
    with open(PROMPT_FILE, "w") as file:
        json.dump(prompt, file, ensure_ascii=False, indent=4)

# エピソードとプロンプトを読み込む
episodes = load_episodes()
prompt_data = load_prompt()

# タイトル
st.title("結婚式の挨拶生成アプリ")

# 挨拶の時間
speech_time = st.slider("挨拶の時間（分）", 1, 10, 5)

# 内容の面白さ
humor = st.slider("内容の面白さ", 1, 10, 5)

# 盛り込むエピソード
episode1 = st.text_input("エピソード1")
episode2 = st.text_input("エピソード2")
episode3 = st.text_input("エピソード3")

# プロンプトの編集
st.subheader("プロンプトの編集")
default_prompt = prompt_data["default_prompt"]
edited_prompt = st.text_area("編集されたプロンプト", value=prompt_data["edited_prompt"] or default_prompt)

if st.button("プロンプトを保存"):
    prompt_data["edited_prompt"] = edited_prompt
    save_prompt(prompt_data)
    st.success("プロンプトが保存されました。")

# 娘のエピソード
st.subheader("娘のエピソード")
new_daughter_episode = st.text_area("新しい娘のエピソード")
if st.button("娘のエピソードを追加"):
    episodes["daughter_episodes"].append(new_daughter_episode)
    save_episodes(episodes)
    st.rerun()

for i, episode in enumerate(episodes["daughter_episodes"]):
    st.text_area(f"娘のエピソード {i+1}", value=episode, key=f"daughter_{i}")
    if st.button(f"削除 娘のエピソード {i+1}", key=f"delete_daughter_{i}"):
        episodes["daughter_episodes"].pop(i)
        save_episodes(episodes)
        st.rerun()

# 婿のエピソード
st.subheader("婿のエピソード")
new_son_in_law_episode = st.text_area("新しい婿のエピソード")
if st.button("婿のエピソードを追加"):
    episodes["son_in_law_episodes"].append(new_son_in_law_episode)
    save_episodes(episodes)
    st.rerun()

for i, episode in enumerate(episodes["son_in_law_episodes"]):
    st.text_area(f"婿のエピソード {i+1}", value=episode, key=f"son_in_law_{i}")
    if st.button(f"削除 婿のエピソード {i+1}", key=f"delete_son_in_law_{i}"):
        episodes["son_in_law_episodes"].pop(i)
        save_episodes(episodes)
        st.rerun()

# 挨拶生成ボタン
if st.button("挨拶を生成"):
    with st.spinner("挨拶を生成中..."):
        api_key = os.getenv("CLAUDE_API_KEY")
        
        if not api_key:
            st.error("Claude APIキーが設定されていません。")
            st.stop()

        # 挨拶のプロンプトを作成
        prompt = edited_prompt if edited_prompt else default_prompt
        prompt = prompt.format(
            speech_time=speech_time,
            humor=humor,
            episode1=episode1,
            episode2=episode2,
            episode3=episode3,
            daughter_episodes=', '.join(episodes['daughter_episodes']),
            son_in_law_episodes=', '.join(episodes['son_in_law_episodes'])
        )
        
        # 挨拶を生成
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = completion(
                    model="claude-3-5-sonnet-20240620",
                    messages=[{"role": "user", "content": prompt}],
                    api_key=api_key
                )
                # 挨拶を表示
                st.success("挨拶が正常に生成されました。")
                st.write(response['choices'][0]['message']['content'])
                break
            except APIConnectionError as e:
                if attempt < max_retries - 1:
                    st.warning(f"API接続エラーが発生しました。再試行中... (試行 {attempt + 1}/{max_retries})")
                    time.sleep(2 ** attempt)  # エクスポネンシャルバックオフ
                else:
                    st.error("API接続エラーが発生しました。後でもう一度お試しください。")
            except Exception as e:
                st.error(f"予期せぬエラーが発生しました: {str(e)}")
                break