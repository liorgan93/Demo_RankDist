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

    set_background("other images/background.webp")





