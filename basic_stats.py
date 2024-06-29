import requests
import streamlit as st
import pandas as pd

import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# # streamlit run "C:/Users/Namaste/Desktop/Others/Numa/Machine Learning Projects/fruit_stats/my_streamlit_app.py"
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
st.write("""
# My first app!*
""")
# py -m streamlit run my_streamlit_app.py

response = requests.get("https://www.fruityvice.com/api/fruit/all")

json_data= response.json()



# Extract the necessary information
fruits = json_data
extracted_fruits = []

for fruit in fruits:
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
#
# Create a DataFrame
df_extracted = pd.DataFrame(extracted_fruits)
df=pd.DataFrame(df_extracted)



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
        name=df['name'][i]
    ))

# Update layout for better visualization
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
    legend_title='Fruits',
    width=1200,  # Set the width of the figure
    height=800   # Set the height of the figure
)


# Display the plot using Streamlit with specified width and height
st.plotly_chart(fig, use_container_width=True)