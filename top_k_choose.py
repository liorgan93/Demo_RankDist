import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
import base64

def top_k_choose_page():
    st.set_page_config(page_title="RankDist Demo", layout="wide")
    from user_classification_intro import set_background
    set_background("other images/background.webp")

    audio_folder = "top_k_songs_audio"
    csv_file_path = "playlists_excel/top_k_songs.csv"
    songs_data = pd.read_csv(csv_file_path)

    persona_name = st.session_state.persona

    st.markdown("""
    <style>

        .block-container {
            padding-top: 20px !important;
            padding-bottom: 2px !important;
            padding-bottom: 0px !important;
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
            padding: 3px !important; /* פחות padding */
        }

        div[data-testid="stExpander"] div.streamlit-expanderContent {
            color: white !important;
            min-width: 100% !important;
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
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
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .instructions {
            background: linear-gradient(90deg, #3b5998, #4a69bd); 
            color: white;
            border-radius: 25px;
            padding: 13px;
            margin: auto;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            max-width: 500px;
            font-family: Arial, sans-serif;
            font-size: 22px;
            border: 3px solid #a0c4ff;
            margin-bottom: 0px !important;
            padding-right: 0px;
            padding-left: 0px;
        }
        """,
        unsafe_allow_html=True,
    )


    with st.container():
        st.markdown(f"""<div class="instructions"> 
                            <div class="song-title">Choose the TOP 3 songs you would recommend for {persona_name}</div>""",unsafe_allow_html = True)

        if "error_msg" not in st.session_state:
            st.session_state.error_msg = ""

        def handle_confirm_click():
            if len(selected_songs) != 3:
                st.session_state.error_msg = "You must select exactly 3 songs before continuing."
            else:
                st.session_state.page = "compare_recommendations"
                st.session_state.user_choice = selected_songs

        col_next = st.columns([0.15, 0.7, 0.15])

        with col_next[1]:
            selected_songs = st.multiselect("", songs_data["song"].tolist(), max_selections=3)
        col_next = st.columns([1, 1, 1])

        with col_next[1]:
            st.button("Confirm", key="confirm_button", on_click=handle_confirm_click, use_container_width=True)

        st.markdown("""
            <div style="width: 100%; text-align: center; margin: 25px 0;">
                <div style="display: flex; justify-content: center; 
                            background: linear-gradient(135deg, rgba(80, 40, 120, 0.95), rgba(60, 60, 150, 0.95)); 
                            color: white; font-size: 18x; font-weight: bold; padding: 2px 0; 
                            border-radius: 50px; width: 100%; text-align: center; box-shadow: 0px 0px 10px rgba(0,0,0,0.5);">
                    You can listen to the songs below (Loading the songs may take a few moments) 🎧
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)

    cols = st.columns(3, gap="small")

    def encode_audio(audio_path):
        try:
            with open(audio_path, "rb") as audio_file:
                encoded_audio = base64.b64encode(audio_file.read()).decode()
            return encoded_audio
        except FileNotFoundError:
            return None

    for idx, row in songs_data.iterrows():
        song_name = row["song"]
        audio_path = os.path.join(audio_folder, f"{song_name}.mp3")

        with cols[idx % 3]:
            with st.expander(f"🎶 Listen to - {song_name}"):
                audio_base64 = encode_audio(audio_path)

                if audio_base64:
                    audio_html = f"""
                    <audio controls style="width: 100%; height: 30px;">
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
                    </audio>
                    """
                    components.html(audio_html, height=40)
                else:
                    st.error(f"Could not load audio for {song_name}.")

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
