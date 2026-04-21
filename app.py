import streamlit as st
import pandas as pd
import pickle

st.title("📈 Stock Price Prediction (SARIMAX)")

# Load data
data = pd.read_csv("aapl.csv")
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
data.set_index('Date', inplace=True)

close = data['Close']

# Load model
model = pickle.load(open("sarimax_model.pkl", "rb"))

# Input
steps = st.number_input("Enter number of days", 1, 30, 5)

if st.button("Predict"):

    forecast = model.forecast(steps=steps)

    future_dates = pd.date_range(start=close.index[-1], periods=steps+1, freq='B')[1:]
    forecast_series = pd.Series(forecast.values, index=future_dates)

    st.subheader("Predicted Prices")
    st.write(forecast_series)

    st.subheader("Chart")
    st.line_chart(pd.concat([close.tail(50), forecast_series]))