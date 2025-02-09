import streamlit as st
import pandas as pd
import plotly.express as px 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")


# st.set_page_config(
#      page_title = "Stock Price Page",
#      page_icon= "💲"
# )

bajaj = pd.read_csv(r"model_data/datasets/Bajaj.csv")
hdfc  = pd.read_csv(r"model_data/datasets/HDFC.csv")
Maruti = pd.read_csv(r"model_data/datasets/Maruti.csv")
reliance = pd.read_csv(r"model_data/datasets/Reliance.csv")
TATA = pd.read_csv(r"model_data/datasets/TATA.csv")


Dataset = {"Bajaj Finance Ltd.":bajaj,
            "HDFC Bank Ltd." : hdfc,
            "Maruti Suzuki India Ltd." : Maruti,
            "Reliance Industries Ltd." : reliance,
            "Tata Consultancy Services Ltd.": TATA}

st.title("Stock Price Dashboard")
comp = st.selectbox("Select a Company",['Bajaj Finance Ltd.','HDFC Bank Ltd.','Maruti Suzuki India Ltd.','Reliance Industries Ltd.','Tata Consultancy Services Ltd.'],index = None)

if comp:
    data = Dataset[comp]
    data.sort_values(by = 'Date ')

    st.subheader('Closing Price Over Time')
    fig = px.line(data, x='Date ', y='close ')
    st.plotly_chart(fig)
    st.write("")

    st.subheader('Volume of Trades Over Time')
    fig = px.bar(data, data['Date '], data['VOLUME '],color = 'VOLUME ')
    st.plotly_chart(fig)
    st.write('')

    st.subheader('Distribution of Closing Prices')
    fig = px.histogram(data, x='close ', nbins =50,  hover_data=data.columns )
    fig.update_layout(bargap = 0.2 ,width=1000, height=400)
    st.plotly_chart(fig)

    st.subheader('High and Low Prices Over Time')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['HIGH '], mode='lines', name='High Price', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=data.index, y=data['LOW '], mode='lines', name='Low Price', line=dict(color='red')))
    fig.update_layout(title='', xaxis_title='Date', yaxis_title='Price', title_font_size=24, xaxis_title_font_size=18, yaxis_title_font_size=18)
    st.plotly_chart(fig)

    st.subheader('Candlestick Chart')
    fig = go.Figure(data=[go.Candlestick(x=data['Date '],
                                        open=data['OPEN '],
                                        high=data['HIGH '],
                                        low=data['LOW '],
                                        close=data['close '],
                                        name='Candlestick')])

    fig.update_layout(title='', xaxis_title='Date ', yaxis_title='Price ')
    st.plotly_chart(fig)
