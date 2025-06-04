import streamlit as st
import base64
import time

def click_a():
    st.session_state.page = "perfect_precision_choose"

def click_b():
    st.session_state.page = "ordered_list_choose"

def click_c():
    st.session_state.page = "relevant_set_choose"

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def method_choose_page():
    st.set_page_config(page_title="RankDist Demo")
    from user_classification_intro import set_background
    set_background("other images/background.webp")

    perfect_precision = get_base64_image("other images/blue.jpg")
    relevant_set = get_base64_image("other images/green.jpg")
    ordered_list = get_base64_image("other images/red.jpg")
    persona_name = st.session_state.persona
    gender_value = st.session_state.gender_pronoun



    st.markdown("""
        <style>
            .block-container {
                padding-top: 30px !important;
                padding-bottom: 0px !important;

            }
            .header-container {
                background-color: rgba(0, 0, 50, 0.99);
                padding: 1px;
                text-align: center;
                margin: 0 auto 5px auto !important;

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
            <p><strong>2️⃣<span style="text-decoration: underline;">Ordered List:</span></strong> Select and rank the TOP 3 songs in the correct order</p>
            <p><strong>3️⃣<span style="text-decoration: underline;">Perfect Precision:</span></strong> Pick exactly the TOP 3 songs, no mistakes allowed</p>

        </div>
    """, unsafe_allow_html=True)



    st.markdown("""
        <style>
        .st-key-aa button, .st-key-bb button, .st-key-cc button {
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
        .st-key-aa button:hover, .st-key-bb button:hover, .st-key-cc button:hover {
            transform: rotate(360deg) scale(1.1);
            box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8);
        }
        .st-key-cc button {
            background-image: url('data:image/webp;base64,""" + relevant_set + """');
        }
        .st-key-bb button {
            background-image: url('data:image/webp;base64,""" + ordered_list + """');
        }
        .st-key-aa button {
            background-image: url('data:image/webp;base64,""" + perfect_precision + """');
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.button("", key="cc", on_click=click_c, use_container_width=True)
        st.button("", key="bb", on_click=click_b, use_container_width=True)
        st.button("", key="aa", on_click=click_a, use_container_width=True)
