import streamlit as st
import base64
def render_progress_bar(current_step, top_pad=55):
    steps = ['taste match',
             'meet the persona',
             'recommend songs',
             'results']

    step_html = "".join(
        f'<div class="progress-step{" completed" if steps.index(s) < steps.index(current_step) else " active" if s==current_step else ""}">'
        + s +
        '</div>'
        for s in steps
    )

    st.markdown(f"""
    <style>
    @keyframes popFade {{
        0% {{
            opacity: 0;
            transform: scale(0.92) translateY(6px);
        }}
        60% {{
            opacity: 0.8;
            transform: scale(1.02) translateY(-2px);
        }}
        100% {{
            opacity: 1;
            transform: scale(1) translateY(0);
        }}
    }}

    .progress-bar-wrapper {{
        width: 100%;
        background: linear-gradient(90deg, #1b2d59, #26366a, #2f4580);
        display: flex;
        justify-content: space-between;
        flex-wrap: nowrap;   
        padding: 4px 0.5%;
        min-height: 36px;
        position: sticky;
        top: 0;
        z-index: 9999;
        margin-top: 3px;
        border-radius: 3px;
        position: relative;
    }}

    .progress-bar-wrapper::before {{
        content: "";
        position: absolute;
        top: 50%;
        left: 3%;
        right: 3%;
        height: 2px;
        background-color: white;
        opacity: 0.4;
        z-index: 0;
        transform: translateY(-50%);
    }}

    .progress-step {{
        font-family: 'Arial Narrow', sans-serif;
        font-weight: 500;
        font-size: 11px;
        letter-spacing: 0px;
        flex: 1;
        min-width: 0;
        text-align: center;
        line-height: 1.1;        
        padding: 2px 2px !important;  
        color: #fff;
        background: #444;
        margin: 0 3px;
        border-radius: 8px;
        transition: all 0.4s ease;
        white-space: normal;
        overflow-wrap: break-word; 
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 1;
    }}

    .progress-step:last-child {{
        border-right: none;
    }}

    .progress-step.active {{
        font-family: 'Arial Narrow', sans-serif;
        background: #ffffff;
        color: #000000;
        font-weight: 600;
    }}

    .progress-step.completed {{
        background: #25d366;
        color: #ffffff;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: 500;
        font-size: 11px;
        animation: popFade 1.3s ease-out;
        text-shadow: 0 0 1px #00000077;
    }}

    [data-testid="stAppViewContainer"] .block-container {{
        padding-top: {top_pad}px !important;
    }}
    </style>

    <div class="progress-bar-wrapper">{step_html}</div>
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