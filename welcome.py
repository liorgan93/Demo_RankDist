import streamlit as st
import base64
from user_classification_intro import set_background


if "page" not in st.session_state:
    st.session_state.page = "welcome"


def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

def welcome_page():
    st.set_page_config(page_title="RankDist Demo")

    def click_button():
        st.session_state.page = "opening"

    set_background("other images/background.webp")

    logo = get_base64_image("other images/logo.jpg")
    music = get_base64_image("other images/music notes.png")

    st.markdown(
        f"""
        <style>
        .container {{
            background: linear-gradient(135deg, rgba(10, 10, 40, 0.98), rgba(20, 20, 60, 0.98));
            border-radius: 20px;
            padding: 5px;
            box-shadow: 0px 0px 20px rgba(0, 0, 100, 0.8);
            text-align: center;
            margin: auto;
            margin-bottom: 10px;
            width: 100%;
            max-width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            
        }}
        .block-container {{
            padding-top: 25px !important;
            margin-top: 25px !important;
            padding-bottom: 0px !important;

        }}
        .title-text {{
            font-size: 21px !important;
            font-weight: bold;
            text-shadow: 4px 4px 15px rgba(0,150,255,0.9);
            color: #B3E5FC;
            margin-bottom: 3px;
            margin-top: 0px;
            padding-bottom: 3px;
            padding-top: 0px;

        }}
        .treble-clef {{
            padding-top: 0px;
            margin-bottom: 0px;
            max-width: 100%;
        }}
        .music-image {{
            margin-bottom: 0px;
            padding-bottom: 0px;
            height: 70px;
            
            width: auto;
            object-fit: contain;

        }}
        @keyframes pulse {{
          0% {{ transform: scale(1); }}
          50% {{ transform: scale(1.05); }}
          100% {{ transform: scale(1); }}
        }}
        
        @keyframes glow {{
          0%, 100% {{ filter: drop-shadow(0 0 0px rgba(0, 204, 255, 0)); }}
          50% {{ filter: drop-shadow(0 0 5px rgba(0, 204, 255, 0.4)); }}
        }}
        
        .logo-img {{
          animation: glow 2.5s ease-in-out infinite, pulse 2.5s ease-in-out infinite;
          width: 187px; 
          height: 88px; 
          margin-bottom: 3px;
        }}

        .time_est {{
            font-size: 14px;
            color: #CCCCCC;
            text-align: left;
            font-weight: bold;
            padding-bottom: 13px;

        }}
        </style>
        <div class="container">
            <img class="logo-img" src="data:image/webp;base64,{logo}" class="logo-image">
            <p class="title-text">Welcome to our Music Recommendation Experience</p>
            <div class="time_est"> Estimated time: <strong> 8–10 minutes </strong> </div>
            <img src="data:image/webp;base64,{music}" class="music-image">
        </div>
        """,
        unsafe_allow_html=True,
    )
    start = get_base64_image("other images/start.jpg")
    st.markdown("""
            <style>
            .st-key-start_button button {
                width: 115px;
                height: 115px;
                background-color: transparent;
                border: none;
                cursor: pointer;
                border-radius: 50%;
                transition: transform 0.6s ease-in-out, box-shadow 0.3s;
                box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.5);
                background-image: url('data:image/webp;base64,""" + start + """');
                background-size: cover;
                margin: auto;
                display: flex;
                flex-direction: column;
                margin-top: -17px;

            }
            .st-key-start_button button:hover {
                transform: rotate(360deg) scale(1.1);
                box-shadow: 0px 0px 30px rgba(255, 255, 255, 0.8);
            }
            </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.button("", key="start_button", on_click=click_button)

    st.markdown(
        f"""
            <style>
            .container-footer-note {{
                background: linear-gradient(135deg, rgba(60, 60, 60, 1), rgba(80, 80, 80, 1));
                border-radius: 3px;
                padding: 8px;
                box-shadow: 0px 0px 20px rgba(0, 0, 100, 0.8);
                text-align: center;
                margin: auto;
                width: 100%;
                max-width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                overflow-x: hidden;
                margin-top: 6px;
            }}

            .footer-note {{
                font-size: 11px;
                color: #CCCCCC;
                text-align: left;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.2;
                text-align: justify;
            }}
            </style>
            <div class="container-footer-note">
               <div class="footer-note">
                ✱ This demo offers an interactive music experience using songs played via Spotify’s official embed feature.
                All content is the property of the respective rights holders and is used solely for educational and research demonstration purposes.
            </div>
            </div>
            """,
        unsafe_allow_html=True,
    )


if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "opening":
    from opening import opening_page
    opening_page()
elif st.session_state.page == "user_classification_intro":
    from user_classification_intro import user_classification_intro_page
    user_classification_intro_page()
elif st.session_state.page == "user_classification":
    from user_classification import user_classification_page
    user_classification_page()
elif st.session_state.page == "persona_reveal":
    from persona_reveal import persona_reveal_page
    persona_reveal_page()
elif st.session_state.page == "know_the_persona_intro":
    from know_the_persona_intro import know_the_persona_intro_page
    know_the_persona_intro_page()
elif st.session_state.page == "know_the_persona":
    from know_the_persona import know_the_persona_page
    know_the_persona_page()
elif st.session_state.page == "method_choose":
    from method_choose import method_choose_page
    method_choose_page()
elif st.session_state.page == "perfect_precision_choose":
    from perfect_precision_choose import perfect_precision_choose_page
    perfect_precision_choose_page()
elif st.session_state.page == "relevant_set_choose":
    from relevant_set_choose import relevant_set_choose_page
    relevant_set_choose_page()
elif st.session_state.page == "ordered_list_choose":
    from ordered_list_choose import ordered_list_choose_page
    ordered_list_choose_page()
elif st.session_state.page == "relevant_set_compare_recommendations":
    from relevant_set_compare_recommendations import relevant_set_compare_recommendations_page
    relevant_set_compare_recommendations_page()
elif st.session_state.page == "perfect_precision_compare_recommendations":
    from perfect_precision_compare_recommendations import perfect_precision_compare_recommendations_page
    perfect_precision_compare_recommendations_page()
elif st.session_state.page == "ordered_list_compare_recommendations":
    from ordered_list_compare_recommendations import ordered_list_compare_recommendations_page
    ordered_list_compare_recommendations_page()
elif st.session_state.page == "compare_recommendations":
    from relevant_set_compare_recommendations import relevant_set_compare_recommendations_page
    relevant_set_compare_recommendations_page()
elif st.session_state.page == "thank_you":
    from thank_you import thank_you_page
    thank_you_page()
elif st.session_state.page == "research_page":
    from research_page import research_page
    research_page()
elif st.session_state.page == "thank_you_research":
    from thank_you_research import thank_you_research
    thank_you_research()