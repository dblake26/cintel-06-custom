from pathlib import Path
import pandas as pd
from faicons import icon_svg
import plotly.express as px
from shiny import reactive, render, ui, input

# Name the page
ui.page_opts(title="Desiree's Life Expectancy Dashboard", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(title="Life Expectancy vs. Healthcare Expenditure", style="background-color: #D8BFD8;"):
    ui.markdown("""
    Despite access to healthcare being essential to survival for many, it is not accessible to everyone.  This dashboard was designed to explore the correlation between the total amount spent in healthcare and life expectancy. 
    
    Interact and explore, and remember, housing should be (because it is) healthcare!  
    """)

    # Create a slider for selecting the year range
    input.slider("year_range", "Year Range", min=1970, max=2020)

    # Add checkbox
    ui.input_checkbox_group(
        "country",
        "Country",
        ["Canada", "France", "Great Britain", "Germany", "Japan", "USA"],
        selected=["Canada", "France", "Great Britain", "Germany", "Japan", "USA"],
    )
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

# Define a reactive calculation to read the CSV file
@reactive.calc
def dat():
    infile = Path(__file__).parent / "healthexp.csv"
    return pd.read_csv(infile)

# Define a reactive calculation to filter the data based on the selected year range
@reactive.calc
def filtered_data():
    return dat()[(dat()["Year"] >= input.year_range[0]) & (dat()["Year"] <= input.year_range[1])]

# Define the scatterplot
@render.plotly
def scatterplot():
    fig = px.scatter(filtered_data(), x="Life_Expectancy", y="Spending_USD", color="Year",
                     title="Life Expectancy vs. USD Spent by Year",
                     labels={"Life_Expectancy": "Life Expectancy", "Spending_USD": "USD Spent"})
    return fig

# Define a reactive calculation to generate the data frame
@reactive.calc
def dataframe():
    return dat()

# Define a reactive calculation to generate the table
@reactive.calc
def table():
    return dat()

# Render the UI elements
with ui.layout_columns():
    with ui.card(full_screen=True, style="background-color: #D8BFD8;"):
        ui.card_header("Life Expectancy and Expenditure USD")

        # Show the scatterplot
        ui.show(scatterplot)

    with ui.navset_card_underline():
        with ui.nav_panel("Data frame"):
            # Show the data frame
            @render.data_frame
            def frame():
                return dataframe()

        with ui.nav_panel("Table"):
            # Show the table
            @render.table
            def table_view():
                return table()
