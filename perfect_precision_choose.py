import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from other_functions import set_background
from other_functions import render_progress_bar

def render_song_with_fallback(embed_url: str, height=85):
    st.components.v1.html(f"""
    <!-- Loader -->
    <div id="loader" style="display: flex; justify-content: center; align-items: center; height: {height}px;">
        <div class="spinner"></div>
    </div>

    <!-- Error Message and Retry Button -->
    <div id="error-msg" style="display: none; height: {height}px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;">
        <p style="margin:0; font-size:16px; font-weight:600; color:#fff; font-family:Arial, sans-serif;">Oops! The song failed to load</p>
        <div onclick="reloadIframe()" class="try-again-button">
            <div class="try-text">TRY AGAIN ⟳</div>
        </div>
    </div>

    <!-- Iframe container -->
    <div style="width: 100%; display: flex; justify-content: center;">
        <div id="iframe-container" style="display: none;"></div>
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
        iframe.height = {height};  // ←←← FIXED: now a number
        iframe.style.borderRadius = "12px";
        iframe.frameBorder = "0";
        iframe.allow = "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";
        iframe.loading = "lazy";

        iframe.onload = function() {{
            iframeLoaded = true;
            if (!gaveUp) {{
                document.getElementById("loader").style.display = "none";
                iframeContainer.style.display = "block";
                document.getElementById("error-msg").style.display = "none";
            }}
        }};

        iframeContainer.appendChild(iframe);

        setTimeout(function() {{
            if (!iframeLoaded) {{
                gaveUp = true;
                document.getElementById("loader").style.display = "none";
                iframeContainer.style.display = "none";
                document.getElementById("error-msg").style.display = "flex";
            }}
        }}, 4500);
    }}

    function reloadIframe() {{
        document.getElementById("loader").style.display = "flex";
        document.getElementById("error-msg").style.display = "none";
        document.getElementById("iframe-container").style.display = "none";
        createIframe();
    }}

    createIframe();
    </script>

    <!-- Styles -->
    <style>
    .spinner {{
      border: 4px solid rgba(0, 0, 0, 0.1);
      width: 30px;
      height: 30px;
      border-radius: 50%;
      border-left-color: #1DB954;
      animation: spin 1s linear infinite;
      margin: auto;
    }}

    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}

    .try-again-button {{
        width: 110px;
        height: 40px;
        background-color: #4d4d4d;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
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
        font-size: 14px;
        font-weight: bold;
        color: white;
        text-align: center;
        z-index: 1;
    }}
    </style>
    """, height=height)



def perfect_precision_choose_page():
    st.set_page_config(page_title="RankDist Demo", layout="wide")
    render_progress_bar("recommend songs")
    st.markdown("""
            <style>
                .progress-bar-wrapper{
                    max-width: 700px;   
                    margin-left: auto;
                    margin-right: auto;
                }
            </style>
        """, unsafe_allow_html=True)

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
                    Perfect Precision
                </div>
                <div class="text_choose">
                    Choose exactly the TOP 3 songs you’d recommend to {persona_name}
                </div>
            </div>
        """, unsafe_allow_html=True)

        if "error_msg" not in st.session_state:
            st.session_state.error_msg = ""

        def handle_confirm_click():
            if len(selected_songs) != 3:
                st.session_state.error_msg = "You must select exactly 3 songs."
            else:
                st.session_state.page = "perfect_precision_compare_recommendations"
                st.session_state.user_choice = selected_songs

        col_next = st.columns([0.15, 0.7, 0.15])
        with col_next[1]:
            selected_songs = st.multiselect("", songs_data["song"].tolist(), max_selections=3)

        col_next = st.columns([1, 1, 1])
        with col_next[1]:
            st.button("Confirm", key="confirm_button", on_click=handle_confirm_click, use_container_width=True)

        st.markdown("""
                <style>
                div[data-testid="stAlert"]{
                    background-color: #C62828 !important;   
                    padding-top: 0px !important;
                    padding-bottom: 0px !important;
                    margin-top: 0px !important;
                    margin-bottom: 0px !important;
                }
                div[data-testid="stAlert"] p {
                    text-align: center; !important;
                    font-weight: 700 !important; 
                }

                </style>
                """, unsafe_allow_html=True)
        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)

        st.markdown("""
            <div style="width: 100%; text-align: center; margin: 25px 0;">
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
                render_song_with_fallback(embed_url)
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

