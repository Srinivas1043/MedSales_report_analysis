import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px


# define app and server
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],suppress_callback_exceptions=True)
server = app.server

# define sidebar
sidebar = html.Div(
    [
        html.H2("SIMS Data", className="display-4"),
        html.Hr(),
        dbc.Nav
        (
    
            [
                dbc.NavLink("Home", href="/", active="exact"),
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


def ip_discount_pie_chart():
    return px.pie(ip_discount_report_df,values='TOTAL AMOUNT',names = 'INSURANCE NAME')

def ip_discount_bar():
    return px.bar(ip_discount_report_df,x='INSURANCE NAME',y='DISCOUNT')

def ip_scatter_total_discount():
    return px.scatter(ip_discount_report_df,x='TOTAL AMOUNT',y='DISCOUNT',color = 'INSURANCE NAME')
@callback(
    Output('discount-graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = ip_discount_report_df[ip_discount_report_df['INSURANCE NAME']==value]
    return px.line(dff, x='BILL DATE', y='DISCOUNT')



ip_discount_report = html.Div([
    html.H1("IP Discount Report"),
    html.Br(),
    # insert code for IP Discount Report final visualization here
    html.H3("Insurance Company Name"),
    html.P('To visualise the discount given by each insurance company with regards to date'),
    dcc.Dropdown(ip_discount_report_df['INSURANCE NAME'].unique(), 'Insurance Name', id='dropdown-selection'),
    dcc.Graph(id='discount-graph-content'),

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
def admit_discharge_date_bill_amount_analysis():
    ip_sales_details_df['duration'] = ip_sales_details_df['dischargedatetime'] -ip_sales_details_df['admitdatetime']
    ip_sales_details_df['numberofdays'] = ip_sales_details_df['duration'].apply(pd.to_timedelta).dt.days
    return px.scatter(ip_sales_details_df, x='numberofdays', y='billamount', color="Company", hover_name="Specialisation", size='numberofdays')

def ip_netamt_specialisation_bar():
    return px.bar(ip_sales_details_df,y= 'Specialisation',x='netamount',color ='category')

def ip_netamt_cat_bar():
    return px.bar(ip_sales_details_df,y= 'category',x='netamount',color ='Specialisation')

def ip_net_amt_company_bar():
    return px.bar(ip_sales_details_df,y = 'Company',x='netamount',color ='Area')

def ip_package_fees_specialisation_bar():
    return px.bar(ip_sales_details_df,y='Specialisation',x='PackageFees',color ='category')

def ip_package_fees_cat_bar():
    return px.bar(ip_sales_details_df,y='category',x='PackageFees',color ='Specialisation')

def ip_package_fees_company_bar():
    return px.bar(ip_sales_details_df,y ='Company',x='PackageFees',color ='Area')


ip_sales_details = html.Div([
    html.H1("IP Sales Details"),
    html.Br(),
    # insert code for IP Sales Details visualization here
    dcc.Graph(id='discharge-difference', figure=admit_discharge_date_bill_amount_analysis()),
    dcc.Graph(id='ip_netamount_specialisation', figure=ip_netamt_specialisation_bar()),
    dcc.Graph(id='ip_netamount_category', figure=ip_netamt_cat_bar()),
    dcc.Graph(id='ip_netamount_company', figure=ip_net_amt_company_bar()),
    dcc.Graph(id='ip_packagefees_specialisation', figure=ip_package_fees_specialisation_bar()),
    dcc.Graph(id='ip_packagefees_category', figure=ip_package_fees_cat_bar()),
    dcc.Graph(id='ip_packagefees_company', figure=ip_package_fees_company_bar()),
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
# define page content for IP Sales Summary Report sheet
ip_sales_summary_df = pd.read_excel('data/final/Ip_Sales_Summary_Report_Final.xlsx')

def admit_discharge_room_rent_analysis():
    ip_sales_summary_df['duration'] = ip_sales_summary_df['DischargeDatetime'] - ip_sales_summary_df['AdmitDatetime']
    ip_sales_summary_df['numberofdays'] = ip_sales_summary_df['duration'].apply(pd.to_timedelta).dt.days
    return px.scatter(ip_sales_summary_df, x='numberofdays', y='Room Rent', color="Diagnosis", hover_name="Category", size='Bill Amount')


def ip_pharm_diagnosis_bar():
    return px.bar(ip_sales_summary_df,y ='Diagnosis',x='Pharmacy',color ='State')

def ip_docfees_surgerydept_bar():
    return px.bar(ip_sales_summary_df,y ='SURGERYTYPE',x='Doctor Fees',color ='Country')

def ip_food_beverages_pie_chart():
    return px.bar(ip_sales_summary_df,x='Food and Beverages',y = 'Company', color='Test')

ip_sales_summary_report = html.Div([
    html.H1("IP Sales Summary Report"),
    html.Br(),
    # insert code for IP Sales Summary Report visualization here
    dcc.Graph(id='admit_discharge_room_rent_analysis', figure=admit_discharge_room_rent_analysis()),
    dcc.Graph(id='ip_pharm_diagnosis_bar', figure=ip_pharm_diagnosis_bar()),
    dcc.Graph(id='ip_docfees_surgerydept_bar', figure=ip_docfees_surgerydept_bar()),
    dcc.Graph(id='ip_food_beverages_pie_chart', figure=ip_food_beverages_pie_chart()),
])




# define page content for SIMS Dashboard sheet

cards = dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Sales Detail Analysis", className="card-title"),
                    html.P(f"There are {len(ip_sales_details_df)} rows"),
                    dbc.Button("Go to Page 1", color="primary", href="/ip_sales_details"),
                ]
            ),
            className="mb-3",
            style={
                'background-image': 'url("https://www.absolutdata.com/wp-content/uploads/2022/06/Is-Dark-Data-the-Key-to-Transforming-Your-Business-blog.jpg")',
                'background-size': 'cover',
                'background-position': 'center',
                'color': 'white'
            }
        ),
        width=6,
        md={'size': 6, 'offset': 0}
    ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Discount Report Analysis", className="card-title"),
                    html.P(f"There are {len(ip_discount_report_df)} rows"),
                    dbc.Button("Go to Page 2", color="primary", href="/ip_discount_report"),
                ]
            ),
            className="mb-3",
            style={
                'background-image': 'url("https://www.absolutdata.com/wp-content/uploads/2022/06/Is-Dark-Data-the-Key-to-Transforming-Your-Business-blog.jpg")',
                'background-size': 'cover',
                'background-position': 'center',
                'color': 'white'
            }
        ),
        width=6,
        md={'size': 6, 'offset': 0}
    ),
], className="mb-4")

dashboard_home = html.Div([
    html.H1("Welcome to SIMS Dashboard"),
    html.Br(),
    # insert code for IP Equipment Details visualization here
    cards
], className="container")




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
    elif pathname == "/":
        return dashboard_home
    else:
        return html.H1("404 - Page Not Found")
if __name__ == "__main__":
    app.run_server(debug=True)
