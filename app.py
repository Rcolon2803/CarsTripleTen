import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("vehicles_us.csv")


# Optional filter: remove price = 0
if st.checkbox("Remove vehicles with price = 0"):
    df = df[df['price'] > 0]
    st.success("Zero-price listings removed from view.")

# App title
st.title("🚗 Used Vehicle Explorer Dashboard")

# Price Distribution Histogram
st.subheader("💰 Price Distribution")
fig_price = px.histogram(df, x='price', nbins=100, title="Vehicle Price Distribution")
st.plotly_chart(fig_price)

# Price vs. Odometer Scatter Plot
st.subheader("📉 Price vs. Odometer by Type")
fig_scatter = px.scatter(
    df, x='odometer', y='price', color='type',
    title='Price vs. Odometer Colored by Vehicle Type',
    labels={'odometer': 'Mileage (mi)', 'price': 'Price ($)'}
)
st.plotly_chart(fig_scatter)

# Average Price by Fuel Type Bar Chart
st.subheader("⛽ Average Price by Fuel Type")
avg_price_by_fuel = df.groupby('fuel')['price'].mean().reset_index()
avg_price_by_fuel = avg_price_by_fuel.sort_values(by='price', ascending=False)

fig_bar = px.bar(
    avg_price_by_fuel,
    x='fuel',
    y='price',
    color='price',
    color_continuous_scale='Tealrose',
    title='Average Vehicle Price by Fuel Type'
)
st.plotly_chart(fig_bar)

# Sunburst Chart: Type > Condition > Fuel
st.subheader("🌞 Vehicle Category Breakdown")
sunburst_data = df.groupby(['type', 'condition', 'fuel'])['price'].mean().reset_index()

fig_sunburst = px.sunburst(
    sunburst_data,
    path=['type', 'condition', 'fuel'],
    values='price',
    color='price',
    color_continuous_scale='RdBu',
    title='Average Price by Type → Condition → Fuel')
st.plotly_chart(fig_sunburst)

# Footer
st.caption("Built with ❤️ using Streamlit, Plotly, and Pandas")
