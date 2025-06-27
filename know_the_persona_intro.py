import streamlit as st
import time
from other_functions import render_progress_bar, set_background, get_base64_image


def typewriter_html_safe_chars(full_html_text: str, speed: float = 30.0):
    typed = ""
    tag_buffer = ""
    inside_tag = False
    container = st.session_state.main_container

    for char in full_html_text:
        if char == '<':
            inside_tag = True
            tag_buffer = char
        elif char == '>' and inside_tag:
            tag_buffer += char
            typed += tag_buffer
            tag_buffer = ""
            inside_tag = False
        elif inside_tag:
            tag_buffer += char
        else:
            typed += char

        container.markdown(
            f"""
                <div class="container">
                    <div class="header"> Know or Don't Know? </div>
                    <div class="sub-header">{typed}</div>
                    <div class="description"></div>
                </div>
                """,
            unsafe_allow_html=True
        )
        if not inside_tag:
            time.sleep(1 / speed)

    container.markdown(
        f"""
            <div class="container">
                <div class="header"> Know or Don't Know? </div>
                <div class="sub-header">{typed}</div>
                <div class="description">
                    <span class="green-text">Know this song?</span> Tap 💡<br>
                    <span class="red-text">Never heard of it?</span> Tap 🙉
                </div>
            </div>
            """,
        unsafe_allow_html=True
    )


def know_the_persona_intro_page():
    st.set_page_config(page_title="RankDist Demo")
    st.empty()
    render_progress_bar("meet the persona")
    set_background("other images/background.webp")

    def handle_start_click():
        st.session_state.page = "know_the_persona"

    lets_go = get_base64_image("other images/lets go.jpg")

    st.markdown(f"""
            <style>
            .container {{
                animation: fadeIn 0.7s ease-out both;
                background: linear-gradient(135deg, rgba(42, 91, 168, 0.97), rgba(76, 130, 199, 0.98), rgba(59, 111, 179, 0.98));
                color: white;
                border-radius: 25px;
                padding: 15px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                max-width: 450px;
                min-height: 280px;
                margin: auto;
                font-family: 'Poppins', sans-serif;
                margin-top: -20px !important;
            }}
            .block-container {{
                padding-top: 5px !important;
                margin-top: 5px !important;
                padding-bottom: 0px !important;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .header {{
                margin-top: 10px;
                font-size: 28px;
                color: #ffffff;
                font-family: 'Bebas Neue', sans-serif;
                font-weight: 800;
                text-shadow: 2px 2px 8px rgba(0,0,0,1);
            }}
            .sub-header {{
                font-size: 17px;
                font-weight: 500;
                color: #ffffff;
                font-family: 'Verdana', sans-serif;
                margin-bottom: 5px;
                margin-top: 5px;
                min-height: 65px;
            }}
            .description {{
                animation: pulse 2s infinite ease-in-out;
                font-size: 23px;
                margin-top: 14px;
                color: #ffffff;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 1; }}
                50% {{ transform: scale(1.05); opacity: 0.95; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            .green-text {{
                color: #32ff3e;
                font-weight: 600;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
            }}
            .red-text {{
                color: #ff3239;
                font-weight: 600;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
            }}
            .st-key-lets_go button {{
                width: 125px;
                height: 125px;
                background-color: transparent;
                border: none;
                cursor: pointer;
                border-radius: 50%;
                margin-top: 20px !important;
                transition: transform 0.6s ease-in-out, box-shadow 0.3s;
                box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.5);
                background-image: url('data:image/webp;base64,{lets_go}');
                background-size: cover;
                margin: auto;
                display: flex;
                flex-direction: column;
            }}
            .st-key-lets_go button:hover {{
                transform: rotate(360deg) scale(1.1);
                box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8);
            }}
            </style>
        """, unsafe_allow_html=True)

    persona_name = st.session_state.persona
    gender_possessive = st.session_state.possessive

    st.session_state.main_container = st.empty()
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])

    with button_col2:
        st.button("", key="lets_go", on_click=handle_start_click)

    typewriter_html_safe_chars(
        f"Listen to <strong style='color: #e64bff; text-shadow: 1px 1px 3px rgba(0,0,0,0.28);'>{persona_name}'s favorite songs</strong> and mark those you know. Knowing {gender_possessive} musical taste <strong style='color: #e64bff; text-shadow: 1px 1px 3px rgba(0,0,0,0.28);'>will help you recommend songs later</strong>",
        speed=23
    )
