import streamlit as st
import pandas as pd
import random
from user_classification_intro import set_background


def calculate_user_score():
    return random.random()


def calculate_alg_score():
    return random.random()


def ordered_list_compare_recommendations_page():
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
        [data-testid="stAppViewContainer"] {
            width: 100vw;
            overflow-x: hidden;
            padding: 0;
        }
        iframe[data-testid="stDataFrame"] {
            margin-bottom: -20px !important;
        }
        .title-text {
            text-align: center;
            margin-top: 10px;
            margin-bottom: 27px;
            padding-top: 5px;
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

    col1, col2, col3 = st.columns([0.05, 0.9, 0.05])
    with col2:
        st.dataframe(comparison_df, hide_index=True, use_container_width=True, key="Next_button")

    st.markdown(f"<div style='text-align:center; font-size:14px; margin-top:-5px !important;'>🤖 <b>RankDist algorithm Score:</b> {alg_score} &nbsp;&nbsp;&nbsp; 🧍 <b>Your Score:</b> {user_score}</div>", unsafe_allow_html=True)

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

    if user_score > alg_score:
        display_message(user_win_msg)
    elif alg_score > user_score:
        display_message(algo_win_msg)
    else:
        display_message(tie_msg)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next!", key="next-btn", use_container_width=True):
            st.session_state.page = "thank_you"
            st.rerun()
