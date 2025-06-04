import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from user_classification_intro import set_background

def relevant_set_choose_page():
    st.set_page_config(page_title="RankDist Demo", layout="wide")
    set_background("other images/background.webp")

    csv_file_path = "playlists_excel/top_k_songs.csv"
    songs_data = pd.read_csv(csv_file_path)
    persona_name = st.session_state.persona
    persona_number = st.session_state.chosen_person_number
    cluster_file_path = f"alg_results/cluster_{persona_number}.csv"
    if os.path.exists(cluster_file_path):
        cluster_data = pd.read_csv(cluster_file_path)

    st.markdown("""
    <style>
        .block-container {
            padding-top: 30px !important;
            padding-bottom: 30x !important;
            margin: 0px !important;
        }

        .custom-container {
            background: linear-gradient(135deg, rgba(30, 30, 80, 0.97), rgba(50, 50, 110, 0.97));
            padding: 0px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 0px;
            margin-top: 0px;
        }

        .custom-container h3 {
            font-size: 18px;
            margin-top: 15px;
        }

        div[data-testid="stExpander"] {
            min-width: 100% !important;
            background: linear-gradient(135deg, rgba(30, 30, 80, 1), rgba(50, 50, 110, 1));
            color: white !important;
            border-radius: 8px !important;
            margin-bottom: 0px;
            margin-top: 0px;
            padding: 3px !important;
        }

        div[data-testid="stExpander"] div.streamlit-expanderContent {
            color: white !important;
            min-width: 100% !important;
            background: rgba(255, 255, 255, 0.1) !important;
            padding: 3px !important;
            border-radius: 8px !important;
            margin-bottom: 0px;
            margin-top: 0px;
        }

        div[data-testid="stExpander"] summary {
            color: white !important;
            min-width: 100% !important;
            font-size: 14px !important;
            padding: 5px !important;
            margin-bottom: 0px;
            margin-top: 0px;
        }

        .stButton button {
            width: 100%;
            font-size: 18px;
            padding: 8px;
            border-radius: 15px;
            background-color: #800080;
            color: white;
            border: 1px solid black;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-top: 0px;
        }

        .stButton button:hover {
            background-color: #660066;
        }

        .container {
            background: linear-gradient(90deg, #3b5998, #4a69bd); 
            color: white;
            border-radius: 25px;
            padding: 4px;
            margin: auto;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            max-width: 500px;
            font-family: Arial, sans-serif;
            border: 3px solid #a0c4ff;
            margin-bottom: 0px !important;
        }

        .method_name {
            font-size: 16px;
            text-align: left;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            padding-left: 10px;
            color: #ff3333;
            text-shadow:
                -1px -1px 0 #000,
                 1px -1px 0 #000,
                -1px  1px 0 #000,
                 1px  1px 0 #000,
                -2px  0px 0 #000,
                 2px  0px 0 #000,
                 0px -2px 0 #000,
                 0px  2px 0 #000;
            font-weight: bold;
        }

        .text_choose {
            font-size: 23px;
            font-weight: bold;
            padding-top: 0px !important;
            line-height: 1.2;
        }

        .notice-text {
            display: flex;
            justify-content: center;
            background: linear-gradient(135deg, rgba(80, 40, 120, 0.95), rgba(60, 60, 150, 0.95));
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 2px 0;
            border-radius: 50px;
            width: 100%;
            text-align: center;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(f"""
            <div class="container">
                <div class="method_name">
                    Relevant Set
                </div>
                <div class="text_choose">
                    Choose TOP 3 songs you’d recommend to {persona_name} 🎧
                </div>
            </div>
        """, unsafe_allow_html=True)

        if "error_msg" not in st.session_state:
            st.session_state.error_msg = ""

        def handle_confirm_click():
            if len(selected_songs) != 3:
                st.session_state.error_msg = "You must select exactly 3 songs before continuing"
            else:
                st.session_state.page = "relevant_set_compare_recommendations"
                st.session_state.user_choice = selected_songs

        col_next = st.columns([0.15, 0.7, 0.15])
        with col_next[1]:
            selected_songs = st.multiselect("", songs_data["song"].tolist(), max_selections=3)

        col_next = st.columns([1, 1, 1])
        with col_next[1]:
            st.button("Confirm", key="confirm_button", on_click=handle_confirm_click, use_container_width=True)
        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)

        st.markdown("""
            <div style="width: 100%; text-align: center; margin: 25px 0;">
                <div class="notice-text">
                    You can listen to the songs below (Loading the songs may take a few moments) 🎧
                </div>
            </div>
        """, unsafe_allow_html=True)



    cols = st.columns(3, gap="small")

    for idx, row in cluster_data.iterrows():
        song_name = row["relevant_set_songs"]
        track_url = row["relevant_set_songs_links"]

        if "track/" in track_url:
            track_id = track_url.split("track/")[-1].split("?")[0]
            embed_url = f"https://open.spotify.com/embed/track/{track_id}"
        else:
            embed_url = track_url

        with cols[idx % 3]:
            with st.expander(f"🎶 Listen to - {song_name}"):
                embed_html = f"""
                    <iframe style="border-radius:12px" 
                        src="{embed_url}" 
                        width="100%" 
                        height="80" 
                        frameBorder="0" 
                        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                        loading="lazy">
                    </iframe>
                    """
                components.html(embed_html, height=85)

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
