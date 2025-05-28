import streamlit as st
from user_classification_intro import set_background
import time
import base64


def thank_you_research():
    placeholder = st.empty()
    placeholder.empty()
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
            .flipped-emoji {
                display: inline-block;
                transform: scaleX(-1);
            }

            .thank-you-container {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                text-align: center;
                padding-top: 60px;
                padding-bottom: 60px;
                background: linear-gradient(135deg, rgba(225, 200, 255, 0.95), rgba(200, 220, 255, 0.95));
                border-radius: 30px;
                max-width: 90%;
                margin: auto;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            }
            .thank-you-title {
                font-size: 32px;
                font-weight: bold;
                color: #222;
                margin-bottom: 15px;
            }
            .thank-you-message {
                font-size: 20px;
                color: #444;
                margin-bottom: 25px;
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
             Thank you for your participation! 🎉<span class="flipped-emoji"></span>
        </div>
        <div class="thank-you-message">
            We appreciate your time and insights — Your input has been successfully recorded and will contribute meaningfully to our research.
        </div>
    </div>""", unsafe_allow_html=True)

