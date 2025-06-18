import time

import streamlit as st
from user_classification_intro import set_background
import base64


def thank_you_page():

    st.set_page_config(page_title="RankDist Demo")
    def get_base64_encoded_file(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()
            return base64.b64encode(file_data).decode()

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
                padding-top: 60px !important;
            }

            .thank-you-container {
                text-align: center;
                padding: 35px 10px;
                border-radius: 30px;
                max-width: 800px;
                background: linear-gradient(135deg, #d0f5d3, #e8d4f5);
            }

            .thank-you-title {
                font-family: 'Cormorant Garamond', serif;
                font-size: 28px;
                font-weight: bold;
                color: #FFBF00;
                padding: 0 4px;
                margin-bottom: 15px;
                text-shadow: 3px 3px 8px rgba(0, 80, 160, 0.8), 0 0 12px rgba(0, 0, 0, 0.6);
                letter-spacing: 0.7px;
            }

            .thank-you-message {
                font-family: Georgia, 'Times New Roman', serif;
                font-size: 17px;
                color: #333;
                margin-bottom: 15px;
                font-weight: bold;
                padding: 3px 0px;
            }

            .download-button a {
                display: inline-block;
                text-decoration: none;
                background-color: #1E90FF;
                color: white;
                padding: 14px 30px;
                border-radius: 30px;
                font-size: 17px;
                font-weight: 600;
                transition: background-color 0.3s ease, transform 0.2s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }

            .download-button a:hover {
                background-color: #1C86EE;
                transform: scale(1.05);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="thank-you-container">
        <div class="thank-you-title">
            Thank You for Participating!
        </div>
        <div class="thank-you-message">
            We hope you enjoyed the demo!
            If you'd like to learn more about the methods demonstrated in this demo feel free to download and read the paper below
        </div>
        <div class="download-button">
            <a href="data:application/pdf;base64,{encoded_file}" download="A Rank-Based Approach to Recommender System's Top-K Queries with Uncertain Scores (Technical Report).pdf">⬇️ Download Paper (PDF)</a>
        </div>
    </div>""", unsafe_allow_html=True)

    st.balloons()




