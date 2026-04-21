import streamlit as st
import pandas as pd

st.title("📈 Stock Price Prediction")

# Load data
data = pd.read_csv("aapl.csv")   # <-- rename file
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
data.set_index('Date', inplace=True)

close = data['Close']

# Input
steps = st.number_input("Enter number of days", 1, 30, 5)

# Prediction
if st.button("Predict"):
    returns = close.pct_change().dropna()
    avg_return = returns.mean()

    last_value = close.iloc[-1]
    forecast = []

    for i in range(steps):
        next_value = last_value * (1 + avg_return)
        forecast.append(next_value)
        last_value = next_value

    future_dates = pd.date_range(start=close.index[-1], periods=steps+1, freq='B')[1:]
    forecast_series = pd.Series(forecast, index=future_dates)

    st.subheader("Predicted Prices")
    st.write(forecast_series)

    st.subheader("Chart")
    st.line_chart(pd.concat([close.tail(50), forecast_series]))
