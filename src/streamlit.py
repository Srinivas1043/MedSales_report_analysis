import streamlit as st
import plotly.express as px
from app_code import *

st.set_page_config(page_title = "SIMS", page_icon="⚡")

st.title("SIMS DATA ANALYSIS⚡")
st.markdown('#### Forecasting sales data ')
#read file
df = pd.read_excel("../data/final/Ip_Discount_Report_Final.xlsx")

#Creating the sidebar menu 
container_cat = st.sidebar.container()

select_model = st.sidebar.selectbox("Select a Forecasting Model",   
                                 options = models.keys())       

forecast_horizon = st.sidebar.slider(label = 'Forecast Horizon (hours)',
                                     min_value = 12, max_value = 168, value = 24)         


df['BILL DATE'] = pd.to_datetime(df['BILL DATE'],infer_datetime_format=True)

print(df.dtypes)
fig = px.area(df, x = df['BILL DATE'], y = df['TOTAL AMOUNT'], color_discrete_sequence=px.colors.qualitative.Prism)
fig.update_traces(line=dict(width=0.25))
fig.update_layout(height = 450, margin={"r":1,"t":10,"l":1,"b":1},
                  yaxis=dict(showgrid=False),
                  plot_bgcolor = '#FFFFFF', title = "",
                  legend = dict(orientation = 'h', title = ''),
                  yaxis_title='', xaxis_title='')

st.plotly_chart(fig, use_container_width = True)
cols_insurance = ['TOTAL AMOUNT','DEPOSIT']
df = df[df.columns & cols_insurance]
with container_cat:
        insurance_cat = st.selectbox(label = 'Select any column to visualise', options = df.columns)   

st.markdown(f'#### {insurance_cat} Electricity Generation Forecast in {cols_insurance} (MW)')

#Generating and plotting a forecast for the selected category
forecast_results = get_forecast_results(df[insurance_cat].to_frame(),models[select_model], forecast_horizon)
          
st.markdown('Result for test set and specified forecast horizon')                   
st.plotly_chart(forecast_results['forecast_fig'], use_container_width = True)
st.dataframe(forecast_results['metrics'].style.format(precision = 3))

with st.expander('Display More Plots'):
        # st.markdown('#### Seasonal Decomposition Plot')
        # st.plotly_chart(forecast_results['decomp_fig'], use_container_width = True)
        
        st.markdown('#### ACF Plot')
        st.plotly_chart(forecast_results['acf_fig'], use_container_width = True)

        if forecast_results['diag_fig'] != None:
                diag_fig = forecast_results['diag_fig']
                diag_fig.update_layout(height = 600,
                margin={"r":1,"t":19,"l":1,"b":1},
                plot_bgcolor = '#FFFFFF', title = '')

                st.markdown('#### Diagnostics Plot')
                st.plotly_chart(forecast_results['diag_fig'], use_container_width = True)