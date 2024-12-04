import streamlit as st



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
