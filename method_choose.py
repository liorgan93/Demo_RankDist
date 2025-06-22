import streamlit as st
from other_functions import get_base64_image
from other_functions import render_progress_bar
from other_functions import set_background

def click_relevant_set():
    st.session_state.page = "relevant_set_choose"

def click_ordered_list():
    st.session_state.page = "ordered_list_choose"

def click_perfect_precision():
    st.session_state.page = "perfect_precision_choose"


def method_choose_page():
    st.set_page_config(page_title="RankDist Demo")
    render_progress_bar("ccc")
    set_background("other images/background.webp")

    perfect_precision = get_base64_image("other images/perfect_precision.jpg")
    relevant_set = get_base64_image("other images/relevant_set.jpg")
    ordered_list = get_base64_image("other images/ordered_list.jpg")
    persona_name = st.session_state.persona
    gender_value = st.session_state.gender_pronoun



    st.markdown("""
        <style>
            .block-container {
                padding-top: 5px !important;
                margin-top: 5px !important;
                padding-bottom: 0px !important;

            }
            .header-container {
                background-color: rgba(0, 0, 50, 0.99);
                padding: 1px;
                text-align: center;
                margin-top: -20px; !important;
            }

            .header-text {
                color: #ADD8E6;
                font-size: 18px !important;
                margin: 0;
                font-weight: bold;
            }
            .sub-header-text {
                color: #CCCCCC;
                font-size: 20px !important;
                margin: 0;
                font-weight: bold;
            }

            .explanation-container {
                background-color: rgba(30, 30, 60, 0.95);
                padding: 3px;
                border-radius: 20px;
                margin-top: 0px;
            }
            .explanation-container p {
                color: #FFFFFF;
                font-size: 13.5px;
                margin: 0 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="header-container">
            <p class="header-text">Now that you know {persona_name}, you’re ready to recommend songs for {gender_value}!</p>
            <p class="sub-header-text">Let’s Choose a task</p>
        </div>


        <div class="explanation-container">
            <p><strong>1️⃣<span style="text-decoration: underline;">Relevant Set:</span></strong> Choose the TOP 3, order doesn’t matter</p>
            <p><strong>2️⃣<span style="text-decoration: underline;">Ordered List:</span></strong> Pick the TOP 3 songs in exact order – 1st, 2nd, 3rd</p>
            <p><strong>3️⃣<span style="text-decoration: underline;">Perfect Precision:</span></strong> Choose exactly the TOP 3 songs – one mistake and it's wrong</p>
        </div>
    """, unsafe_allow_html=True)



    st.markdown("""
        <style>
        .st-key-perfect_precision button, .st-key-ordered_list button, .st-key-relevant_set button {
            width: 97px;
            height: 97px;
            background-color: transparent;
            border: none;
            cursor: pointer;
            border-radius: 50%;
            transition: transform 0.6s ease-in-out, box-shadow 0.3s;
            box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.5);
            background-size: cover;
            margin: auto;
            display: flex;
            flex-direction: column;

        }
        .st-key-perfect_precision button:hover, .st-key-ordered_list button:hover, .st-key-relevant_set button:hover {
            transform: rotate(360deg) scale(1.1);
            box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8);
        }
        .st-key-relevant_set button {
            background-image: url('data:image/webp;base64,""" + relevant_set + """');
        }
        .st-key-ordered_list button {
            background-image: url('data:image/webp;base64,""" + ordered_list + """');
        }
        .st-key-perfect_precision button {
            background-image: url('data:image/webp;base64,""" + perfect_precision + """');
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.button("", key="relevant_set", on_click=click_relevant_set, use_container_width=True)
        st.button("", key="ordered_list", on_click=click_ordered_list, use_container_width=True)
        st.button("", key="perfect_precision", on_click=click_perfect_precision, use_container_width=True)
