import streamlit as st
import base64
import streamlit.components.v1 as components

def render_progress_bar(current_step, top_pad=55):
    steps = ['taste match',
             'meet the persona',
             'recommend songs',
             'results']

    step_html = "".join(
        f'<div class="progress-step{" completed" if steps.index(s) < steps.index(current_step) else " active" if s==current_step else ""}">{s}</div>'
        for s in steps
    )

    st.markdown(f"""
    <style>
    @keyframes fadeGreen {{
        0% {{
            background-color: #444;
        }}
        100% {{
            background-color: #25d366;
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
        transition: all 0.6s ease;
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
        background: #ffffff;
        color: #000000;
        font-weight: 600;
    }}

    .progress-step.completed {{
        background: #25d366;
        color: #ffffff;
        animation: fadeGreen 0.8s ease-out;
        font-weight: 500;
        font-size: 11px;
        font-family: 'Arial Narrow', sans-serif;
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


def render_song(embed_url: str, idx: int, height=85):
    st.components.v1.html(f"""
        <!-- Loader -->
        <div id="loader{idx}" style="display: flex; justify-content: center; align-items: center; height: {height}px;">
            <div class="spinner"></div>
        </div>

        <!-- Error Message and Retry Button -->
        <div id="error-msg{idx}" style="display: none; height: {height}px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding-top: 0px; gap: 5px;">
            <p style="margin:10px; font-size:14px; font-weight:600; color:#fff; font-family:Arial, sans-serif;">Oops! The song failed to load</p>
            <div onclick="reloadIframe{idx}()" class="try-again-button">
                <div class="try-text">⟳</div>
            </div>
        </div>

        <!-- Iframe container -->
        <div style="width: 100%; display: flex; justify-content: center;">
            <div id="iframe-container{idx}" style="display: none; transform-origin: top center;"></div>
        </div>

        <!-- Logic -->
        <script>
        let iframeLoaded{idx} = false;
        let gaveUp{idx} = false;

        function createIframe{idx}() {{
            iframeLoaded{idx} = false;
            gaveUp{idx} = false;

            const iframeContainer = document.getElementById("iframe-container{idx}");
            iframeContainer.innerHTML = "";

            const iframe = document.createElement("iframe");
            iframe.src = "{embed_url}";
            iframe.width = "100%";
            iframe.height = "85";
            iframe.style.marginBottom = "0px";
            iframe.frameBorder = "0";
            iframe.allowFullscreen = true;
            iframe.allow = "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";

            iframe.onload = function() {{
                iframeLoaded{idx} = true;
                if (!gaveUp{idx}) {{
                    document.getElementById("loader{idx}").style.display = "none";
                    document.getElementById("iframe-container{idx}").style.display = "block";
                    document.getElementById("error-msg{idx}").style.display = "none";
                }}
            }};

            iframeContainer.appendChild(iframe);

            setTimeout(function() {{
                if (!iframeLoaded{idx}) {{
                    gaveUp{idx} = true;
                    document.getElementById("loader{idx}").style.display = "none";
                    document.getElementById("iframe-container{idx}").style.display = "none";
                    document.getElementById("error-msg{idx}").style.display = "flex";
                }}
            }}, 4500);
        }}

        function reloadIframe{idx}() {{
            document.getElementById("loader{idx}").style.display = "flex";
            document.getElementById("error-msg{idx}").style.display = "none";
            document.getElementById("iframe-container{idx}").style.display = "none";
            createIframe{idx}();
        }}

        window.addEventListener("DOMContentLoaded", function() {{
            createIframe{idx}();
        }});
        </script>

        <!-- Styles -->
        <style>
        .spinner {{
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border-left-color: #1DB954;
            animation: spin 1s linear infinite;
            margin: auto;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        .try-again-button {{
            position: relative;
            width: 30px;
            height: 30px;
            background-color: #4d4d4d;
            border-radius: 50%;
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
            font-size: 16px;
            font-weight: bold;
            color: white;
            text-align: center;
            z-index: 1;
        }}
        </style>
    """, height=height)