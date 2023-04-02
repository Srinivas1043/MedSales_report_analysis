import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

# define app and server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

# define sidebar
sidebar = html.Div(
    [
        html.H2("SIMS Data", className="display-4"),
        html.Hr(),
        dbc.Nav
        (
    
            [
                dbc.NavLink("IP Discount Report", href="/ip_discount_report", active="exact"),
                dbc.NavLink("Equipment - IP Sales Detail", href="/equipment_ip_sales_detail", active="exact"),
                dbc.NavLink("IP Sales Details",href="/ip_sales_details", active="exact"),
                dbc.NavLink("IP Sales Report", href="/ip_sales_report", active="exact"),
                dbc.NavLink("IP Sales Summary Report",href="/ip_sales_summary_report", active="exact")
            ],vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "20rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    },
)
# define content area
content = html.Div(id="page-content", style={"margin-left": "22rem", "margin-right": "2rem"})

# define app layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
# define callback to toggle sidebar
@app.callback(
    [dash.dependencies.Output("sidebar", "style"), dash.dependencies.Output("page-content", "style")],
    [dash.dependencies.Input("toggle-sidebar", "n_clicks")],
    [dash.dependencies.State("sidebar", "style"), dash.dependencies.State("page-content", "style")],
)
def toggle_sidebar(n_clicks, sidebar_style, content_style):
    if n_clicks is None:
        return sidebar_style, content_style
    if sidebar_style.get("margin-left") == "0px":
        sidebar_style["margin-left"] = "-20rem"
        content_style["margin-left"] = "2rem"
    else:
        sidebar_style["margin-left"] = "0px"
        content_style["margin-left"] = "22rem"
    return sidebar_style, content_style

# define page content for IP Discount Report Final sheet
ip_discount_report_df =pd.read_excel('data/final/Ip_Discount_Report_Final.xlsx')

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = ip_discount_report_df[ip_discount_report_df['INSURANCE NAME']==value]
    return px.line(dff, x='BILL DATE', y='DISCOUNT')

def ip_discount_pie_chart():
    return px.pie(ip_discount_report_df,values='TOTAL AMOUNT',names = 'INSURANCE NAME')

def ip_discount_bar():
    return px.bar(ip_discount_report_df,x='INSURANCE NAME',y='DISCOUNT')

def ip_scatter_total_discount():
    return px.scatter(ip_discount_report_df,x='TOTAL AMOUNT',y='DISCOUNT',color = 'INSURANCE NAME')
ip_discount_report = html.Div
([
    html.H1("IP Discount Report"),
    html.Br(),
    # insert code for IP Discount Report final visualization here
    html.H3("Insurance Company Name"),
    html.P('To visualise the discount given by each insurance company with regards to date'),
    dcc.Dropdown(ip_discount_report_df['INSURANCE NAME'].unique(), 'Insurance Name', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    html.H4('Total Amount vs Insurance company '),
    html.P('To explore the contribution of each insurance company to attain total amount'),
    dcc.Graph(id='ip_pie-chart',figure = ip_discount_pie_chart()),
    html.H5('Discount VS Insurance Company'),
    html.P('To get information about the discount value provided by each insurance company'),
    dcc.Graph(id ='ip_bar-chart',figure= ip_discount_bar()),
    html.H6('Total Amount vs Discount'),
    html.P('The discount provided to total amount for each patient by insurance company is visualized here'),
    dcc.Graph(id='ip_scatter_total_discount',figure=ip_scatter_total_discount()) 
])


# define page content for Equipment - IP Sales Detail sheet
ip_equipment_df =pd.read_excel('data/final/Ip_Equipment_Final.xlsx')
equipment_ip_sales_detail = html.Div([
    html.H1("Equipment - IP Sales Detail"),
    html.Br(),
    # insert code for Equipment - IP Sales Detail visualization here
])

# define page content for IP Sales Details sheet
ip_sales_details_df = pd.read_excel('data/final/Ip_Sales_Details_Final.xlsx')
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = ip_discount_report_df[ip_discount_report_df['INSURANCE NAME']==value]
    return px.line(dff, x='BILL DATE', y='DISCOUNT')
ip_sales_details = html.Div([
    html.H1("IP Sales Details"),
    html.Br(),
    # insert code for IP Sales Details visualization here
])


# define page content for IP Sales Report sheet
ip_sales_report_df = pd.read_excel('data/final/Ip_Sales_Report_Final.xlsx')
ip_sales_report = html.Div([
    html.H1("IP Sales Report"),
    html.Br(),
    # insert code for IP Sales Report visualization here 
dcc.Graph(
        id="ip-sales-chart",
        figure={
            "data": [
                {
                    "x": ip_sales_report_df['SPECIALISATION'],
                    "y": ip_sales_report_df['BILL AMOUNT'],
                    "type": "bar",
                }
            ],
            "layout": {
                "title": "IP Sales Report by Product",
                "xaxis": {"title": "Product"},
                "yaxis": {"title": "Sales"},
            },
        },
    ),
])

# define page content for IP Sales Summary Report sheet
ip_sales_summary_df = pd.read_excel('data/final/Ip_Sales_Summary_Report_Final.xlsx')
ip_sales_summary_report = html.Div([
    html.H1("IP Sales Summary Report"),
    html.Br(),
    # insert code for IP Sales Summary Report visualization here
])


# define callback to display page content based on URL
@app.callback(dash.dependencies.Output("page-content", "children"), [dash.dependencies.Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/ip_discount_report":
        return ip_discount_report 
    elif pathname == "/equipment_ip_sales_detail":
        return equipment_ip_sales_detail
    elif pathname == "/ip_sales_details":
        return ip_sales_details
    elif pathname =="/ip_sales_report":
        return ip_sales_report
    elif pathname == "/ip_sales_summary_report":
        return ip_sales_summary_report
    else:
        return html.H1("404 - Page Not Found")
if __name__ == "__main__":
    app.run_server(debug=True)

