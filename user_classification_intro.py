import streamlit as st
import base64
import time

def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

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

def user_classification_intro_page():
    st.set_page_config(page_title="RankDist Demo")
    set_background("other images/background.webp")

    st.markdown(
        """
        <style>
        .container {
            background: linear-gradient(135deg, rgba(42, 91, 168, 0.98), rgba(76, 130, 199, 0.97), rgba(59, 111, 179, 0.98));
            color: white;
            border-radius: 25px;
            padding: 8px;
            padding-bottom: 15px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            margin: auto;
            font-family: 'Poppins', sans-serif;
        }
        .block-container {
            padding-top: 30px !important;
            margin-top: 30px !important;
            padding-bottom: 0px !important;

        }
        
        .header {
            margin-top: 10px;
            font-size: 28px;
            font-weight: 600;
            color: #ffffff;
        }
        .sub-header {
            font-size: 20px;
            font-weight: 500;
            color: #ffffff;
            font-family: 'Verdana', sans-serif; 
            margin-bottom: 5px;
            margin-top: 0px;

        }
        .description {
            font-size: 22px;
            font-weight: 300;
            margin-top: 14px;
            margin-bottom: 10px;
            color: #ffffff;
        }
        .footer {
            font-size: 16px;
            margin-top: 20px;
            color: #ffffff;
        }
        .green-text {
            color: #50c878;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
        }
        .red-text {
            color: #FF4747; 
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
        }
        </style>
        <div class="container">
            <div class="header"> Like or Dislike? </div>
            <div class="sub-header"> First, Let get familiar with your music taste! </div>
            <div class="description">
                <span class="green-text">Like the song?</span>&nbsp;&nbsp;Tap 👍 <br>
                <span class="red-text">Not your vibe?</span>&nbsp;&nbsp;Tap 👎
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def handle_start_click():
        st.session_state.page = "user_classification"

    lets_go = get_base64_image("other images/lets go.jpg")
    st.markdown("""
            <style>
            .st-key-lets_go button{
                width: 125px;
                height: 125px;
                background-color: transparent;
                border: none;
                cursor: pointer;
                border-radius: 50%;
                margin-bottom: 0px;
                margin-top: 20px !important;
                transition: transform 0.6s ease-in-out, box-shadow 0.3s;
                box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.5);
                background-image: url('data:image/webp;base64,""" + lets_go + """');
                background-size: cover;
                margin: auto;
                display: flex;
                flex-direction: column;

            }
            .st-key-lets_go button:hover {
                transform: rotate(360deg) scale(1.1);
                box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8);
            }
            </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("", key="lets_go", on_click=handle_start_click)



