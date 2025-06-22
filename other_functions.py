import streamlit as st
import base64

def render_progress_bar(current_step, top_pad=55):
    steps = ['taste match',
             'know the persona',
             'recommend song',
             'results']

    step_html = "".join(
        f'<div class="progress-step{" active" if s==current_step else ""}">{s}</div>'
        for s in steps
    )

    st.markdown(f"""
    <style>
    .progress-bar-wrapper{{
        width:100%;
        background:linear-gradient(90deg,#0e1e40,#122750,#1a3366);
        display:flex; justify-content:space-between; flex-wrap:nowrap;   
        padding:4px 5%;
        min-height:36px;
        position:sticky; top:0; z-index:9999; margin-top:6px; border-radius:3px;
    }}

    .progress-step{{
        flex:1;               
        min-width:0;              
        text-align:center;
        font:400 11.5px 'Poppins',sans-serif;
        line-height:1.1;        
        padding:2px 2px; !important;  
        color:#fff; background:#666;
        margin:0 3px; border-radius:8px;
        transition:background-color .3s;
        white-space:normal;      
        overflow-wrap:break-word; 
        display:flex;          
        align-items:center;    
        justify-content:center;
    }}

    .progress-step.active{{background:#fff;color:#000;}}

    [data-testid="stAppViewContainer"] .block-container{{
        padding-top:{top_pad}px !important;
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