import streamlit as st
import pandas as pd
import ast
from collections import Counter
from classsification_functions import sample_unique_tracks_per_cluster
from other_functions import set_background
from other_functions import render_progress_bar

def button_click_problem():
    st.session_state.page = "user_classification_intro"
    del st.session_state.song_feedback
    del st.session_state.current_song_index

def user_classification_page():
    st.set_page_config(page_title="RankDist Demo")
    if not st.session_state.problem:
        render_progress_bar("taste match")
    set_background("other images/background.webp")
    all_songs_df = pd.read_csv('playlists_excel/songs_for_classification.csv')
    max_attempts = 150
    sample_size = 10
    n_clusters = 5
    sample = None

    if "song_feedback" not in st.session_state:
        st.session_state.song_feedback = []
    if "current_song_index" not in st.session_state:
        st.session_state.current_song_index = 0
        for y in range(max_attempts):
            sampled_df = sample_unique_tracks_per_cluster(all_songs_df)
            sample = sampled_df.sample(n=sample_size).reset_index(drop=True)

            cluster_counts = Counter()
            for row in sample['clusters_for_track']:
                if isinstance(row, str):
                    row = ast.literal_eval(row)
                cluster_counts.update(row)

            unique_artists = sample['artist'].nunique() == len(sample)
            valid_clusters = all(2 <= cluster_counts.get(cluster, 0) < 4 for cluster in range(n_clusters))

            if valid_clusters and unique_artists:
                st.session_state.songs_df = sample
                break
    if "songs_df" not in st.session_state:
        st.session_state.songs_df = sample
    current_index = st.session_state.current_song_index

    if current_index < len(st.session_state.songs_df):
        st.session_state.button_clicked = False
        song_title = st.session_state.songs_df.loc[current_index, 'name']
        song_artist = st.session_state.songs_df.loc[current_index, 'artist']

        st.markdown(
            """
            <style>
            .container {
                background: linear-gradient(90deg, #3b5998, #4a69bd); 
                color: white;
                border-radius: 25px;
                padding: 1px;
                text-align: center;
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
                max-width: 500px;
                margin: 20px auto;
                font-family: Arial, sans-serif;
                font-size: 20px;
                border: 3px solid #a0c4ff;
                margin-bottom: 0px !important;
                padding-bottom: 0px !important;
                padding-right: 0px;
                padding-left: 0px;
                margin-top: -20px; !important;
            }
            .block-container {
                padding-top: 5px !important;
                margin-top: 5px !important;
                padding-bottom: 0px !important;

            }
            .stButton button {
                padding: 8px 45px !important;
                border-radius: 15px !important;
                margin: 0px auto !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
            }

            .st-key-like button {
                background-color: #32CD32;
                background-blend-mode: overlay;
                transition: background-color 0.3s ease;

            }

            .st-key-dislike button {
                background-color: #FF1A1A;
                background-blend-mode: overlay;
                transition: background-color 0.3s ease;

            }
            .st-key-like button:hover {
                background-color: #008000;
                background-blend-mode: overlay;

            }
            .st-key-dislike button:hover {
                background-color: #B22222;
                background-blend-mode: overlay;

            }
            img {
                border-radius: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                max-height: 25vh;
                display: flex;
                flex-direction: column;
            }
            .song-title {
                margin: 0;             
                padding: 0;         
                line-height: 1.1;
                font-size: 19px;
                font-weight: 600;
                color: white;
                margin-bottom: 0px;
                margin-top: 0px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }

            .song-artist {
                font-size: 17px;
                color: #e0ffe3;
                font-style: normal;
                opacity: 0.9;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            }

            </style>

            """,
            unsafe_allow_html=True,
        )
        total_steps = 10
        completed_steps = current_index + 1
        progress = " ".join(["●" if i < completed_steps else "○" for i in range(total_steps)])

        st.markdown(
            f"""
            <div class="container">
                <div style="text-align: left; font-size: 12px; padding-left: 10px;">{progress} {completed_steps}/{total_steps}</div>
                <div class="song-title">{song_title}</div>
                <div class="song-artist">{song_artist}</div>
                
            </div>
            """,
            unsafe_allow_html=True,
        )


        track_url = st.session_state.songs_df.loc[current_index, 'embed_code']

        if "track/" in track_url:
            track_id = track_url.split("track/")[-1].split("?")[0]
            embed_url = f"https://open.spotify.com/embed/track/{track_id}?theme=0"
        else:
            embed_url = track_url

        st.components.v1.html(f"""
        <!-- Loader -->
        <div id="loader" style="display: flex; justify-content: center; align-items: center; height: 265px;">
            <div class="spinner"></div>
        </div>

        <!-- Error Message and Retry Button -->
        <div id="error-msg" style="display: none; height: 265px; background: linear-gradient(145deg, #000000, #1a1a1a); display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding-top: 20px; gap: 10px;">
        <p style="margin:10px; font-size:20px; font-weight:600; color:#fff; font-family:Arial, sans-serif;"> Oops! The song failed to load </p>
            <div onclick="reloadIframe()" class="try-again-button">
                <div class="try-text">TRY AGAIN ⟳</div>
            </div>
        </div>

        <!-- Iframe container -->
        <div style="width: 100%; display: flex; justify-content: center;">
            <div id="iframe-container" style="display: none; transform: scale(0.74); transform-origin: top center;"></div>
        </div>

        <!-- Logic -->
        <script>
        let iframeLoaded = false;
        let gaveUp = false;

        function createIframe() {{
            iframeLoaded = false;
            gaveUp = false;

            const iframeContainer = document.getElementById("iframe-container");
            iframeContainer.innerHTML = "";

            const iframe = document.createElement("iframe");
            iframe.src = "{embed_url}";
            iframe.width = "100%";
            iframe.height = "352px";
            iframe.style.borderRadius = "30px";
            iframe.style.marginBottom = "0px";
            iframe.frameBorder = "0";
            iframe.allowFullscreen = true;
            iframe.allow = "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";

            iframe.onload = function() {{
                iframeLoaded = true;
                if (!gaveUp) {{
                    document.getElementById("loader").style.display = "none";
                    document.getElementById("iframe-container").style.display = "block";
                    document.getElementById("error-msg").style.display = "none";
                }}
            }};

            iframeContainer.appendChild(iframe);

            setTimeout(function() {{
                if (!iframeLoaded) {{
                    gaveUp = true;
                    document.getElementById("loader").style.display = "none";
                    document.getElementById("iframe-container").style.display = "none";
                    document.getElementById("error-msg").style.display = "flex";
                }}
            }}, 4000);
        }}

        function reloadIframe() {{
            document.getElementById("loader").style.display = "flex";
            document.getElementById("error-msg").style.display = "none";
            document.getElementById("iframe-container").style.display = "none";
            createIframe();
        }}

        window.addEventListener("DOMContentLoaded", function() {{
            createIframe();
        }});
        </script>

        <!-- Styles -->
        <style>
        .spinner {{
          border: 4px solid rgba(0, 0, 0, 0.1);
          width: 40px;
          height: 40px;
          border-radius: 50%;
          border-left-color: #1DB954;
          animation: spin 1s linear infinite;
          margin: auto;
        }}

        @keyframes spin {{
          to {{ transform: rotate(360deg); }}
        }}

        .try-again-button {{
            position: relative;
            width: 150px;
            height: 150px;
            background-color: #4d4d4d;
            border-radius: 50%;
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: sans-serif;
            user-select: none;
            transition: transform 0.2s;
        }}

        .try-again-button:hover {{
            transform: scale(1.05);
        }}

        .try-text {{
            font-size: 18px;
            font-weight: bold;
            color: white;
            text-align: center;
            z-index: 1;
        }}


        .top-left {{
            top: 12px;
            left: 12px;
        }}

        .bottom-right {{
            bottom: 12px;
            right: 12px;
        }}
        </style>
        """, height=265)

        problem_msg = """
        <div style="display: flex; justify-content: center; align-items: center; min-height: 200px; flex-direction: column;">
            <div style="
                background-color: #2b2b2b;
                padding: 5px 10px;
                border-radius: 12px;
                box-shadow: 0 0 15px rgba(0,0,0,0.3);
                color: #eeeeee;
                text-align: center;
                max-width: 500px;
                font-family: 'Segoe UI', sans-serif;
            ">
                <p style="margin-top: 0; color: #dddddd; font-size:22px;">Oops! A minor technical issue happened 🛠️</p>
                <p style="font-size: 15px;">
                    Due to a technical issue, we couldn’t save your song feedback.<br>
                    We’re sorry about that - We’ll restart the rating process for you.<br>
                    Thanks for your patience!
                </p>
            </div>
        </div>
        <div style="height: 10px;"></div>
        """

        def handle_like():
            if not st.session_state.button_clicked:
                st.session_state.button_clicked = True
                st.session_state.song_feedback.append([1])
                st.session_state.current_song_index += 1
                if st.session_state.current_song_index >= len(st.session_state.songs_df):
                    if len(st.session_state.song_feedback) != 10:
                        st.session_state.problem = True
                        st.markdown(problem_msg, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col2:
                            st.button("ok", key="ok", on_click=button_click_problem, use_container_width=True)
                            return
                    st.session_state.page = "persona_reveal"


        def handle_dislike():
            if not st.session_state.button_clicked:
                st.session_state.button_clicked = True
                st.session_state.song_feedback.append([0])
                st.session_state.current_song_index += 1
                if st.session_state.current_song_index >= len(st.session_state.songs_df):
                    if len(st.session_state.song_feedback) != 10:
                        st.session_state.problem = True
                        st.markdown(problem_msg, unsafe_allow_html=True)
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col2:
                            st.button("ok", key="ok", on_click=button_click_problem, use_container_width=True)
                            return
                    st.session_state.page = "persona_reveal"

        col1, col2, col3 = st.columns(3)

        with col3:
            st.button("👎", key="dislike", on_click=handle_dislike)

        with col1:
            st.button("👍", key="like", on_click=handle_like)
    else:
        st.session_state.page = "persona_reveal"


