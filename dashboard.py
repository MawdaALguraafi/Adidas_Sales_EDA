
#import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page settings
st.set_page_config(page_title="Adidas Dashboard", layout="wide")

#Apply custom HTML/CSS styling to the dashboard. >>>
st.markdown("""
<style>
body { background-color: #0A0A0A; color: #E0E1DD; }
.sidebar .sidebar-content { background-color: #0D1B2A; color: #E0E1DD; }
</style>
""", unsafe_allow_html=True)

#Streamlit ignore or block this HTML/CSS here we are asking Streamlit to apply this raw HTML/CSS.^



#/Load Clean Data
df = pd.read_csv("cleaned_data_sales.csv")

# Page Header
col_logo, col_title = st.columns([1,4]) # Logo and Title

with col_logo:
    st.image("/content/adidas.png", width=120)

with col_title:
    st.title("Adidas Sales Dashboard")


# ===== Sidebar Filters =====
st.sidebar.header("Filters")


# Selectbox choices  list
regions = ["All"] + sorted(df["Region"].unique()) # Ex. All + west , north etc.
methods = ["All"] + sorted(df["Sales Method"].unique()) # Ex. All + online , in-store etc.
years = ["All"] + sorted(df["Year"].unique()) # Ex. All + 2020,2021 etc.

# Dropdown menu st.sidebar.selectbox(Label,Options or list)
selected_region = st.sidebar.selectbox("Select Region", regions)
selected_method = st.sidebar.selectbox("Select Sales Method", methods)
selected_year = st.sidebar.selectbox("Select Year", years)

# Apply filters
# A COPY -  Why to filter without changing the actual data
filtered_df = df.copy()


if selected_region != "All":#NOT All?
    filtered_df = filtered_df[filtered_df["Region"] == selected_region] # Copy the df and filter it according to the selected Region.
if selected_method != "All":#NOT All?
    filtered_df = filtered_df[filtered_df["Sales Method"] == selected_method] # Copy the df and filter it according to the selected Sales Method.
if selected_year != "All":#NOT All?
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]  # Copy the df and filter it according to the selected Year.


# Find the product with the highest total units sold in the filtered data to display as the Top Product KPI
top_product_name = filtered_df.groupby("Product")["Units Sold"].sum().idxmax()

# ===== KPIs =====
col1, col2, col3, col4 = st.columns(4)

#.metric(Lable,value)
col1.metric("Total Sales", f"${filtered_df['Total Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Operating Profit'].sum():,.0f}")
col3.metric("Total Units Sold", f"{filtered_df['Units Sold'].sum():,}")


col4.markdown(f"""
**Top Product:**
<span style='font-size:20px; line-height:1.2'>{top_product_name}</span>
""", unsafe_allow_html=True) # Again here we are asking Streamlit to apply this raw HTML/CSS.^


# Colors for dashboard
chart_colors = [
    '#1E3A8A',  # Indigo 800
    '#2563EB',  # Blue 600
    '#3B82F6',  # Blue 500
    '#60A5FA',  # Blue 400
    '#93C5FD',  # Blue 300
    '#BFDBFE',  # Blue 200
    '#E0F2FE',  # Light Blue 100
]

# Fisrt Row : Overview Charts
# Subheader
st.subheader("Overview Charts")

row1_col1, row1_col2 = st.columns(2)



# Row1 - Column1: Monthly Sales Line Chart
with row1_col1:
    st.markdown("### Monthly Sales (by Year & Month)")

    # Ensure 'Invoice Date' is datetime
    filtered_df['Invoice Date'] = pd.to_datetime(filtered_df['Invoice Date'])

    # Create 'YearMonth' column in "Jan 2020" format
    filtered_df['YearMonth'] = filtered_df['Invoice Date'].dt.strftime('%b %Y')

    # Aggregate total sales per 'YearMonth'
    monthly_sales = (
        filtered_df.groupby('YearMonth')['Total Sales']
        .sum()
        .reset_index()
    )

    # Sort x-axis by actual date
    monthly_sales['Date'] = pd.to_datetime(monthly_sales['YearMonth'])
    monthly_sales = monthly_sales.sort_values('Date')

    # Create the plot
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    ax.plot(
        monthly_sales['YearMonth'],
        monthly_sales['Total Sales'],
        color=chart_colors[2],
        linewidth=4,
        marker='o'  # Show points on the line
    )

    ax.set_title("Monthly Sales (Year & Month)", color="#FFFFFF")
    ax.set_xlabel("Month-Year", color="#FFFFFF")
    ax.set_ylabel("Total Sales ($)", color="#FFFFFF")

    # Customize x-axis and y-axis
    plt.xticks(rotation=45, ha="right", fontsize=9, color="#FFFFFF")
    plt.yticks(color="#FFFFFF")

    # Remove chart borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the figure in Streamlit
    st.pyplot(fig)



# Row1 - Column2: Profit by Region Bar Chart
with row1_col2:
    st.markdown("### Profit by Region") # Add a header above the chart

    # Group the filtered data by 'Region' and sum the 'Operating Profit' for each region
    profit_region = filtered_df.groupby('Region')['Operating Profit'].sum()

    # Create a matplotlib figure and axis for the bar chart
    fig, ax = plt.subplots()

    # Set the figure and axis background to transparent
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Select bar colors from the chart_colors list
    # Only take as many colors as there are regions
    bar_colors = chart_colors[:len(profit_region)]

    # Create a Bar Chart ax.bar(x, y , bar color , edge color)
    ax.bar(profit_region.index, profit_region.values, color=bar_colors, edgecolor='none')

    # Set chart title and color white
    ax.set_title("Profit by Region", color="#FFFFFF")
    # Set x-axis label and y-axis and color white
    ax.set_ylabel("Profit ($)", color="#FFFFFF")
    ax.set_xlabel("Region", color="#FFFFFF")

    # Set x-axis tick and y-axis labels color white
    ax.tick_params(axis='x', colors="#FFFFFF")
    ax.tick_params(axis='y', colors="#FFFFFF")

    # Format y-axis numbers with commas and no decimals for readability
    from matplotlib.ticker import StrMethodFormatter
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # Remove chart borders (top, bottom, left, right)
    for spine in ax.spines.values():
        spine.set_visible(False)


    # Display the figure in Streamlit
    st.pyplot(fig)




# Second Row: Detailed Charts
st.subheader("Detailed Charts")
row2_col1, row2_col2 = st.columns(2)

# Second Row first Column:Top Products by Units Sold
with row2_col1:
    st.markdown("### Top Products by Units Sold") # Add a header above the chart
    # Group the filtered DataFrame by 'Product' and sum the 'Units Sold' for each product
    # Then sort the products in descending order and take the top 10
    top_products = ( filtered_df.groupby("Product")["Units Sold"].sum().sort_values(ascending=False).head(10))

    # Create a matplotlib figure and axis for the bar chart
    #figsize=(width, height)
    fig, ax = plt.subplots(figsize=(9, 10))
    # Set figure and axis backgrounds to transparent
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Select as many colors from chart_colors as there are products in 'top_products'
    bar_colors = chart_colors[:len(top_products)]

    # Create horizontal bar chart
    # ax.barh(the y-values ,the x-values ,color ,edgecolor )
    ax.barh(top_products.index[::-1],top_products.values[::-1],color=bar_colors,edgecolor='none')

    # Set the Chart title color label white and size 16
    ax.set_title("Top Products by Units Sold", color="#FFFFFF", fontsize=16, fontweight='bold')
    # Set the x-axis label and y-axis , color label white and size 14
    ax.set_xlabel("Units Sold", color="#FFFFFF", fontsize=10)
    ax.set_ylabel("Product", color="#FFFFFF", fontsize=14)

    #The tick labels on the x-axis and y-axis color and size
    ax.tick_params(axis='x', colors="#FFFFFF", labelsize=12)
    ax.tick_params(axis='y', colors="#FFFFFF", labelsize=12)

    # Remove chart borders (top, bottom, left, right)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the figure in Streamlit
    st.pyplot(fig)


# Second Row Second Column:Profit by Sales Method
with row2_col2:# Add a header above the chart
    st.markdown("### Profit by Sales Method")

    # Group the data by "Sales Method" and sum up the "Operating Profit"
    profit_method = filtered_df.groupby('Sales Method')['Operating Profit'].sum()

    # Create a new matplotlib figure and axes for Pie Chart
    fig, ax = plt.subplots()
    # Set the background transparent
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Select colors for each slice from your predefined chart_colors
    # [:len(profit_method)] ensures the number of colors matches the number of slices
    pie_colors = chart_colors[:len(profit_method)]

    #ax.pie(profite value , label by method , percentage , start from up 90 , color of pie , text color)
    ax.pie(profit_method.values,labels=profit_method.index,autopct='%1.1f%%',startangle=90,colors=pie_colors,textprops={'color': "#FFFFFF"} )

    # Keep the pie chart circular (equal aspect ratio)
    ax.axis('equal')

    # Remove any chart spines (borders around plot area)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the chart in Streamlit
    st.pyplot(fig)
