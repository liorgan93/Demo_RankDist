import streamlit as st
from user_classification_intro import set_background
from other_functions import get_base64_encoded_file


def thank_you_page():
    st.set_page_config(page_title="RankDist Demo")
    page_clearer = st.empty()
    page_clearer.markdown(
        "<style>html,body{background:#fff;}</style>",
        unsafe_allow_html=True)


    set_background("other images/thank_you background.webp")
    file_path = "A Rank-Based Approach to Recommender System's Top-K Queries with Uncertain Scores (Technical Report).pdf"
    encoded_file = get_base64_encoded_file(file_path)


    st.markdown(
        """
        <style>
            .block-container {
                padding-bottom: 0px !important;
                margin-bottom: 0px !important;
                margin-top: 0px !important;
                padding-top: 40px !important;
            }

            .thank-you-container {
                text-align: center;
                padding: 35px 10px;
                border-radius: 30px;
                max-width: 800px;
                background: linear-gradient(135deg, #aad7ff, #d8b9eb);
            }

            .thank-you-title {
                font-family: 'Cormorant Garamond', serif;
                font-size: 27px;
                font-weight: 1000;
                color: blue;
                padding: 0 4px;
                margin-bottom: 18px;
                margin-top: 8px;
                letter-spacing: 0.7px;
            }

            .thank-you-message {
                font-family: Georgia, 'Times New Roman', serif;
                font-size: 17px;
                color: #333;
                margin-bottom: 20px;
                font-weight: bold;
                padding: 3px 0px;
            }

            .download-button a {
                display: inline-block;
                text-decoration: none;
                background-color: black;
                color: white;
                padding: 14px 30px;
                border-radius: 30px;
                font-size: 17px;
                font-weight: 600;
                transition: background-color 0.3s ease, transform 0.2s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }

            .download-button a:hover {
                transform: scale(1.05);
            }
            .logo-img {
              width: 113px; 
              height: 130px; 
              margin-bottom: 50px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    logo = get_base64_encoded_file("other images/logo.jpg")
    st.markdown(f"""
    <div class="thank-you-container">
        <img style="width: 180px; height: 90px; margin-top: -20px;" src="data:image/webp;base64,{logo}">
        <div class="thank-you-title">
            Thank You for Participating!
        </div>
        <div class="thank-you-message">
            we hope you enjoyed the demo! </br>
            Curious about the RankDist algorithm? Feel free to download the paper below!
        </div>
        <div class="download-button">
            <a href="data:application/pdf;base64,{encoded_file}" download="A Rank-Based Approach to Recommender System's Top-K Queries with Uncertain Scores (Technical Report).pdf">Download paper (PDF)</a>
        </div>
    </div>""", unsafe_allow_html=True)

    st.balloons()




