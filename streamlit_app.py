import streamlit as st

hide_github_icon_style = """
<style>
.stGithubIcon { display: none; }
</style>
"""
st.markdown(hide_github_icon_style, unsafe_allow_html=True)


dashboard_page = st.Page(
    page = "views/Dashboard.py",
    title = "Dashboards",
    icon = ":material/bar_chart:",
    default = True,
)

prediciton_page = st.Page(
    page = "views/Prediction.py",
    title = "Prediction",
    icon = ":material/batch_prediction:"
)

st.logo("assets/nifty 50.png")

pg = st.navigation(pages = [dashboard_page,prediciton_page])
pg.run()

