import streamlit as st
import base64

import streamlit as st
import base64

def render_progress_bar(current_step, top_pad=55):
    steps = ['aaa', 'bbb', 'ccc', 'ddd']

    step_html = ""
    for step in steps:
        class_name = "progress-step active" if step == current_step else "progress-step"
        step_html += f'<div class="{class_name}">{step}</div>'

    # CSS + HTML
    st.markdown(f"""
    <style>
    /* הסרגל עצמו */
    .progress-bar-wrapper {{
        width: 100%;
        background: linear-gradient(90deg, #0e1e40, #122750, #1a3366);
        display: flex;
        justify-content: space-between;
        padding: 4px 8%;
        height: 36px;
        position: sticky;
        top: 0;
        z-index: 9999;
        margin-top: 6px;
    }}

    .progress-step {{
        flex-grow: 1;
        text-align: center;
        line-height: 28px;
        font-size: 14px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        color: white;
        background-color: #666;
        margin: 0 4px;
        border-radius: 4px;
        transition: background-color 0.3s;
    }}

    .progress-step.active {{
        background-color: #fff;
        color: #000;
    }}

    [data-testid="stAppViewContainer"] .block-container {{
        padding-top: {top_pad}px !important;
    }}
    </style>

    <div class="progress-bar-wrapper">
        {step_html}
    </div>
    """, unsafe_allow_html=True)


def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
        page_background = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #FFFFFF;
        }}
        </style>
        """
        st.markdown(page_background, unsafe_allow_html=True)


def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()