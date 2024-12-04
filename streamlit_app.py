import streamlit as st

# st.title("Stock Price Prediction")
# st.sidebar.selectbox("Select a company",['Bajaj','HDFC','Maruti','Reliance','TATA'])

# st.date_input("Enter a date:")
# st.set_page_config(
#     page_title = "Stock Price page",
#     page_icon = ":material/attach_money:"
# )

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
