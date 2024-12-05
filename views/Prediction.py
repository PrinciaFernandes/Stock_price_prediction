import streamlit as st
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
import sklearn
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go

st.title("Stock Price Prediction")
st.text('')

bajaj = pd.read_csv(r"model_data/datasets/Bajaj.csv")
hdfc  = pd.read_csv(r"model_data/datasets/HDFC.csv")
Maruti = pd.read_csv(r"model_data/datasets/Maruti.csv")
reliance = pd.read_csv(r"model_data/datasets/Reliance.csv")
TATA = pd.read_csv(r"model_data/datasets/TATA.csv")

bajaj_model = tf.keras.models.load_model(rf"model_data/models/Bajaj/Bajaj_model.h5")
hdfc_model  = tf.keras.models.load_model(rf"model_data/models/HDFC/HDFC_model.h5")
Maruti_model = tf.keras.models.load_model(rf"model_data/models/Maruti/Maruti_model.h5")
reliance_model = tf.keras.models.load_model(rf"model_data/models/Reliance/Reliance_model.h5")
TATA_model = tf.keras.models.load_model(rf"model_data/models/TATA/TATA_model.h5")


def scaler_loader(name):
    with open(rf"model_data/models/{name}/{name}_scaler.pkl", 'rb') as f:
        scaler = pickle.load(f)
    return scaler

window_size = 60
def create_sequences(data, window_size):
    sequences = []
    sequences.append(data[0:0 + window_size])
    return np.array(sequences)

Dataset = {"Bajaj Finance Ltd.":bajaj,
            "HDFC Bank Ltd." : hdfc,
            "Maruti Suzuki India Ltd." : Maruti,
            "Reliance Industries Ltd." : reliance,
            "Tata Consultancy Services Ltd.": TATA}

models = {
    "Bajaj Finance Ltd.":[bajaj_model , scaler_loader("Bajaj")],
    "HDFC Bank Ltd." :[hdfc_model , scaler_loader("HDFC")],
    "Maruti Suzuki India Ltd." : [Maruti_model , scaler_loader("Maruti")],
    "Reliance Industries Ltd.": [reliance_model , scaler_loader("Reliance")],
    "Tata Consultancy Services Ltd." : [TATA_model, scaler_loader("TATA")]
}

comp = st.selectbox(" Select a Company",['Bajaj Finance Ltd.','HDFC Bank Ltd.','Maruti Suzuki India Ltd.','Reliance Industries Ltd.','Tata Consultancy Services Ltd.'],index = None)

if comp != None:
    model = models[comp][0]
    scaler = models[comp][1]

    dataset = Dataset[comp]

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.write("Prev. Close")
        prev_close = dataset['PREV. CLOSE '].iloc[-1]
        st.button(str(prev_close),key = 1)
    with col2:
        st.write("Open")
        open = dataset['OPEN '].iloc[-1]
        st.button(str(open),key = 2)
    with col3:
        st.write("High")
        high = dataset['HIGH '].iloc[-1]
        st.button(str(high),key = 3)
    with col4:
        st.write("Low")
        low = dataset['LOW '].iloc[-1]
        st.button(str(low),key = 4)
    with col5:
        st.write("VWAP")
        vwap = dataset['vwap '].iloc[-1]
        st.button(str(vwap),key = 5)
    st.write(" ")


    n = st.text_input("# Enter the no. of days you want to get the prediction",None)
    b = st.button(" Predict",use_container_width=True,key = 10)
    if n != None:
        n = int(n)
        
        if b:
            price = scaler.transform(dataset.iloc[:,6].values.reshape(-1,1))
            pred = [dataset.iloc[-1,6]]
            window_size = 60
            df = price[len(price) - window_size : ]
            d = pd.to_datetime(dataset.iloc[-1,0], format="%Y-%m-%d")
            date_ls = [str(d.date())]
            for i in range(n):
                sequence = create_sequences(df[-window_size:], window_size)[-1]
                sequence = sequence.reshape(1, window_size, 1)
                # Make the prediction
                prediction = model.predict(sequence)
                df = np.append(df.reshape(-1), prediction)
                prediction = scaler.inverse_transform(prediction)

                d += timedelta(days=1)
                date_ls.append(str(d.date()))
                pred.append(prediction[0][0])

            line1 = go.Scatter(x=dataset.iloc[-10:,0], y=dataset.iloc[-10:,6], mode='lines', name='Prev. data')

            # Create the line for y
            line2 = go.Scatter(x=date_ls, y=pred, mode='lines', name='Predicted data',line=dict(color='red'))

            # Create the figure and add both lines
            fig = go.Figure()
            fig.add_trace(line1)
            fig.add_trace(line2)

            fig.update_layout(title=f'Prediction of {n} days', xaxis_title='Close Price', yaxis_title='Days')
            st.plotly_chart(fig)


       



