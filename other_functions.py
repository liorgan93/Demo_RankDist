import streamlit as st
import base64
import streamlit.components.v1 as components
import pandas as pd
import random
from io import StringIO

# Renders a visual progress bar, highlighting the current step.
def render_progress_bar(current_step, top_pad=55):
    steps = ['set your taste',
             'meet your match',
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

# Encodes an image file to a base64 string for embedding in HTML.
def get_base64_encoded_file(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()


# Embeds a Spotify song in an iframe with a loader.
def render_song(embed_url: str, idx: int, height: int = 85):
    st.components.v1.html(f"""
        <div id="loader{idx}" style="display:flex;justify-content:center;align-items:center;height:{height}px;">
            <div class="spinner"></div>
        </div>

        <div id="error-msg{idx}" style="display:none;height:{height}px;flex-direction:column;align-items:center;justify-content:flex-start;gap:5px;">
            <p style="margin:10px;font-size:14px;font-weight:600;color:#fff;font-family:Arial,sans-serif;">Oops! The song failed to load</p>
            <div onclick="reloadIframe{idx}()" class="try-again-button"><div class="try-text">⟳</div></div>
        </div>

        <div style="position:relative;width:100%;display:flex;justify-content:center;">
            <div id="tiny-reload{idx}" class="tiny-reload" style="display:none;" onclick="reloadIframe{idx}()">↻</div>
            <div id="iframe-container{idx}" style="display:none;"></div>
        </div>

        <script>
        let iframeLoaded{idx}=false, gaveUp{idx}=false;

        function createIframe{idx}(){{
            iframeLoaded{idx}=false; gaveUp{idx}=false;
            const c=document.getElementById("iframe-container{idx}");
            c.innerHTML="";
            const f=document.createElement("iframe");
            f.src="{embed_url}";
            f.width="90%"; f.height="{height}";
            f.frameBorder="0";
            f.allowFullscreen=true;
            f.allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";
            f.onload=function(){{
                iframeLoaded{idx}=true;
                if(!gaveUp{idx}){{
                    document.getElementById("loader{idx}").style.display="none";
                    c.style.display="block";
                    document.getElementById("error-msg{idx}").style.display="none";
                    document.getElementById("tiny-reload{idx}").style.display="flex";
                }}
            }};
            c.appendChild(f);
            setTimeout(function(){{
                if(!iframeLoaded{idx}){{
                    gaveUp{idx}=true;
                    document.getElementById("loader{idx}").style.display="none";
                    c.style.display="none";
                    document.getElementById("error-msg{idx}").style.display="flex";
                    document.getElementById("tiny-reload{idx}").style.display="none";
                }}
            }},4000);
        }}

        function reloadIframe{idx}(){{
            document.getElementById("loader{idx}").style.display="flex";
            document.getElementById("error-msg{idx}").style.display="none";
            document.getElementById("iframe-container{idx}").style.display="none";
            document.getElementById("tiny-reload{idx}").style.display="none";
            createIframe{idx}();
        }}

        window.addEventListener("DOMContentLoaded",createIframe{idx});
        </script>

        <style>
        .spinner{{
            border:4px solid rgba(0,0,0,0.1);
            width:24px;height:24px;border-radius:50%;
            border-left-color:#1DB954;animation:spin 1s linear infinite;
        }}
        @keyframes spin{{to{{transform:rotate(360deg);}}}}

        .try-again-button{{
            width:30px;height:30px;background:#4d4d4d;border-radius:50%;
            display:flex;align-items:center;justify-content:center;cursor:pointer;
            transition:transform .2s;
        }}
        .try-again-button:hover{{transform:scale(1.05);}}
        .try-text{{font-size:16px;font-weight:bold;color:#fff;}}

        .tiny-reload{{
            position:absolute;top:6px;right:0px;
            width:21px;height:21px;background:#4d4d4d;border-radius:50%;
            display:flex;align-items:center;justify-content:center;cursor:pointer;
            font-size:12px;color:#fff;transition:transform .2s;z-index:10;
        }}
        .tiny-reload:hover{{transform:rotate(90deg) scale(1.05);}}
        </style>
    """, height=height)




def read_random_subtable(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.read().splitlines()

    table_indices = [i for i, line in enumerate(lines) if line.strip().startswith("#SET")]

    table_ranges = []
    for idx in range(len(table_indices)):
        start = table_indices[idx] + 1
        end = table_indices[idx + 1] if idx + 1 < len(table_indices) else len(lines)
        table_ranges.append((start, end))


    selected_start, selected_end = random.choice(table_ranges)
    selected_lines = lines[selected_start:selected_end]

    selected_text = "\n".join(selected_lines)
    return pd.read_csv(StringIO(selected_text))

