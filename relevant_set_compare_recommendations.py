import streamlit as st
import pandas as pd
import random
from user_classification_intro import set_background


def calculate_user_score():
    return 0.67, "2/3"

def calculate_alg_score():
    return 1, "3/3"

def html_table(df):
    html = """
    <style>
        .dark-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
            font-family: 'Segoe UI', sans-serif;
            color: #e5e5e5;
            background-color: #000000;
            border: 1px solid #333;
            border-radius: 8px;
            overflow: hidden;
        }
        .dark-table td {
            border: 1px solid #444;
            padding: 5px;
            text-align: left;
            font-size: 11px;
            font-weight: 600 !important;

        }
        .dark-table th {
            text-align: left;
            background-color: #1f1f2e; 
            color: #aaaaaa;           
            font-weight: bold;
            font-size: 12.5px;
        }
        .dark-table tr {
            background-color: #000000;
        }
    </style>
    <table class="dark-table">
        <thead>
            <tr>
    """
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html

def relevant_set_compare_recommendations_page():
    st.set_page_config(page_title="RankDist Demo")
    set_background("other images/blue_b.jpg")
    selected_songs = st.session_state.user_choice
    algorithm_df = pd.read_csv("alg_results.csv")

    if 'top_k' not in algorithm_df.columns:
        st.error("Error: The file must contain a 'top_k' column.")
        return

    algorithm_songs = sorted(set(algorithm_df['top_k'].dropna().tolist()))
    user_songs = sorted(set(selected_songs))

    matching_songs = sorted(set(user_songs).intersection(set(algorithm_songs)))
    non_matching_user_songs = sorted(set(user_songs) - set(algorithm_songs))
    non_matching_algorithm_songs = sorted(set(algorithm_songs) - set(user_songs))

    max_length = max(len(matching_songs) + len(non_matching_user_songs), len(matching_songs) + len(non_matching_algorithm_songs))
    user_column = matching_songs + non_matching_user_songs + [""] * (max_length - len(matching_songs) - len(non_matching_user_songs))
    algorithm_column = matching_songs + non_matching_algorithm_songs + [""] * (max_length - len(matching_songs) - len(non_matching_algorithm_songs))

    real_top_k = ["Dancing Queen", "Hallelujah", "Imagine"]
    real_top_k_column = real_top_k + [""] * (max_length - len(real_top_k))

    comparison_df = pd.DataFrame({
        "Your picks": user_column,
        "RankDist's output": algorithm_column,
        "True preference": real_top_k_column
    })

    user_score = calculate_user_score()
    alg_score = calculate_alg_score()

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 40px !important;
            padding-bottom: 0px !important;
        }
        .title-text {
            text-align: center;
            margin-top: 0px;
            margin-bottom: 25px;
            padding-top: 0px;
            font-size: 24px !important;
            font-weight: bold;
            text-shadow: 4px 4px 15px rgba(0,150,255,0.9);
        }
        .stButton button {
            width: 100%;
            font-size: 18px;
            padding: 15px;
            border-radius: 15px;
            background-color: #800080;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-top: 0px !important;
        }
        .stButton button:hover {
            background-color: #660066;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="title-text">Comparison and Evaluation</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; margin-top:-28px; font-size:15px; font-weight: bold; font-family: Segoe UI, sans-serif;">Your picks VS the RankDist algorithm</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.05, 0.9, 0.05])
    with col2:
        st.markdown(html_table(comparison_df), unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; font-size:17px; margin-top:-5px !important;'>🧍<b>Your Score:</b> {user_score[1]} &nbsp;&nbsp;&nbsp;🤖<b>RankDist Score:</b> {alg_score[1]}</div>", unsafe_allow_html=True)


    user_win_msg = "You won 🏆 — your intuition beat the algorithm!"
    algo_win_msg = "The RankDist algorithm won 🏆 — looks like it can mimic and even surpass human intuition!"
    tie_msg = "It’s a tie between you and the algorithm 🏆🏆 - great minds think alike!"

    def display_message(text):
        is_tie = (text == tie_msg)
        if "—" in text:
            bold_part, regular_part = text.split("—", 1)
        elif "-" in text:
            bold_part, regular_part = text.split("-", 1)
        else:
            bold_part, regular_part = text, ""

        bold_font_size = "17px" if is_tie else "21px"
        html = f"""
         <div style="
             background: linear-gradient(135deg, #66ccff, #99ddff);
             border-radius: 10px;
             margin-top: 10px;
             margin-bottom: 10px;
             text-align: center;
             padding: 8px 3px;
         ">
             <div style="color: black; font-size: {bold_font_size}; font-weight: bold; margin-bottom: 6px;">
                 {bold_part.strip()}
             </div>
             <div style="color: black; font-size: 17px; line-height: 1.2;">
                 {regular_part.strip()}
             </div>
         </div>
         <div style="color: white; font-size: 14px; font-style: italic; margin-top: 0px; margin-bottom: 5px;">
         * Score calculated using accuracy
         </div>
         """
        st.markdown(html, unsafe_allow_html=True)

    if user_score[0] > alg_score[0]:
        display_message(user_win_msg)
    elif alg_score [0]> user_score[0]:
        display_message(algo_win_msg)
    else:
        display_message(tie_msg)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next!", key="next-btn", use_container_width=True):
            st.session_state.page = "thank_you"
            st.rerun()
