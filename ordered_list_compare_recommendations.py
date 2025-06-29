import streamlit as st
import pandas as pd
from user_classification_intro import set_background
from other_functions import render_progress_bar
import math


def calculate_score(predicted_items, true_items):
    true_relevances = {item: len(true_items) - idx for idx, item in enumerate(true_items)}
    dcg = 0.0
    for i, item in enumerate(predicted_items):
        rel = true_relevances.get(item, 0)
        dcg += rel / math.log2(i + 2)

    ideal_relevances = sorted(true_relevances.values(), reverse=True)
    idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal_relevances[:len(predicted_items)]))

    if idcg == 0:
        return 0.0, "0/0"
    ndcg = dcg / idcg
    return ndcg, f"{ndcg:.2f}"


def html_table(df):
    html = f"""
    <style>
        .dark-table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
            margin: 0 auto;
            font-family: 'Segoe UI', sans-serif;
            background-color: #0f111a;
            border: 1px solid #2b2d38;
            border-radius: 8px;
            overflow: hidden;
            color: #e6e8f1;
        }}

        .dark-table th {{
            background: linear-gradient(135deg, #29314f 0%, #1d243c 100%);
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 6px;
            border: none;
        }}

        .dark-table td {{
            background-color: #0f111a;
            font-size: 10px;
            font-weight: 600;
            padding: 6px 8px;
            border: 1px solid #2b2d38;
            overflow: hidden;
            white-space: nowrap;
        }}

        .dark-table th.row-num,
        .dark-table td.row-num {{
            width: 6%;
            text-align: center;
            background-color: #1a1d29;
            color: #9aa0b5;
            font-weight: 600;
        }}

        .dark-table tr:hover td {{
            background-color: #1a1d29;
        }}
    </style>

    <table class="dark-table">
        <thead>
            <tr>
                <th class="row-num">#</th>
    """

    # כותרות הנתונים
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    # שורות הטבלה + מספור
    for i, (_, row) in enumerate(df.iterrows(), start=1):
        html += "<tr>"
        html += f"<td class='row-num'>{i}</td>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html




def ordered_list_compare_recommendations_page():
    st.set_page_config(page_title="RankDist Demo")
    render_progress_bar("results")
    set_background("other images/blue background.jpg")

    selected_songs = st.session_state.user_choice
    persona_number = st.session_state.chosen_person_number
    cluster_file_path = f"alg_results/cluster_{persona_number}.csv"

    cluster_df = pd.read_csv(cluster_file_path)
    if 'ordered_list_results_alg' not in cluster_df.columns or 'ordered_list_results_true' not in cluster_df.columns:
        st.error("Error: The file must contain 'ordered_list_results_alg' and 'ordered_list_results_true' columns.")
        return

    user_songs = selected_songs
    algorithm_songs = cluster_df["ordered_list_results_alg"].dropna().tolist()
    true_preference = cluster_df["ordered_list_results_true"].dropna().tolist()

    max_length = max(len(user_songs), len(algorithm_songs), len(true_preference))

    def pad_list(lst, length):
        return lst + [""] * (length - len(lst))

    comparison_df = pd.DataFrame({
        "Your picks": pad_list(user_songs, max_length),
        "RankDist's output": pad_list(algorithm_songs, max_length),
        "True preference": pad_list(true_preference, max_length)
    })

    user_score = calculate_score(user_songs, true_preference)
    alg_score = calculate_score(algorithm_songs, true_preference)

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 5px !important;
            margin-top: 5px !important;
            margin-bottom: 0px: !important;
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
            margin-top: -20px; !important;
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

    col1, col2, col3 = st.columns([0.025, 0.95, 0.025])
    with col2:
        st.markdown(html_table(comparison_df), unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; font-size:17px; margin-top:-5px !important;'>🧍<b>Your Score:</b> {user_score[1]} &nbsp;&nbsp;&nbsp;🤖<b>RankDist Score:</b> {alg_score[1]}</div>", unsafe_allow_html=True)

    user_win_msg = "You won 🏆 — your intuition beat the algorithm!"
    algo_win_msg = "The RankDist algorithm won 🏆 — looks like it can mimic and even surpass human intuition!"
    tie_msg = "You and the algorithm tied 🏆🏆 - great minds think alike!"

    def display_message(text):
        is_tie = (text == tie_msg)
        if "—" in text:
            bold_part, regular_part = text.split("—", 1)
        elif "-" in text:
            bold_part, regular_part = text.split("-", 1)
        else:
            bold_part, regular_part = text, ""

        bold_font_size = "18px" if is_tie else "21px"
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
         <div style="color: white; font-size: 13px; font-style: italic; margin-top: 0px; margin-bottom: 5px; line-height: 1.1;">
         * RankDist algorithm optimized DCG in expectation <br>
         * Score calculated using nDCG for convenience
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
            st.empty()
            st.rerun()
