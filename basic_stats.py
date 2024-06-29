import requests
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Streamlit button for rerun
st.button("Re-run")

st.write("""
# My first app!
""")

# Fetch data from the API
response = requests.get("https://www.fruityvice.com/api/fruit/all")
json_data = response.json()

# Extract the necessary information
fruits = json_data
extracted_fruits = []

for fruit in fruits:
    if fruit['name'].lower() not in ['hazelnut', 'dragonfruit']:
        event_info = {
            'name': fruit['name'],
            'family': fruit['family'],
            'order': fruit['order'],
            'genus': fruit['genus'],
            'calories': fruit['nutritions']['calories'],
            'fat': fruit['nutritions']['fat'],
            'sugar': fruit['nutritions']['sugar'],
            'carbohydrates': fruit['nutritions']['carbohydrates'],
            'protein': fruit['nutritions']['protein']
        }
        extracted_fruits.append(event_info)

# Create a DataFrame
df = pd.DataFrame(extracted_fruits)

# Create custom hover text
df['hover_text'] = df.apply(
    lambda row: f"Fruit: {row['name']}<br>Protein: {row['protein']}g<br>Carbohydrates: {row['carbohydrates']}g<br>Fat: {row['fat']}g",
    axis=1
)

# Create the 3D scatter plot with Plotly
fig = go.Figure()

# Define the colormap
colormap = px.colors.sequential.Viridis

# Add each fruit as a scatter plot point with custom hover text
for i in range(len(df)):
    fig.add_trace(go.Scatter3d(
        x=[df['protein'][i]],
        y=[df['carbohydrates'][i]],
        z=[df['fat'][i]],
        mode='markers+text',
        marker=dict(size=10, color=colormap[i % len(colormap)]),
        text=df['name'][i],
        textposition='top center',
        hovertext=df['hover_text'][i],
        hoverinfo='text',
        showlegend=False  # Disable legend for each trace
    ))

# Define axis colors
protein_color = 'red'
carbohydrates_color = 'blue'
fat_color = 'green'

# Update layout for better visualization
fig.update_layout(
    title='3D Scatter Plot of Fruits by Nutrient Content',
    scene=dict(
        xaxis=dict(title='Protein (g)', titlefont=dict(color=protein_color), tickfont=dict(color=protein_color)),
        yaxis=dict(title='Carbohydrates (g)', titlefont=dict(color=carbohydrates_color), tickfont=dict(color=carbohydrates_color)),
        zaxis=dict(title='Fat (g)', titlefont=dict(color=fat_color), tickfont=dict(color=fat_color))
    ),
    template='plotly_dark',  # Set the dark template
    showlegend=False,  # Disable legend in the layout
    width=1200,
    height=800
)

# Display the plot using Streamlit with specified width and height
st.plotly_chart(fig, use_container_width=True)
