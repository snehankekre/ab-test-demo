import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="A/B Test Comparison",
    page_icon="📈",
    initial_sidebar_state="expanded",
)


@st.cache
def load_data():
    group = ["Control", "Treatment"]
    conversion = [16, 48]
    return pd.DataFrame({"Group": group, "Conversion": conversion})


@st.cache(allow_output_mutation=True)
def plot_chart(df):
    chart = (
        alt.Chart(df)
        .mark_bar(color="green")
        .encode(
            x=alt.X("Group:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Conversion:Q", title="Conversion rate (%)"),
            opacity="Group:O",
        )
        .properties(width=400, height=500)
    )

    chart_text = chart.mark_text(
        align="center", baseline="middle", dy=-10, color="black"
    ).encode(text="Conversion:Q")

    final = chart + chart_text
    return final


st.title("A/B Test Comparison")

with st.sidebar.form("parameters"):
    experiment = st.selectbox("Select experiment:", options=["1", "2", "3"])
    alpha = st.slider(
        "Significance threshold (α):",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01,
        help="The probability of the test rejecting the null hypothesis, given that the null hypothesis is assumed to be true",
    )
    hypothesis = st.radio("Hypothesis type:", options=["One-sided", "Two-sided"])
    confirm = st.form_submit_button("Confirm")

col1, col2, _ = st.beta_columns(3)

with col1:
    st.header("Delta")
    delta = '<p style="font-family:sans-serif; font-size: 40px;"><b>125%</b></p>'
    st.markdown(delta, unsafe_allow_html=True)

with col2:
    st.header("Significant?")
    significant = '<p style="font-family:sans-serif; color:Green; font-size: 40px;"><b>YES</b></p>'
    st.markdown(significant, unsafe_allow_html=True)


df = load_data()
bar_chart = plot_chart(df)
st.altair_chart(bar_chart)

st.markdown(
    """
|           | Converted | Total | Conversion Rate | p-value |
| :---:     |  :----:   | :---: | :---:           | :---:   |
| Control   | 50        | 300   |  16%            | 0.01    |
| Treatment | 48        | 100   |  48%            |         |
"""
)
