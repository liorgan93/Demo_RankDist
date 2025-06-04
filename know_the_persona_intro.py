import streamlit as st
import base64

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

def know_the_persona_intro_page():
    st.set_page_config(page_title="RankDist Demo")
    set_background("other images/background.webp")

    def handle_start_click():
        st.session_state.page = "know_the_persona"

    st.markdown(
        """
        <style>
        .container {
            background: linear-gradient(135deg, rgba(42, 91, 168, 0.97), rgba(76, 130, 199, 0.98), rgba(59, 111, 179, 0.98));
            color: white;
            border-radius: 25px;
            padding-bottom: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 450px;
            margin: auto;
            font-family: 'Poppins', sans-serif;
        }
        .header-small {
            font-size: 14px;
            font-weight: 700;
            color: #FFFFFF; 
            background-color: rgba(94, 35, 157, 0.8); 
            padding: 1px 4px; 
            border-radius: 15px; 
            margin-bottom: 17px;
            
        }
        .block-container {
            padding-top: 20px !important;
            margin-top: 20px !important;
            padding-bottom: 0px !important;

        }
        .header {
            margin-top: 12px;
            font-size: 28px;
            font-weight: 600;
            color: #ffffff;
        }
        .sub-header {
            font-size: 17px;
            font-weight: 500;
            color: #ffffff;
            font-family: 'Verdana', sans-serif; 
            margin-bottom: 5px;
            margin-top: 0px;

        }
        .description {
            font-size: 20px;
            font-weight: 300;
            margin-top: 14px;
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
        """,
        unsafe_allow_html=True,
    )

    persona_name = st.session_state.persona
    gender_value = st.session_state.gender_pronoun

    st.markdown(f"""
        <div class="container">
            <div class="header-small">Soon you'll recommend songs for {persona_name} 📝 but first, let’s get to know {gender_value} better better to make better recommendations 🎯</div>
            <div class="header"> Know or Don't Know? </div>
            <div class="sub-header">We’ll now show you <strong>songs that {persona_name} likes</strong>. Listen to them to know {gender_value} better, and indicate for each song whether you know it</div>
            <div class="description">
                <span class="green-text">Know this song?</span> Tap ✅<br>
                <span class="red-text">Never heard of it?</span> Tap ✖️️
            </div>
        </div>
    """, unsafe_allow_html=True)

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

