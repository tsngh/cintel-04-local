import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render
import seaborn as sns
from shiny import reactive
from palmerpenguins import load_penguins

# Load the penguins dataset
penguins_df = load_penguins()

ui.page_opts(title="Tesheena's Palmer Penguins", fillable=True)

with ui.sidebar(position="right", open="open"):
    ui.h2("Sidebar")
    
    ui.input_selectize(
        "selected_attributes",
        "Penguin's Attributes", 
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    
    ui.input_numeric("plotly_bin_count", "Number of Plotly Bins", 10, min=1, max=15)

    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 5, 25, 15)

    ui.input_checkbox_group(
        "selected_species_list",
        "Penguin Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    ui.hr()

    ui.a("GitHub", href="https://github.com/tsngh/cintel-02-data", target="_blank")

with ui.card():
    ui.card_header("Table View")
    @render.data_frame
    def data_table():
        return render.DataTable(penguins_df, filters=False,selection_mode='row')

with ui.card():
    ui.card_header("Grid View")
    @render.data_frame
    def data_grid():
        return render.DataGrid(penguins_df, filters=False, selection_mode="row")

with ui.layout_columns():
    with ui.card():
        ui.card_header("Plotly Histogram of Penguins")
        @render_plotly
        def histogram_plotly():
            filtered_df = penguins_df[penguins_df['species'].isin(input.selected_species_list())]
            return px.histogram(
                data_frame=filtered_df,
                x=input.selected_attributes(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    with ui.card():
        ui.card_header("Seaborn Histogram of Penguins")
        @render.plot
        def histogram_seaborn():
            filtered_df = penguins_df[penguins_df['species'].isin(input.selected_species_list())]
            return sns.histplot(
                data=filtered_df,
                x=input.selected_attributes(),
                bins=input.seaborn_bin_count(),
                hue="species",
            )

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        filtered_df = penguins_df[penguins_df['species'].isin(input.selected_species_list())]
        return px.scatter(
            filtered_df,
            x="body_mass_g",
            y=input.selected_attributes(),
            color="species",
            labels={
                "body_mass_g": "Body Mass (g)",
                input.selected_attributes(): f"{input.selected_attributes().replace('_', ' ').title()} (mm)"
            }
        )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    return penguins_df[penguins_df["species"].isin(selected_species)]
