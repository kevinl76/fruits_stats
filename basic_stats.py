import requests
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

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
            'calories': fruit['nutritions']['calories'],
            'fat': fruit['nutritions']['fat'],
            'sugar': fruit['nutritions']['sugar'],
            'carbohydrates': fruit['nutritions']['carbohydrates'],
            'protein': fruit['nutritions']['protein']
        }
        extracted_fruits.append(event_info)

# Create a DataFrame
df = pd.DataFrame(extracted_fruits)

# Create a multiselect menu for fruit selection
options = st.multiselect(
    'Select fruits to display',
    df['name'].unique()
)

# Display the selected options
st.write("You selected:", options)

if options:
    # Filter the DataFrame based on the selected fruits
    selected_fruits = df[df['name'].isin(options)]

    # Create radar chart for the selected fruits
    fig = go.Figure()

    for i, row in selected_fruits.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[ row['fat'], row['sugar'], row['carbohydrates'], row['protein']],
            theta=[ 'Fat', 'Sugar', 'Carbohydrates', 'Protein'],
            fill='toself',
            name=row['name']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(df['fat'].max(), df['sugar'].max(), df['carbohydrates'].max(), df['protein'].max())]
            )
        ),
        showlegend=True,
        template='ggplot2',  # Set the dark template
        title='Nutritional Content of Selected Fruits'
    )

    # Display the radar chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please select at least one fruit to display the chart.")
