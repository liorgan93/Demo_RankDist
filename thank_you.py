import streamlit as st
from user_classification_intro import set_background
import time
import base64


def thank_you_page():
    st.set_page_config(page_title="RankDist Demo")
    def get_base64_encoded_file(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()
            return base64.b64encode(file_data).decode()

    file_path = "A Rank-Based Approach to Recommender System's Top-K Queries with Uncertain Scores (Technical Report).pdf"
    encoded_file = get_base64_encoded_file(file_path)

    set_background("other images/background.webp")
    st.balloons()
    st.markdown(
        """
        <style>
            .block-container {
                padding-bottom: 0px !important;
    
            }
            .flipped-emoji {
                display: inline-block;
                transform: scaleX(-1);
            }
            .thank-you-container {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                text-align: center;
                padding-top: 40px;
                padding-bottom: 30px;
                background: linear-gradient(135deg, rgba(225, 200, 255, 0.95), rgba(200, 220, 255, 0.95));
                border-radius: 30px;
                max-width: 100%;
                margin: auto;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            }
            .thank-you-title {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                text-align: center;
                padding: 20px 10px;
                margin-bottom: 25px;
                background: linear-gradient(135deg, #1e1e3f, #3a3a8a, #6a1b9a);
                border-radius: 15px;
                box-shadow: 0 4px 25px rgba(58, 58, 138, 0.6), 0 0 15px rgba(106, 27, 154, 0.5);
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6), 0 0 10px rgba(106, 27, 154, 0.9);
                transition: all 0.3s ease-in-out;
            }
            .thank-you-message {
                font-size: 19px;
                color: #444;
                margin-bottom: 15px;
                padding: 0 15px;
            }
            .download-button a {
                display: inline-block;
                text-decoration: none;
                background-color: #1E90FF;
                color: white;
                padding: 12px 25px;
                border-radius: 25px;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            .download-button a:hover {
                background-color: #1C86EE;
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
            We appreciate your time and hope you enjoyed the demo. If you'd like to To learn more about the methods demonstrated in this demo, You're welcome to download the paper below!
        </div>
        <div class="download-button">
            <a href="data:application/pdf;base64,{encoded_file}" download="A Rank-Based Approach to Recommender System's Top-K Queries with Uncertain Scores (Technical Report).pdf">⬇️ Download Paper (PDF)</a>
        </div>
    </div>""", unsafe_allow_html=True)

