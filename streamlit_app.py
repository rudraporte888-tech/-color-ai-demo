
import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(
    page_title="Color AI Demo",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Color Prediction AI Dashboard")
st.caption("Educational Demo | Statistical Analysis")

COLORS = ["Red", "Green", "Violet"]

if "history" not in st.session_state:
    st.session_state.history = []

# Result entry
st.subheader("Add Previous Result")

with st.form("result_form"):
    result = st.selectbox("Actual Result", COLORS)
    submitted = st.form_submit_button("Add Result")

    if submitted:
        st.session_state.history.append(result)
        st.success("Result added!")

# CSV restore
st.subheader("Import Previous History")
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded and st.button("Import CSV"):
    df = pd.read_csv(uploaded)

    if "Result" in df.columns:
        valid = df["Result"].astype(str).str.title()
        valid = valid[valid.isin(COLORS)].tolist()
        st.session_state.history = valid
        st.success("History imported!")
    else:
        st.error("CSV must contain a Result column.")

history = st.session_state.history

st.divider()

# Statistics
st.subheader("📊 Analysis")

if history:
    counts = Counter(history)
    total = len(history)

    # Add-one smoothing
    probabilities = {
        c: (counts[c] + 1) / (total + len(COLORS))
        for c in COLORS
    }

    best = max(probabilities, key=probabilities.get)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Results", total)
    c2.metric("Most Frequent", best)
    c3.metric("Top Estimated Frequency",
              f"{probabilities[best]*100:.1f}%")

    st.subheader("Estimated Color Distribution")

    chart = pd.DataFrame({
        "Color": COLORS,
        "Estimated Probability": [
            probabilities[c] * 100 for c in COLORS
        ]
    }).set_index("Color")

    st.bar_chart(chart)

    st.subheader("Experimental Next-Color Estimate")
    st.metric("Highest Historical Estimate", best)
    st.write({
        c: f"{probabilities[c]*100:.1f}%"
        for c in COLORS
    })

    st.caption(
        "These are smoothed historical frequencies, "
        "not reliable predictions of the next random result."
    )

    st.subheader("📜 Result History")

    history_df = pd.DataFrame({
        "Round": range(1, total + 1),
        "Result": history
    })

    st.dataframe(
        history_df.iloc[::-1],
        use_container_width=True
    )

    csv = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download History CSV",
        csv,
        "color_history.csv",
        "text/csv"
    )

    if st.button("Clear All History"):
        st.session_state.history = []
        st.rerun()

else:
    st.info("Add some results to start the analysis.")
    st.write("Your dashboard is waiting for data.")
