# Import necessary libraries
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly, render_widget
import pandas as pd
import plotly.express as px
from pathlib import Path  # Import the Path class from the pathlib module

# Name the page
ui.page_opts(title="Desiree's Life Expectancy Dashboard", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(title="Life Expectancy vs. Healthcare Expenditure", style="background-color: #D8BFD8;"):
    ui.markdown("""
    Despite access to healthcare being essential to survival for many, it is not accessible to everyone.  
    This dashboard was designed to explore the correlation between the total amount spent in healthcare and life expectancy. 
    Interact and explore, and remember, housing should be (because it is) healthcare!  
    """)

    # Add a selectize input for selecting the year range
    ui.p("Select the year range below:")

    ui.input_slider("min_year", "Min Year:", min=1970, max=2020, value=1970, step=1)
    ui.input_slider("max_year", "Max Year:", min=1970, max=2020, value=2020, step=1)

    @reactive.calc
    def update_receiver_slider():
        # Update the receiver slider based on the selected year range
        ui.update_slider(
            "receiver",
            value=max(min(input.receiver(), input.max_year()), input.min_year()),
            min=input.min_year(),
            max=input.max_year(),
        )
    # Add checkbox
    ui.input_checkbox_group(
        "country",
        "Country",
        ["Canada", "France", "Great Britain", "Germany", "Japan", "USA"],
        selected=["Canada", "France", "Great Britain", "Germany", "Japan", "USA"],
    )

    # Add GitHub links
    ui.a(
        "GitHub Source",
        href="https://github.com/dblake26/cintel-06-custom/blob/main/app.py",
        target="_blank",
        style="color: black; display: block; margin-top: 20px;",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/dblake26/cintel-06-custom",
        target="_blank",
        style="color: black;",
    )

@reactive.calc
# Define a function to read the CSV file
def read_data():
    infile = Path(__file__).parent / "healthexp.csv"
    return pd.read_csv(infile)
    
# Define a function to filter the data based on the selected year range
def filter_data(data, year_range):
    return data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]
# Define a function to filter the data based on the selected country
def filter_by_country(data, countries):
    return data[data["Country"].isin(countries)]

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("stethoscope"), style="background-color: #D8BFD8;"):
        "Average Life Expectancy"

        @render.text
        def average_life_expectancy():
            # Calculate the mean and round to two decimal points
            data = filtered_data()  # Use filtered data here
            mean_life_expectancy = data["Life_Expectancy"].mean()
            rounded_mean = round(mean_life_expectancy, 2)
            return rounded_mean

    with ui.value_box(showcase=icon_svg("dollar-sign"), style="background-color: #D8BFD8;"):
        "Average Healthcare Expenditure"

        @render.text
        def average_spending_USD():
            # Calculate the mean and round to two decimal points
            data = filtered_data()  # Use filtered data here
            mean_spending_USD = data["Spending_USD"].mean()
            rounded_mean = round(mean_spending_USD, 2)
            return rounded_mean

# Define a reactive calculation to filter the data based on the selected year range and countries
@reactive.calc
def filtered_data():
    data = read_data()
    data = filter_data(data, (input.min_year(), input.max_year()))
    data = filter_by_country(data, input.country())
    return data


with ui.navset_card_underline():
    with ui.nav_panel("Data frame"):
        @render.data_frame
        def frame():
            # Display the data frame
            return read_data()

    with ui.nav_panel("Table"):
        @render.table
        def table():
        # Display the table
            return read_data()
