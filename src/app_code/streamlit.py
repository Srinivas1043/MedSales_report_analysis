import pandas as pd

df_analysis_ip_discount_report = pd.read_excel('../../data/final/Ip_Discount_Report_Final.xlsx')
df_train = df_analysis_ip_discount_report[['BILL DATE','BILLAMOUNT']]
df_train = df_train.rename(columns={"BILL DATE": "ds", "BILLAMOUNT": "y"})

# 
from neuralprophet import NeuralProphet
m = NeuralProphet()
m.fit(df_train, freq="D")

# forecasting 
future = m.make_future_dataframe(df_train, periods=30)
forecast = m.predict(future)
forecast = forecast.rename(columns={"ds": "BILL DATE", "yhat1": "BILLAMOUNT"})
forecast

import pickle
with open('neuralProphet.pkl', "wb") as f:
    pickle.dump(m, f)

import matplotlib.pyplot as plt
import streamlit as st
from datetime import date
import pandas as pd
from PIL import Image
import pickle

st.title('Discount Report Price Forecasting')
st.sidebar.title("About")
st.sidebar.info("Forecasting Billamount using 'NeuralProphet' Machine Learning model.")
def get_input():
	st.sidebar.header("Input From user")
	st.sidebar.subheader("Select range of Date for visualize data for particular date range.")
	st.sidebar.write("(From 07-03-2021 to 13-09-2021)")
	start_date = st.sidebar.text_input("Start Date", "07-03-2021")
	end_date = st.sidebar.text_input("End Date", "13-09-2021")
	st.write("")
	st.sidebar.subheader("Enter Period for Forecasting of Price")
	period = st.sidebar.text_input("Period (In Days)", "30")
	return start_date, end_date, period
START = "13-09-2015"
TODAY = date.today().strftime("%d-%M-%Y")


def get_data(start, end):
	df = pd.read_excel('../../data/final/Ip_Discount_Report_Final.xlsx')
	start = pd.to_datetime(start)
	end = pd.to_datetime(end)
	start_row = 0
	end_row = 0

	for i in range(0, len(df)):
		if start <=	pd.to_datetime(df['BILL DATE'][i]):
			start_row = i
			break
	for j in range(0, len(df)):
		if end >= pd.to_datetime(df['BILL DATE'][len(df)-1-j]):
			end_row = len(df) - 1 - j
			break

	df = df.set_index(pd.DatetimeIndex(df['BILL DATE'].values))
	return df.iloc[start_row:end_row+1, :]
start, end, period = get_input()
data = get_data(start, end)



def model_np():
	m = pickle.load(open('neuralProphet.pkl', 'rb'))
	st.subheader("Using NeuralProphet")
	df = data.copy()
	df.reset_index(inplace=True)
	df_train = df[['BILL DATE','BILLAMOUNT']]
	df_train = df_train.rename(columns={"BILL DATE": "ds", "BILLAMOUNT": "y"})
	future = m.make_future_dataframe(df_train, periods=int(period))
	forecast = m.predict(future)
	forecast = forecast.rename(columns={"ds": "BILL DATE", "yhat1": "BILLAMOUNT"})
	st.write("Forecasting billamount from 07-03-2021 to 13-09-2021")
	st.write(forecast[['BILL DATE', 'BILLAMOUNT']].head())
	st.write(f"Forecasting of Close Price of {period} days")
	st.line_chart(forecast['BILLAMOUNT'])
model_np()