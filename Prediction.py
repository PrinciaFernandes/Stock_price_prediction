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

bajaj = pd.read_csv(r"C:\Users\Princia\Stock price prediction\model_data\preprocessed_data\Bajaj.csv")
hdfc  = pd.read_csv(r"C:\Users\Princia\Stock price prediction\model_data\preprocessed_data\HDFC.csv")
Maruti = pd.read_csv(r"C:\Users\Princia\Stock price prediction\model_data\preprocessed_data\Maruti.csv")
reliance = pd.read_csv(r"C:\Users\Princia\Stock price prediction\model_data\preprocessed_data\reliance.csv")
TATA = pd.read_csv(r"C:\Users\Princia\Stock price prediction\model_data\preprocessed_data\TATA.csv")


def model_loader(name):
    model = tf.keras.models.load_model(rf"C:\Users\Princia\Stock price prediction\model_data\models\models\{name}\{name}_model.h5")
    return model

def scaler_loader(name):
    with open(rf"C:\Users\Princia\Stock price prediction\model_data\models\models\{name}\{name}_scaler.pkl", 'rb') as f:
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
    "Bajaj Finance Ltd.":[model_loader("Bajaj") , scaler_loader("Bajaj")],
    "HDFC Bank Ltd." :[model_loader("HDFC") , scaler_loader("HDFC")],
    "Maruti Suzuki India Ltd." : [model_loader("Maruti") , scaler_loader("Maruti")],
    "Reliance Industries Ltd.": [model_loader("Reliance") , scaler_loader("Reliance")],
    "Tata Consultancy Services Ltd." : [model_loader("TATA") , scaler_loader("TATA")]
}

comp = st.selectbox("Select a Company",['Bajaj Finance Ltd.','HDFC Bank Ltd.','Maruti Suzuki India Ltd.','Reliance Industries Ltd.','Tata Consultancy Services Ltd.'],index = None)

if comp != None:
    model = models[comp][0]
    scaler = models[comp][1]


    n = st.text_input("Enter the no. of days you want to get the prediction",None)
    if n != None:
        n = int(n)
        print(type(n))

        df = Dataset[comp]


        dataset = pd.read_csv(rf"C:\Users\Princia\Stock price prediction\datasets_stocks\{comp}.csv")
        # if days :
        #     while(date not in dataset['Date '].values):          
        #         date = str(pd.to_datetime(date, format= "%Y-%m-%d").date() - timedelta(days=1))
        
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
        
        
        if st.button(" Predict",use_container_width=True):
            price = scaler.transform(dataset.iloc[:,7].values.reshape(-1,1))
            pred = [dataset.iloc[-1,7]]
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

            line1 = go.Scatter(x=dataset.iloc[-10:,0], y=dataset.iloc[-10:,7], mode='lines', name='Prev. data')

            # Create the line for y
            line2 = go.Scatter(x=date_ls, y=pred, mode='lines', name='Predicted data',line=dict(color='red'))

            # Create the figure and add both lines
            fig = go.Figure()
            fig.add_trace(line1)
            fig.add_trace(line2)

            fig.update_layout(title=f'Prediction of {n} days', xaxis_title='Close Price', yaxis_title='Days')
            st.plotly_chart(fig)


       



