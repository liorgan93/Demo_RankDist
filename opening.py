import streamlit as st
import base64
from user_classification_intro import set_background


def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()


def opening_page():
    st.set_page_config(page_title="RankDist Demo")
    image_base64 = get_base64_image("other images/RankDist_VS_Human.jpg")
    def click_button():
        st.session_state.page = "user_classification_intro"

    set_background("other images/background.webp")

    st.markdown(f"""
        <style>
        .info-container {{
            background: linear-gradient(135deg, rgba(10, 10, 40, 0.99), rgba(20, 20, 60, 0.99));
            border-radius: 20px;
            padding: 4px;
            box-shadow: 0px 0px 20px rgba(0, 0, 100, 0.8);
            text-align: center;
            margin: auto;
            margin-bottom: 0px;
            width: 98%;
            max-width: 98%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
        }}
        .block-container {{
            padding-top: 30px !important;
            margin-top: 30px !important;
            padding-bottom: 0px !important;

        }}
        .info-text-primary {{
            font-size: 16px;
            color: #BBDEFB;
            font-weight: 550;
            text-shadow: 1px 1px 5px rgba(100, 180, 255, 0.4);
            margin-top: 5px;
            margin-bottom: 26px;
            padding-top: 5px;
        }}
        .info-text-secondary {{
            font-size: 20px;
            color: #4DD0E1;
            font-weight: 700;
            text-shadow: 1px 1px 6px rgba(0, 200, 255, 0.5);
            padding-bottom: 15px;
        }}
        .alg-image {{
            max-width: 100%;
            max-height: 90px;
            margin-bottom: 10px;
            border-radius: 20px;
        }}
        </style>

        <div class="info-container">
            <div class="info-text-primary">
                In this demo you’ll recommend songs for someone 🧠🎵 and we’ll compare your picks to the RankDist algorithm’s output to demonstrate its performance 📊
            </div>
            <div class="info-text-secondary">
                Let’s find out how your intuition compares to data-driven recommendations!
            </div>
            <img src="data:image/webp;base64,{image_base64}" class="alg-image"/">
        </div>
    """, unsafe_allow_html=True)

    next = get_base64_image("other images/Next.jpg")

    st.markdown("""
        <style>
        .st-key-Next_button button {
            width: 125px;
            height: 125px;
            background-color: transparent;
            border: none;
            cursor: pointer;
            border-radius: 50%;
            transition: transform 0.6s ease-in-out, box-shadow 0.3s;
            box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.5);
            background-image: url('data:image/webp;base64,""" + next + """');
            background-size: cover;
            margin: auto;
            display: flex;
            flex-direction: column;
        }
        .st-key-Next_button button:hover {
            transform: rotate(360deg) scale(1.1);
            box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("", key="Next_button", on_click=click_button)
