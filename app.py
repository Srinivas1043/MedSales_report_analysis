import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import html, dcc, callback, Output, Input
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
                dbc.NavLink("Equipment - IP Details Final", href="/ip_equipment_details_final", active="exact"),
                dbc.NavLink("Equipment - IP Sales Final", href="/ip_equipment_sales_final", active="exact"),
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
    """Toggle the visibility of a sidebar and adjust the margins of the content accordingly.

    Parameters:
        n_clicks (int or None): The number of times the toggle button has been clicked.
        sidebar_style (dict): A dictionary of CSS styles for the sidebar element, including its current margin-left value.
        content_style (dict): A dictionary of CSS styles for the content element, including its current margin-left value.

    Returns:
        tuple: A tuple of two dictionaries containing the updated CSS styles for the sidebar and content elements, respectively.
    """
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
    """ This function returns a pie chart 
    visualization using Plotly Express 
    (px.pie()) of the total amount of 
    discount provided by each insurance name in 
    the ip_discount_report_df dataframe.    """
    return px.pie(ip_discount_report_df,values='TOTAL AMOUNT',names = 'INSURANCE NAME')

def ip_discount_bar():
    """This function returns a bar chart visualization using Plotly Express (px.bar()) of the 
    discount provided by each insurance name in the ip_discount_report_df dataframe."""
    
    return px.bar(ip_discount_report_df,x='INSURANCE NAME',y='DISCOUNT')

def ip_scatter_total_discount():
    """This function returns a scatter plot visualization using 
    Plotly Express (px.scatter()) of the relationship between 
    the total amount and discount provided by each insurance 
    name in the ip_discount_report_df dataframe, 
    with each insurance name represented by a different color.    """
    
    return px.scatter(ip_discount_report_df,x='TOTAL AMOUNT',y='DISCOUNT',color = 'INSURANCE NAME')

@callback(
    Output('discount-graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    """
    Update the line chart based on the selected insurance name value.

    Args:
        value (str): The selected value from the insurance name dropdown.

    Returns:
        plotly.graph_objs._figure.Figure: A line chart showing the discount amounts
        for the selected insurance name over time.
    """
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


# define page content for IP Sales Details sheet
ip_sales_details_df = pd.read_excel('data/final/Ip_Sales_Details_Final.xlsx')
def admit_discharge_date_bill_amount_analysis():
    """
    Creates a scatter plot of bill amount versus number of days of hospitalization, colored by company and with specialization shown on hover.
    The function calculates the number of days of hospitalization for each record in the ip_sales_details_df DataFrame by subtracting the admitdatetime from the dischargedatetime columns, and then converts the resulting timedelta object to days using pd.to_timedelta(). The resulting number of days is then plotted on the x-axis, and the bill amount on the y-axis. Each point is colored based on the value in the Company column, and hovering over a point shows the corresponding value in the Specialisation column. The resulting plot is returned as a Plotly Express scatter plot.
    Returns:
    A Plotly Express scatter plot of bill amount versus number of days of hospitalization, colored by company and with specialization shown on hover.

    """
    
    ip_sales_details_df['duration'] = ip_sales_details_df['dischargedatetime'] -ip_sales_details_df['admitdatetime']
    ip_sales_details_df['numberofdays'] = ip_sales_details_df['duration'].apply(pd.to_timedelta).dt.days
    return px.scatter(ip_sales_details_df, x='numberofdays', y='billamount', color="Company", hover_name="Specialisation", size='numberofdays')

def ip_netamt_specialisation_bar():
    """
    Creates a horizontal bar chart using Plotly Express to visualize the net amount billed for each medical specialization in the ip_sales_details_df DataFrame, with the bars colored by category.

    Returns:
    --------
    A Plotly graph object of a horizontal bar chart showing the net amount billed for each medical specialization in the DataFrame.
    """
    return px.bar(ip_sales_details_df,y= 'Specialisation',x='netamount',color ='category')

def ip_netamt_cat_bar():
    """
    This function creates a bar chart using the Plotly Express library to display the net amount of sales for each category in the 'ip_sales_details_df' dataset. The y-axis represents the categories, the x-axis represents the net amount of sales, and the color of the bars represents the specialisation of the sale.

    Returns:
    --------
    fig : plotly.graph_objs._figure.Figure
        A Plotly figure object representing the bar chart.
    """
    return px.bar(ip_sales_details_df,y= 'category',x='netamount',color ='Specialisation')

def ip_net_amt_company_bar():
    """
    Returns a bar chart using Plotly Express that shows the net amount of each company, 
    colored by area.

    Parameters:
    None.

    Returns:
    fig (plotly.graph_objs._figure.Figure): Plotly bar chart object.
    """
    return px.bar(ip_sales_details_df,y = 'Company',x='netamount',color ='Area')

def ip_package_fees_specialisation_bar():
    """
Creates a bar chart using Plotly Express to show the package fees for each specialisation of the IP sales details data, 
colored by the category.

Returns:
- A Plotly Express bar chart object.

Input:
- ip_sales_details_df: A Pandas DataFrame containing IP sales details data with columns 'Specialisation', 'PackageFees',
  and 'category'.
  
Output:
- A Plotly Express bar chart object with 'Specialisation' on the y-axis, 'PackageFees' on the x-axis, and colored by 'category'.
"""
    return px.bar(ip_sales_details_df,y='Specialisation',x='PackageFees',color ='category')

def ip_package_fees_cat_bar():
    """
    Returns a Plotly bar 
    chart showing the distribution of package fees 
    for each category of medical specialization in the inpatient sales details dataset.

    Args:
        None
    
    Returns:
     A Plotly bar chart object displaying the package fees for each category of medical specialization.
    
    Raises:
        None

    """
    return px.bar(ip_sales_details_df,y='category',x='PackageFees',color ='Specialisation')

def ip_package_fees_company_bar():
    """
Creates a bar chart using the Plotly Express library to show the relationship between the package fees charged by companies for inpatient services and the area in which they are located.

Args:
    None

Returns:
    A Plotly bar chart object representing the relationship between the package fees charged by companies for inpatient services and the area in which they are located.

Raises:
    None
    """
    return px.bar(ip_sales_details_df,y ='Company',x='PackageFees',color ='Area')


ip_sales_details = html.Div([
    html.H1("IP Sales Details"),
    html.Br(),
    # insert code for IP Sales Details visualization here
    html.H4('Bill amount vs Duration'),
    html.P('The visualization shows the duration (the difference between admit date and dischard date) \
           of a patient being admitted to the hospital and the related bill amount for the same.'),
    dcc.Graph(id='discharge-difference', figure=admit_discharge_date_bill_amount_analysis()),
 
    html.H4('Net Amount vs Specialisation'),
    html.P('The visualization shows the net amount of the hospital being raised based on the Specialization. The filter used is related to the Company.'),
    dcc.Graph(id='ip_netamount_specialisation', figure=ip_netamt_specialisation_bar()),
 
    html.H4('Net Amount vs Category'),
    html.P('The visualization shows the net amount of the hospital being raised based on the Category. The filter used is  related to the Specialization.'),
    dcc.Graph(id='ip_netamount_category', figure=ip_netamt_cat_bar()),

    html.H4('Net Amount vs Company'),
    html.P('The visualization shows the net amount of the hospital being raised based on the Company. The filter used is related to the Area/State.'),
    dcc.Graph(id='ip_netamount_company', figure=ip_net_amt_company_bar()),
    
    html.H4('Package Fees vs Specialisation'),
    html.P('The visualization shows the Package Fees of the hospital being raised based on the Specialization. The filter used is related to the category.'),
    dcc.Graph(id='ip_packagefees_specialisation', figure=ip_package_fees_specialisation_bar()),
    
    html.H4('Package Fees vs category'),
    html.P('The visualization shows the Package Fees of the hospital being raised based on the category. The filter used is related to the Specialization.'),
    dcc.Graph(id='ip_packagefees_category', figure=ip_package_fees_cat_bar()),
    
    html.H4('Package Fees vs Company'),
    html.P('The visualization shows the Package Fees of the hospital being raised based on the Company. The filter used is related to the Area/State.'),
    dcc.Graph(id='ip_packagefees_company', figure=ip_package_fees_company_bar()),
])



# define page content for IP Sales Report sheet
ip_sales_report_df = pd.read_excel('data/final/Ip_Sales_Report_Final.xlsx')


def ip_bill_amount_sales_report_company_bar():
    """
Creates a line chart using Plotly Express that shows the trend of the total bill amount for each company in the given IP sales report dataframe over time.

Parameters:
ip_sales_report_df (pandas.DataFrame): the IP sales report dataframe containing the following columns - 'datetime', 'COMPANY', 'BILL AMOUNT'

Returns:
A Plotly Express line chart displaying the trend of the total bill amount for each company in the given IP sales report dataframe over time.
"""

    return px.line(ip_sales_report_df,y ='BILL AMOUNT',x='datetime',color ='COMPANY')

def ip_discount_sales_report_company_bar():
    """
Returns an area plot of the discount amounts over time for each company in the IP sales report DataFrame.

Parameters:
None

Returns:
A Plotly express area plot of the discount amounts over time for each company in the IP sales report DataFrame.
"""

    return px.area(ip_sales_report_df,y ='DISCOUNT',x='datetime',color ='COMPANY')

ip_sales_report = html.Div([
    html.H1("IP Sales Report"),
    html.Br(),
    # insert code for IP Sales Report visualization here 
    html.H4('Bill Amount vs Date'),
    html.P('The visualization shows the Bill amount of the hospital being raised based on the date time. The filter used is related to the Company. It is a time series analysis.'),
    dcc.Graph(id='ip_bill_amount_sales_report_company_bar', figure=ip_bill_amount_sales_report_company_bar()),
    
    html.H4('Discount vs Date'),
    html.P('The visualization shows the Discount of the hospital being raised based on the date time. The filter used is related to the Company. It is a time series analysis.'),
    dcc.Graph(id='ip_discount_sales_report_company_bar', figure=ip_discount_sales_report_company_bar()),

])

# define page content for IP Sales Summary Report sheet
ip_sales_summary_df = pd.read_excel('data/final/Ip_Sales_Summary_Report_Final.xlsx')

def admit_discharge_room_rent_analysis():
    """
    Generates a scatter plot using Plotly Express that shows the relationship between the length of stay in the hospital 
    (number of days between admission and discharge) and the room rent amount charged for each patient. The color of each point 
    corresponds to the patient's diagnosis and the size of the point corresponds to the total bill amount charged to the patient. 

    Returns:
    --------
    fig : plotly.graph_objs._figure.Figure
        A Plotly figure object that can be displayed using `plotly.offline.iplot()` or `plotly.io.show()`.
    """
    ip_sales_summary_df['duration'] = ip_sales_summary_df['DischargeDatetime'] - ip_sales_summary_df['AdmitDatetime']
    ip_sales_summary_df['numberofdays'] = ip_sales_summary_df['duration'].apply(pd.to_timedelta).dt.days
    return px.scatter(ip_sales_summary_df, x='numberofdays', y='Room Rent', color="Diagnosis", hover_name="Category", size='Bill Amount')


def ip_pharm_diagnosis_bar():
    """Returns a Plotly bar chart showing the pharmacy sales for each diagnosis in the IP sales summary dataframe, with color denoting the state.

Parameters:
None

Returns:
A Plotly bar chart object.
    """
    return px.bar(ip_sales_summary_df,y ='Diagnosis',x='Pharmacy',color ='State')

def ip_docfees_surgerydept_bar():
    """This function returns a bar chart created using the Plotly Express library. The chart displays the total doctor fees paid for each type of surgery in the given dataset, grouped by country. The y-axis represents the different types of surgery and the x-axis represents the total doctor fees paid for each surgery type.
    The color of the bars represents the doctor who performed the surgery.

    Returns:
        A Plotly bar chart object.
    """
    return px.bar(ip_sales_summary_df,y ='SURGERYTYPE',x='Doctor Fees',color ='DoctorName')

def ip_food_beverages_pie_chart():
    """
    Generates a pie chart showing the total amount of food and beverages sales for each company, colored by test type.

    Returns:
    --------
    A plotly express pie chart object.
    """
    return px.bar(ip_sales_summary_df,x='Food and Beverages',y = 'Company', color='Test')

ip_sales_summary_report = html.Div([
    html.H1("IP Sales Summary Report"),
    html.Br(),
   
    
    # insert code for IP Sales Summary Report visualization here
    html.H4('Room rent vs Duration'),
    html.P('The visualization shows the scatter plot of duration of the patient in the hospital and the room rent paid.'),
    dcc.Graph(id='admit_discharge_room_rent_analysis', figure=admit_discharge_room_rent_analysis()),
    
    html.H4('Diagnosis vs pharmacy fees'),
    html.P('The visualization shows the bar plot of pharmacy fees of the hospital and the Diagnosis used.'),
    dcc.Graph(id='ip_pharm_diagnosis_bar', figure=ip_pharm_diagnosis_bar()),

    html.H4('Surgery Type vs Doctor fees'),
    html.P('The visualization shows the bar plot of Doctor fees of the hospital and the Surgery Type used.'),
    dcc.Graph(id='ip_docfees_surgerydept_bar', figure=ip_docfees_surgerydept_bar()),
    
    html.H4('Company vs Food and Beverages cost'),
    html.P('The visualization shows the bar plot of Food and Beverages cost of the hospital and the Company.'),
    dcc.Graph(id='ip_food_beverages_pie_chart', figure=ip_food_beverages_pie_chart()),
])


# define page content for Equipment - IP Sales Detail sheet
ip_equipment_sales_final_df = pd.read_excel('data/final/Ip_Equipment_Sales_Final.xlsx')

def analyse_amt_vs_time_equipment_sales():
    return px.line(ip_equipment_sales_final_df,y ='amt',x='DateTime',color ='specs')


def analyse_bar_specs_equipment_sales():
    return px.bar(ip_equipment_sales_final_df,y ='amt',x='specs')

def analyse_bar_specialisation_equipment_sales():
    return px.bar(ip_equipment_sales_final_df,y ='amt',x='specialisation')
    
ip_equipment_sales_final = html.Div([
    html.H1("IP Equipment Sales Report"),
    html.Br(),
    
    
    # insert code for IP Sales Summary Report visualization here
    html.H4('Equipment Amount vs Date'),
    html.P('The visualization shows the line plot of equipment amount of the hospital and the date.'),
    dcc.Graph(id='analyse_amt_vs_time_equipment_sales', figure=analyse_amt_vs_time_equipment_sales()),
    html.H4('Type of Tests'),
    html.P('The visualization shows the bar plot of the type of tests'),
    dcc.Graph(id='analyse_bar_specs_equipment_sales', figure=analyse_bar_specs_equipment_sales()),
    html.H4('Specialization Type'),
    html.P('The visualization shows the bar plot of the type of specialization'),
    dcc.Graph(id='analyse_bar_specialisation_equipment_sales', figure=analyse_bar_specialisation_equipment_sales()),
   ]) 


# define page content for Equipment - IP  Detail sheet

ip_equipment_details_final_df = pd.read_excel('data/final/Ip_Equipment_Details_Final.xlsx')

def quantity_vs_datetime():
    return px.line(ip_equipment_details_final_df, x= 'DateTime', y='Quantity', color='Equipment Name')

def amount_vs_datetime():
    return px.line(ip_equipment_details_final_df, x= 'DateTime', y='Amount', color='Equipment Name')
ip_equipment_details_final = html.Div([
    html.H1("IP Equipment Details Report"),
    html.Br(),
   
    
    # insert code for IP Sales Summary Report visualization here
    html.H4('Amount vs Date'),
    html.P('The visualization shows the line plot of Amount and Date of the equipments'),
    dcc.Graph(id='amount_vs_datetime', figure=amount_vs_datetime()),
    html.H4('Quantity vs Date'),
    html.P('The visualization shows the line plot of Quantity and Date of the equipments'),
  
    dcc.Graph(id='quantity_vs_datetime', figure=quantity_vs_datetime()),
    

    
   ])



# define page content for SIMS Dashboard sheet

cards = dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Sales Detail Analysis", className="card-title"),
                    html.P(f"There are {len(ip_sales_details_df)} rows"),
                    dbc.Button("Sales", color="primary", href="/ip_sales_details"),
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
                    dbc.Button("Discount", color="primary", href="/ip_discount_report"),
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
                    html.H4("Sales Report Analysis", className="card-title"),
                    html.P(f"There are {len(ip_sales_report_df)} rows"),
                    dbc.Button("Sales Report", color="primary", href="/ip_sales_report"),
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
                    html.H4("Sales Summary Report Analysis", className="card-title"),
                    html.P(f"There are {len(ip_sales_summary_df)} rows"),
                    dbc.Button("Sales Summary", color="primary", href="/ip_sales_summary_report"),
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

cover_image = "https://simshospitals.com/wp-content/uploads/2021/09/SIMS-Logo.png"
dashboard_home = html.Div([
    html.H1("Welcome to SIMS Dashboard"),
        html.Div([
        html.Img(src=cover_image, style={'width': '100%'})
    ], style={'width': '80%','height':'40%'}),
          html.Br(),
            html.Br(),
    html.P("SIMS Hospital is a leading healthcare provider in the region, offering a wide range of medical services and treatments to patients. As with any healthcare provider, understanding sales data is critical to the success of the hospital. Sales data can help SIMS Hospital track trends in patient demand, identify areas for improvement in services or marketing, and forecast revenue."),
    html.P("To make sense of sales data, SIMS Hospital can conduct sales analysis. This involves collecting and analyzing data on patient visits, treatments, and revenue. Sales analysis can help SIMS Hospital identify key metrics such as patient volumes, revenue by department, and average revenue per patient."),
    html.P("By conducting sales analysis, SIMS Hospital can gain insights into patient behavior, identify trends in revenue and expenses, and optimize resources to improve profitability. Additionally, sales analysis can help SIMS Hospital identify potential areas for growth, such as expanding services in high-demand departments or targeting specific patient demographics."),
    html.P("Overall, sales analysis is a critical tool for SIMS Hospital to understand its business and make data-driven decisions that improve patient outcomes and financial performance."),
    html.Br(),
    # insert code for IP Equipment Details visualization here
    cards
], className="container")




# define callback to display page content based on URL
@app.callback(dash.dependencies.Output("page-content", "children"), [dash.dependencies.Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/ip_discount_report":
        return ip_discount_report 
    elif pathname == "/ip_sales_details":
        return ip_sales_details
    elif pathname =="/ip_sales_report":
        return ip_sales_report
    elif pathname == "/ip_sales_summary_report":
        return ip_sales_summary_report
    elif pathname == "/":
        return dashboard_home
    elif pathname=='/ip_equipment_sales_final':
        return ip_equipment_sales_final
    elif pathname=='/ip_equipment_details_final':
        return ip_equipment_details_final
    else:
        return html.H1("404 - Page Not Found")
    
if __name__ == "__main__":
    app.run_server(debug=True)
