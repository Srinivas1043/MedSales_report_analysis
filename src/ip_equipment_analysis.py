import pandas as pd 
# EXPLORATORY DATA ANALYSIS 

import streamlit as st
import plotly.express as px
df = pd.read_excel('../data/final/Ip_Equipment_Final.xlsx')
st.title('SIMS Equipments Attrition  Dashboard')
st.subheader('Dataset')
st.dataframe(df)
st.subheader('Data Numerical Statistic')
st.dataframe(df.describe())
st.subheader('Data Visualization')
# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

left_column, right_column = st.columns(2)
text_input = st.selectbox('Select Feature', df.columns)

with left_column:
    num_feat = st.selectbox('Select Numerical Feature', df.select_dtypes('number').columns)
    fig = px.histogram(df, x = num_feat, color = text_input)
    st.plotly_chart(fig, use_container_width=True)

with right_column:

    cat_feat = st.selectbox(
    'Select Categorical Feature', df.select_dtypes(exclude ='number').columns)
    fig = px.histogram(df, x =cat_feat, color = text_input )

st.plotly_chart(fig, use_container_width=True)

