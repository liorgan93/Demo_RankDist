import streamlit as st
import base64
def render_progress_bar(current_step, top_pad=55):
    steps = ['taste match',
             'meet the persona',
             'recommend songs',
             'results']

    step_html = "".join(
        f'<div class="progress-step{" completed" if steps.index(s) < steps.index(current_step) else " active" if s==current_step else ""}">'
        + (f'<span class="step-label">✓&nbsp;&nbsp;{s}</span>' if steps.index(s) < steps.index(current_step) else f'<span class="step-label">{s}</span>')
        + '</div>'
        for s in steps
    )

    st.markdown(f"""
    <style>
    /* אנימציה */
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

    /* סרגל עליון מלא */
    .progress-bar-wrapper {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        width: 100vw;
        background: linear-gradient(90deg, #1b2d59, #26366a, #2f4580);
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        padding: 4px 5%;
        min-height: 40px;
        z-index: 9999;
        border-radius: 0 0 6px 6px;
    }}

    /* שלב בודד */
    .progress-step {{
        flex: 1;
        min-width: 0;
        max-width: 100%;
        text-align: center;
        font: 400 11.5px 'Poppins', sans-serif;
        line-height: 1.2;
        padding: 3px 4px !important;
        color: #fff;
        background: #444;
        margin: 2px;
        border-radius: 8px;
        transition: all 0.4s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 36px;
    }}

    /* טקסט בשלב */
    .step-label {{
        white-space: normal;
        word-break: keep-all;
        overflow-wrap: normal;
    }}

    .progress-step.active {{
        background: #ffffff;
        color: #000000;
        font-weight: 600;
    }}

    .progress-step.completed {{
        background: #1DB954;
        color: #ffffff;
        font-weight: 500;
        font-size: 11px;
        animation: popFade 1.3s ease-out;
        text-shadow: 0 0 1px #00000077;
    }}

    /* מסכים קטנים */
    @media (max-width: 480px) {{
        .progress-step {{
            font-size: 10px;
            padding: 2px 3px;
        }}
    }}

    /* תן מקום מתחת לסרגל */
    body {{
        padding-top: {top_pad}px;
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