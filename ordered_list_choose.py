import streamlit as st
import pandas as pd
import os
from other_functions import set_background
from other_functions import render_progress_bar
from other_functions import render_song


def ordered_list_choose_page():
    st.set_page_config(page_title="RankDist Demo")
    render_progress_bar("recommend songs")
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
            padding-top: 5px !important;
            margin-top: 5px !important;
        }

        .custom-container {
            background: linear-gradient(135deg, rgba(30, 30, 80, 0.97), rgba(50, 50, 110, 0.97));
            padding: 0px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 0px;
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
            margin-top: -20px; !important;
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
            font-size: 20px;
            font-weight: bold;
            padding-top: 0px !important;
            line-height: 1.15;
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
                    Ordered List
                </div>
                <div class="text_choose">
                    Choose the TOP 3 songs you'd recommend to {persona_name} in order
                </div>
            </div>
        """, unsafe_allow_html=True)

        if "error_msg" not in st.session_state:
            st.session_state.error_msg = ""

        def handle_confirm_click():
            selections = [place_1, place_2, place_3]
            placeholders = [placeholder1, placeholder2, placeholder3]
            if any(s in placeholders for s in selections):
                st.session_state.error_msg = "Please select a song for each place"
            elif len(set(selections)) < 3:
                st.session_state.error_msg = "A song was selected for more than one place"
            else:
                st.session_state.user_choice = selections
                st.session_state.page = "ordered_list_compare_recommendations"

        st.markdown("""
            <style>
                div[data-testid="stSelectbox"] {
                    margin-bottom: 5px !important;
                }
            </style>
        """, unsafe_allow_html=True)
        col_next = st.columns([0.15, 0.7, 0.15])
        with col_next[1]:
            songs = songs_data["song"].tolist()
            placeholder1 = "Select the song for first place 🥇"
            placeholder2 = "Select the song for second place 🥈"
            placeholder3 = "Select the song for third place 🥉"

            place_1 = st.selectbox("", [placeholder1] + songs, key="place_1", label_visibility="collapsed")
            place_2 = st.selectbox("", [placeholder2] + songs, key="place_2", label_visibility="collapsed")
            place_3 = st.selectbox("", [placeholder3] + songs, key="place_3", label_visibility="collapsed")
            st.button("Confirm", key="confirm_button", on_click=handle_confirm_click, use_container_width=True)

            if st.session_state.error_msg:
                st.error(st.session_state.error_msg)

        st.markdown("""
            <div style="width: 100%; text-align: center; margin-top: 0px; margin-bottom: 25px;">
                <div class="notice-text">
                    You can listen to the songs below💿
                </div>
            </div>
        """, unsafe_allow_html=True)


        cols = st.columns(3, gap="small")
        for idx, row in cluster_data.iterrows():
            song_name = row["perfect_precision_songs"]
            track_url = row["perfect_precision_songs_links"]

            if "track/" in track_url:
                track_id = track_url.split("track/")[-1].split("?")[0]
                embed_url = f"https://open.spotify.com/embed/track/{track_id}"
            else:
                embed_url = track_url

            with cols[idx % 3]:
                with st.expander(f"🎶 Listen to - {song_name}"):
                    render_song(embed_url, idx)

        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
