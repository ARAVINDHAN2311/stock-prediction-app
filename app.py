import streamlit as st
import pandas as pd
import pickle

st.title("📈 Stock Price Prediction")

# Load data
data = pd.read_csv("aapl.csv")

# Convert date safely
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data.set_index('Date', inplace=True)

close = data['Close']

# Load model safely
try:
    model = pickle.load(open("sarimax_model.pkl", "rb"))
    st.success("Model loaded successfully")
except Exception as e:
    st.error(f"Model loading error: {e}")

# Input
steps = st.number_input("Enter number of days", 1, 30, 5)

# Predict
if st.button("Predict"):
    try:
        forecast = model.forecast(steps=int(steps))

        future_dates = pd.date_range(start=close.index[-1], periods=steps+1, freq='B')[1:]
        forecast_series = pd.Series(forecast, index=future_dates)

        st.subheader("Predicted Prices")
        st.write(forecast_series)

        st.subheader("Chart")
        st.line_chart(pd.concat([close.tail(50), forecast_series]))

    except Exception as e:
        st.error(f"Prediction error: {e}")