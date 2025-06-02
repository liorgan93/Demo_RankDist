import streamlit as st
import pandas as pd
from user_classification_intro import set_background


def compare_recommendations_page():
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

    total_matches = len(matching_songs)
    total_possible = max(len(user_songs), len(algorithm_songs))
    match_percentage = (total_matches / total_possible) * 100 if total_possible > 0 else 0

    max_length = max(len(matching_songs) + len(non_matching_user_songs), len(matching_songs) + len(non_matching_algorithm_songs))
    user_column = matching_songs + non_matching_user_songs + [""] * (max_length - len(matching_songs) - len(non_matching_user_songs))
    algorithm_column = matching_songs + non_matching_algorithm_songs + [""] * (max_length - len(matching_songs) - len(non_matching_algorithm_songs))

    real_top_k = ["Dancing Queen", "Imagine", "Hotel California"]
    real_top_k_column = real_top_k + [""] * (max_length - len(real_top_k))

    comparison_df = pd.DataFrame({
        "Your picks": user_column,
        "RankDist's output": algorithm_column,
        "True preference": real_top_k_column
    })

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 40px !important;
            padding-bottom: 0px !important;

        }
        }

        [data-testid="stAppViewContainer"] {
            width: 100vw;
            overflow-x: hidden;
            padding: 0;
        }

        .title-text {
            text-align: center;
            margin-top: 10px;
            margin-bottom: 28px;
            padding-top: 5px;
            font-size: 23px !important;
            font-weight: bold;
        }

        .success-text {
            color: #4CAF50;
            font-size: 17px;
            font-weight: bold;
            text-align: center;
        }

        .failure-text {
            color: #E53935;
            font-size: 17px;
            font-weight: bold;
            text-align: center;
        }
        .tie-text {
            color: ##2196F3;
            font-size: 17px;
            font-weight: bold;
            text-align: center;
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
    st.markdown(
        '<p class="title-text">Comparison and Evaluation</p>',unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.05, 0.9, 0.05])
    with col2:
        st.dataframe(comparison_df, hide_index=True, use_container_width=True, key="Next_button")

    if match_percentage > 50:
        st.markdown('<p class="success-text">The algorithm RankDist won! — look like it can mimic and even surpass human intuition</p>', unsafe_allow_html=True)
    else:
        if match_percentage < 50:
            st.markdown('<p class="success-text">The algorithm RankDist won! — look like it can mimic and even surpass human intuition</p>',unsafe_allow_html=True)
        else:
            st.markdown('<p class="tie-text">it’s a tie between you and the algorithm! - great minds think alike</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next!", key="next-btn", use_container_width=True):
            st.session_state.page = "thank_you"
            st.rerun()