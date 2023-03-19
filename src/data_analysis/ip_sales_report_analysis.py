import pandas as pd 
import streamlit as st
import plotly.express as px
df = pd.read_excel('../../data/final/Ip_Sales_Report_Final.xlsx')
st.title('SIMS Sales Report Dashboard')
st.subheader('Dataset')
st.dataframe(df)
st.subheader('Data Numerical Statistic')
st.dataframe(df.describe())
text_input = st.selectbox('Select Feature', df.columns)
st.subheader('Data Visualization')

num_feat = st.selectbox('Select Numerical Feature', df.select_dtypes('number').columns)
fig = px.histogram(df, x = num_feat, color = text_input)
st.plotly_chart(fig, use_container_width=True)

cat_feat = st.selectbox('Select Categorical Feature', df.select_dtypes(exclude ='number').columns)
fig = px.histogram(df, x =cat_feat, color = text_input )
st.plotly_chart(fig, use_container_width=True)      


num_feat_pie = st.selectbox('Select Numerical Feature for pie chart ', df.select_dtypes('number').columns)
cat_feat_pie = st.selectbox('Select Categorical Feature for pie chart ', df.select_dtypes(exclude ='number').columns)  
fig_pie = px.pie(df, values = num_feat_pie, names = cat_feat_pie,title = f'Pie Chart Visualization for{num_feat_pie} vs {cat_feat_pie}' )
st.plotly_chart(fig_pie,use_container_width = True)



