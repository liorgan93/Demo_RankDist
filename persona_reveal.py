import streamlit as st
import pandas as pd
import ast
from other_functions import set_background
from other_functions import render_progress_bar
from classsification_functions import classify_user_by_preferences
import base64

def button_click():
    st.session_state.page = "know_the_persona_intro"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def persona_reveal_page():
    st.set_page_config(page_title="RankDist Demo")
    render_progress_bar("meet the persona")
    set_background("other images/background.webp")

    st.session_state.songs_df['like/dislike'] = st.session_state.song_feedback
    st.session_state.songs_df['weights'] = st.session_state.songs_df['weights'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    st.session_state.chosen_person_number, scores = classify_user_by_preferences(st.session_state.songs_df)

    if "persona" not in st.session_state:
        names = pd.read_csv("playlists_excel/names.csv")
        names_list = names[names["cluster"] == st.session_state.chosen_person_number]["name"].tolist()
        st.session_state.persona = ", ".join(names_list)
        gender_value = names[names["cluster"] == st.session_state.chosen_person_number]["her/him"].iloc[0]
        st.session_state.gender_pronoun = gender_value

    st.markdown("""
        <style>
        .container {
            background-color: #ffffff;
            border-radius: 30px;
            padding: 0.3px;
            text-align: center;
            font-family: Arial, sans-serif;
            width: 80%;
            margin: auto;
            margin-top: -20px;
        }
        .title {
            font-size: 26px;
            font-weight: 900;
            background: linear-gradient(to bottom, #000000, #222222, #444444); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3), 4px 4px 10px rgba(0, 0, 0, 0.2); 
        }
        .sub_title {
            font-size: 15px;
            color: black;
            font-weight: bold;
            margin-bottom: 15px;
            letter-spacing: 1px;
            line-height: 1.2;
        }
        .header-small {
            font-size: 17px;      
            font-weight: 700;
            color: #FFFFFF;
            background: linear-gradient(90deg,
  #1f3ba6 0%,
  #2847b3 40%,
  #3053bf 75%,
  #3a5fcb 100%);



            padding: 15px 12px;     
            border-radius: 15px;
            margin: 0 auto 17px;
            text-align: center;     
            width: 80%;
            display: block;
            line-height: 1.2;
        }
        .persona-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 0px;
        }
        .persona-img {
            border-radius: 15px;
            max-height: 30vh;
            width: 60%;
            max-width: 80%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 0px;
        }
        .stButton button {
            width: 100%;
            font-size: 18px;
            padding: 15px;
            border-radius: 15px;
            background-color: #800080;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-top: 0;
        }
        .stButton button:hover {
            background-color: #660066;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="container">
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                <span style="font-size: 21px; transform: scaleX(-1);">🎉</span>
                <div class="title">Meet {st.session_state.persona}</div>
                <span style="font-size: 21px;">🎉</span>
            </div>
            <div class="sub_title">Based on your musical taste you share the same vibe!</div>
        </div>
    """, unsafe_allow_html=True)

    try:
        image_path = f"personas_images/{st.session_state.persona}.jpg"
        image_base64 = get_base64_image(image_path)

        col1, col2, col3 = st.columns([0.14, 0.7, 0.15])
        with col2:
            st.markdown(f"""
                <div class="persona-box">
                    <img class="persona-img" src="data:image/jpg;base64,{image_base64}" />
                    <div class="header-small">soon You’ll recommend songs for {st.session_state.persona}!</div>
                </div>
            """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"Could not load the image for {st.session_state.persona}. Please check the file path.")

    col_next = st.columns([1, 1, 1])
    with col_next[1]:
        st.button("Next", key="songs_persona_like", on_click=button_click, use_container_width=True)
