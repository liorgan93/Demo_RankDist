import streamlit as st

def research_page():
    persona_name = st.session_state.persona
    page_style = """
    <style>
    [data-testid="stApp"] {
        background-color: #1e3a5f; /* כחול כהה */
        color: white; /* טקסט לבן */
    }
    h1 {
        font-size: 24px;
        text-align: center;
        color: white;
    }
    h2, h3, h4 {
        font-size: 18px;
        color: white;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 14px;
        margin-bottom: 4px;
        color: white;
    }
    .stSlider > div {
        padding-top: 0px;
        padding-bottom: 0px;
    }
    .stRadio > div {
        padding-top: 0px;
        padding-bottom: 0px;
    }
    button[kind="primary"] {
        background-color: black;
        color: white;
        border: 1px solid white;
        font-size: 16px;
        padding: 0.5em 1em;
    }
    </style>
    """
    st.markdown(page_style, unsafe_allow_html=True)

    st.title(f"After listening to {persona_name} music, please answer a few questions")

    # Question 1
    st.subheader("🎧 Question 1 – Overall Connection")
    st.markdown("To what extent did you feel connected to the music that was played for you?  \n*Scale:* 1️⃣ (Not at all) – 5️⃣ (Very much)")
    q1 = st.slider(
        label="",
        min_value=1,
        max_value=5,
        format="%d",
        key="slider1"
    )

    st.markdown("---")

    # Question 2
    st.subheader("🎵 Question 2 – Match to Personal Taste")
    st.markdown("To what extent do you feel the music matched your personal musical taste?  \n*Scale:* 1️⃣ (Very different) – 5️⃣ (Very similar)")
    q2 = st.slider(
        label="",
        min_value=1,
        max_value=5,
        format="%d",
        key="slider2"
    )

    st.markdown("---")

    # Question 3
    st.subheader("🎶 Question 3 – Would You Choose It Yourself?")
    st.markdown("If you were choosing music on your own, would you choose to listen to these songs?  \n*Answer options:* ✅ Yes / ❌ No")
    q3 = st.radio(
        label="",
        options=["✅ Yes", "❌ No"],
        horizontal=True,
        key="radio1"
    )

    st.markdown("---")

    if st.button("Submit"):
        st.session_state.page = "thank_you_research"
        st.rerun()

