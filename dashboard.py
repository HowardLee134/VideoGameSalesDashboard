import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide", 
    initial_sidebar_state="collapsed" 
)

# Add custom CSS to increase the page margins
st.markdown("""
    <style>
    .reportview-container .main .block-container{
        padding-top: 1rem;  # Adjust top padding
        padding-right: 1rem;  # Adjust right padding
        padding-left: 1rem;  # Adjust left padding
        padding-bottom: 1rem;  # Adjust bottom padding
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
video_games_data = pd.read_csv('data/video_games_sales.csv')

# Mock region_sales DataFrame for demonstration
region_sales = pd.DataFrame({
    'coordinates': [(-99.1332, 19.4326), (10.0183, 53.5511), (120.6917, 30.6895), (14.6048, 9.0625)],  # Example: Mexico City, Hamburg, Tokyo
    'region': ['North America', 'Europe', 'Japan', 'others'],
    'sales': [4392.95, 2434.13, 1291.02, 797.75]
})

# Display Top 3 Games in Donut chart For each Region
def display_top_games(data, region):
    region_totals = {
        'Global': 892.44,  
        'North America': 439.95,  
        'Europe': 243.13,  
        'Japan': 129.02,  
        'Other': 79.75 
    }
    # Dropdown for region selection
    selected_region = st.selectbox(
        "Select Region",
        options=["Global", "North America", "Europe", "Japan", "Other"],
        index=0,  # Default selection (Global)
        key='region_selection'  # Ensure unique key if using multiple selectboxes
    )

    # Map the selected region to the corresponding sales column
    sales_column = {
        'Global': 'global_sales',
        'North America': 'na_sales',
        'Europe': 'eu_sales',
        'Japan': 'jp_sales',
        'Other': 'other_sales'
    }[selected_region]

    # Get top 3 games in the selected region
    top_games = data.nlargest(3, sales_column)[['name', sales_column]]

    # Calculate percentage of total sales
    total_sales = region_totals[selected_region]
    top_games['Percentage'] = (top_games[sales_column] / total_sales) * 100


    # Using loop and st.container to display the charts vertically
    for _, row in top_games.iterrows():
        with st.container():
            donut_fig = go.Figure(go.Pie(
                values=[row['Percentage'], 100 - row['Percentage']],
                labels=[row['name'], ''],
                marker_colors=['#00cc96', '#eeeeee'],
                hole=0.7,
                textinfo='none',
                hoverinfo='label+percent',
                direction='clockwise',
                sort=False,
            ))

            # Update the layout
            donut_fig.update_layout(
                showlegend=False,
                annotations=[dict(
                    text=f"{row['Percentage']:.1f}%",  # The text to display (the percentage)
                    x=0.5, y=0.5,  # Position the text in the center of the donut hole
                    font_size=40,  # Increase the font size here
                    showarrow=False,
                    font=dict(
                        color='#00cc96'  # percentage color 
                    )
                )],
                margin=dict(t=20, l=20, r=20, b=20),
                height=200,
            )
                        # Display the chart
            st.plotly_chart(donut_fig, use_container_width=True)

            # Display the game name with custom styling
            st.markdown(f"<h3 style='text-align: center; color: #00cc96;'>{row['name']}</h3>", unsafe_allow_html=True)

            # Separate each container for visual spacing
            st.markdown("---")

# Region Sales WorldMap DataFrane for demonstration
def plot_global_sales_by_region(region_sales):
    # Load the world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # Define the mapping from country names to regions
    countries_to_regions = {
        'United States of America': 'North America',
        'Canada': 'North America',
        'Mexico': 'North America',
        'Guatemala': 'North America',
        'Cuba': 'North America',
        'Haiti': 'North America',
        'Dominican Republic': 'North America',
        'Honduras': 'North America',
        'Nicaragua': 'North America',
        'El Salvador': 'North America',
        'Costa Rica': 'North America',
        'Panama': 'North America',
        'Jamaica': 'North America',
        'Trinidad and Tobago': 'North America',
        'The Bahamas': 'North America',
        'Barbados': 'North America',
        'Saint Lucia': 'North America',
        'Grenada': 'North America',
        'Saint Vincent and the Grenadines': 'North America',
        'Antigua and Barbuda': 'North America',
        'Belize': 'North America',
        'Saint Kitts and Nevis': 'North America',
        'Dominica': 'North America',
        'France': 'Europe',
        'Germany': 'Europe',
        'United Kingdom': 'Europe',
        'Italy': 'Europe',
        'Spain': 'Europe',
        'Japan': 'Japan',
        'Poland': 'Europe',
        'Ukraine': 'Europe',
        'Romania': 'Europe',
        'Netherlands': 'Europe',
        'Belgium': 'Europe',
        'Sweden': 'Europe',
        'Czech Republic (Czechia)': 'Europe',
        'Greece': 'Europe',
        'Portugal': 'Europe',
        'Hungary': 'Europe',
        'Belarus': 'Europe',
        'Austria': 'Europe',
        'Switzerland': 'Europe',
        'Serbia': 'Europe',
        'Bulgaria': 'Europe',
        'Denmark': 'Europe',
        'Slovakia': 'Europe',
        'Finland': 'Europe',
        'Norway': 'Europe',
        'Ireland': 'Europe',
        'Croatia': 'Europe',
        'Moldova': 'Europe',
        'Bosnia and Herzegovina': 'Europe',
        'Albania': 'Europe',
        'Lithuania': 'Europe',
        'Slovenia': 'Europe',
        'North Macedonia': 'Europe',
        'Latvia': 'Europe',
        'Estonia': 'Europe',
        'Luxembourg': 'Europe',
        'Montenegro': 'Europe',
        'Malta': 'Europe',
        'Iceland': 'Europe',
        'Andorra': 'Europe',
        'Liechtenstein': 'Europe',
        'Monaco': 'Europe',
        'San Marino': 'Europe',
        'Holy See': 'Europe',
        'Russia': 'Europe'
    }

    
    # Assign regions and colors
    world['region'] = world['name'].apply(lambda x: countries_to_regions.get(x, 'Other'))
    region_colors = {
        'North America': 'blue',
        'Europe': 'red',
        'Japan': 'yellow',
        'Other': 'white'
    }
    world['color'] = world['region'].map(region_colors)

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))

    # Set the background color of the figure (outside the axes)
    fig.patch.set_facecolor('#111111')
    
    # Set the background color of the axes (inside the plot area)
    ax.set_facecolor('#111111')
    
    
    world.plot(ax=ax, color=world['color'], edgecolor='orange' , linewidth=0.8)
    ax.axis('off')

    # Adding text annotations for each region's sales
    for index, row in region_sales.iterrows():
        ax.text(row['coordinates'][0], row['coordinates'][1], f"{row['region']}:\n{row['sales']}M",
                ha='center', fontsize=12, fontweight='bold', color='darkblue',
                bbox=dict(facecolor='lightyellow', alpha=0.5, edgecolor='grey', boxstyle='round,pad=0.5'))

    # Display the plot in Streamlit
    st.pyplot(fig)

# Bar chart DataFrame for demostration
def create_genre_sales_chart(data):
    total_genre_sales = data.groupby('genre')['global_sales'].sum().reset_index()
    total_genre_sales['global_sales_millions'] = total_genre_sales['global_sales'] 
    total_genre_sales_sorted = total_genre_sales.sort_values('global_sales_millions', ascending=False)

    fig = px.bar(
        total_genre_sales_sorted,
        x='global_sales_millions',
        y='genre',
        orientation='h',
        labels={'global_sales_millions': 'Sales (Millions)', 'genre': 'Genre'},
        color='global_sales_millions',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(
        margin=dict(t=150, l=0, r=0, b=0),
        xaxis_title="Sales (Millions)",
        yaxis_title="Genre",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# Interative plot for demostration
# Define a function to create an interactive plot based on category
def create_interactive_plot(category):
    # Group the data by the selected category and sum the sales
    grouped_data = video_games_data.groupby(category)[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum()
    
    # Limit the number of publishers for better visualization
    if category == 'publisher':
        top_publishers = video_games_data['publisher'].value_counts().nlargest(15).index
        grouped_data = grouped_data.loc[top_publishers]

    # Create a bar plot for the selected category
    fig = go.Figure()
    for region in ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']:
        fig.add_trace(go.Bar(x=grouped_data.index, y=grouped_data[region], name=region))
    
    fig.update_layout(barmode='group', title=f'Sales by {category}', xaxis_title=category, yaxis_title='Sales')
    
    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)
           
#section for section 5 
def create_top_platforms_pie_chart(data):
    # Group data by platform and sum global sales
    platform_sales = data.groupby('platform')['global_sales'].sum().reset_index()
    # Select the top 6 platforms
    top_platforms = platform_sales.nlargest(6, 'global_sales')
    # Create the pie chart
    fig = px.pie(top_platforms, values='global_sales', names='platform')
    
    
    # Hide the legend
    fig.update_layout(showlegend=False)

    # Update the layout to be similar to the bar chart template
    fig.update_layout(
        autosize=False,
        width=500,  # Width of the chart
        height=500,  # Height of the chart
        margin=dict(t=20, b=0, l=150, r=0),  # Margins around the chart  
    
        legend=dict(
            #orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        
        # Set paper and plot background color to transparent (or any other color you'd like)
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Adjust the domain of the pie to make space for the legend
    fig.update_traces(domain=dict(x=[0, 0.75]))

    # Place labels inside the pie chart segments and increase the font size
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=18)

    return fig





st.markdown("""
    <div style='margin-top: -30px;'>
        <h1 style='text-align: center; color: white; font-size: 50px;'>
            🎮 Video Game Sales Dashboard
        </h1>
    </div>
    """, unsafe_allow_html=True)

# # Sidebar for platform and genre selection
# with st.sidebar:
#     st.title('🎮 Video Game Sales Dashboard')
#     platform_list = video_games_data['platform'].unique().tolist()
#     genre_list = video_games_data['genre'].unique().tolist()
    
#     selected_platform = st.selectbox('Select a platform', platform_list)
#     selected_genre = st.selectbox('Select a genre', genre_list)

# Define the main columns with the given ratios
section1, section2, section3 = st.columns([2, 5, 3])

# Section 1 content (Full Height)
with section1:
    st.markdown("""
    <h1 style='text-align: center; font-size: 25px;'>
        Top 3 Game Sales 
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("")
    display_top_games(video_games_data, 'Global')

# Section 2 content (map plot)
with section2:
    plot_global_sales_by_region(region_sales)

# Section 3 content (Genre Sales Chart)
with section3:
    st.markdown("""
    <h1 style='text-align: center; font-size: 25px;'>
        Platforms Sales
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("")
    
    pie_chart_fig = create_top_platforms_pie_chart(video_games_data)
    st.plotly_chart(pie_chart_fig, use_container_width=True)
    

# Split Section 2 and 3 into top and bottom parts
with section2:
    # st.markdown("#### Section 4: Interactive Sales by Category")
    
    # Insert your dropdown for selecting the category right inside the section
    selected_category = st.selectbox(
        'Choose a category to display sales data:',
        ['year', 'platform', 'genre', 'publisher'],
        key='category_selector'  # A unique key ensures the selectbox functions correctly
    )

    # Now call the function that creates the interactive plot with the selected category
    create_interactive_plot(selected_category)


with section3:
    st.markdown("""
    <h1 style='text-align: center; font-size: 25px; padding-top: 100px;'>
        Genre Sales
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("")
    genre_sales_fig = create_genre_sales_chart(video_games_data)
    st.plotly_chart(genre_sales_fig, use_container_width=True)

# Make sure to call st.container() or st.columns() in the correct scope
# to ensure the content is placed in the desired section

