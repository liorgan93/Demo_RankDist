import streamlit as st
import pandas as pd
from other_functions import set_background
from other_functions import render_progress_bar

def get_songs_by_persona(persona_num):
    set_background("other images/background.webp")
    df = pd.read_csv('csv_files/personas_songs.csv')
    songs_df = df[df['cluster'] == persona_num]
    return songs_df

def know_the_persona_page():
    st.set_page_config(page_title="RankDist Demo")
    st.empty()
    render_progress_bar("meet your match")
    persona_name = st.session_state.persona
    persona_number = st.session_state.chosen_person_number
    st.session_state.persona_songs_df = get_songs_by_persona(persona_number)

    if "song_index" not in st.session_state:
        st.session_state.song_index = 0

    if "known_songs_count" not in st.session_state:
        st.session_state.known_songs_count = 0

    current_index = st.session_state.song_index

    if st.session_state.known_songs_count >= 3 or current_index >= len(st.session_state.persona_songs_df):
        st.session_state.page = "method_choose"
        st.rerun()
    else:
        song_title = st.session_state.persona_songs_df.iloc[current_index]["name"]
        song_artist = st.session_state.persona_songs_df.iloc[current_index]["artist"]

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
                margin-bottom: 3px !important;
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
                padding: 7px 45px !important;
                border-radius: 15px !important;
                margin: 0px auto !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
            }

            .st-key-know button {
                background-color: #32CD32;
                background-blend-mode: overlay;
                transition: background-color 0.3s ease;

            }

            .st-key-dont_know button {
                background-color: #FF1A1A;
                background-blend-mode: overlay;
                transition: background-color 0.3s ease;

            }
            .st-key-know button:hover {
                background-color: #008000;
                background-blend-mode: overlay;

            }
            .st-key-dont_know button:hover {
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
        completed_steps = current_index + 1

        st.markdown(
            f"""<div class="container">
                <div style="text-align: left; margin-bottom: 2px; font-size: 13px; padding-left: 10px; color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.4);">
                    Songs that {persona_name} Likes – Song Number {completed_steps}
                </div>
                <div class="song-title">{song_title}</div>
                <div class="song-artist">{song_artist}</div>
                    </div>
                    """,
            unsafe_allow_html=True,
        )


        track_url = st.session_state.persona_songs_df.iloc[current_index]["embed_code"]

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

         <!-- Iframe container with small reload button -->
         <div class="iframe-wrapper" style="position: relative; width: 100%; display: flex; justify-content: center; overflow: visible;">
             <!-- SMALL RELOAD BUTTON (⟳) -->
             <div class="tiny-reload" onclick="reloadIframe()">↻</div>

             <!-- Original iframe container -->
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
           border: 9px solid rgba(0, 0, 0, 0.1);
           width: 50px;
           height: 50px;
           border-radius: 50%;
           border-left-color: #d6d6cb;
           background:rgba(0,0,0,0.40);
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

         /* ---------- TINY RELOAD BUTTON STYLE ---------- */
         .tiny-reload {{
             position: absolute;
             top: 4px;       
             right: 6px;
             width: 29px;
             height: 29px;
             background-color: #4d4d4d;
             border-radius: 50%;
             box-shadow: 0 4px 8px rgba(0,0,0,0.3);
             display: flex;
             align-items: center;
             justify-content: center;
             cursor: pointer;
             font-size: 17px;
             color: white;
             transition: transform 0.2s;
             z-index: 10;
         }}

         .tiny-reload:hover {{
             transform: rotate(90deg) scale(1.05);
         }}
         </style>
         """, height=265)

        def handle_know_song():
            st.session_state.song_index += 1
            st.session_state.known_songs_count += 1

        def handle_dont_know_song():
            st.session_state.song_index += 1

        col1, col2, col3 = st.columns(3)

        with col3:
            st.button("Dont Know 🙉", key="dont_know", on_click=handle_dont_know_song)

        with col1:
            st.button("Know 💡", key="know", on_click=handle_know_song)
