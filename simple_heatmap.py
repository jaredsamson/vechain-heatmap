import pandas as pd
import folium
from folium.plugins import HeatMap
from folium.plugins import MiniMap
from branca.element import MacroElement
from jinja2 import Template
import os

df = pd.read_csv('https://docs.google.com/spreadsheets/d/1xY3zXaY6WSskTJZ7080enB-GZpAnTlTQGSON5i9hp94/export?format=csv')

# Location coordinates
locations = {
    "Diag": [42.2770, -83.7382],
    "M36 Coffee Roasters": [42.2803, -83.7463],
    "East Hall": [42.2803, -83.7382],
    "Shapiro Undergraduate Library": [42.2753, -83.7340],
    "West Quadrangle": [42.2803, -83.7382],
}

df["latitude"] = df["Where did you scan the QR code?"].map(lambda loc: locations.get(loc, (None, None))[0])
df["longitude"] = df["Where did you scan the QR code?"].map(lambda loc: locations.get(loc, (None, None))[1])

lat = locations["Diag"][0]  # Latitude of 'Diag'
lon = locations["Diag"][1]  # Longitude of 'Diag'
adjusted_lat = lat + 0.002  # Increase latitude slightly

# Base map
m = folium.Map(location=[adjusted_lat, lon], zoom_start=16)

# Heatmap with increased radius (spread)
heat_data = df[["latitude", "longitude"]].dropna().values.tolist()
HeatMap(heat_data, 
        radius=30
        ).add_to(m)  # 6x default (default is 10)

# Title with UMich-style font and wider box
title_html = """
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;700&display=swap" rel="stylesheet">
<div style="
    position: fixed;
    top: 10px; left: 50%;
    transform: translateX(-50%);
    background-color: rgba(255, 255, 255, 0.95);
    padding: 15px 25px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    z-index: 9999;
    font-family: 'Public Sans', 'Arial', sans-serif;
    max-width: 1000px;
    width: 95%;
    text-align: center;
">
    <h1 style="margin: 0; font-size: 36px; color: #00274C; font-weight: bold;">
        VeBetter User Data @ University of Michigan
    </h1>
    <p style="margin: 6px 0 0 0; font-size: 19px; color: #333;">
        Live visualization using Folium Heatmap<br>
        Developed by <strong>Alex Yesilyurt</strong> & <strong>Jared Samson</strong> in collaboration with <strong>Boston Consulting Group</strong>.
    </p>
</div>
"""

legend_html = """
<div style="
    position: fixed;
    bottom: 30px; left: 30px; 
    z-index: 9999;
    background-color: white;
    padding: 10px 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    font-family: 'Public Sans', sans-serif;
">
    <div style="font-weight: bold; margin-bottom: 5px;">Heatmap Intensity</div>
    <div style="display: flex; align-items: center;">
        <div style="width: 120px; height: 12px;
                    background: linear-gradient(to right, blue, lime, yellow, orange, red); 
                    margin-right: 10px;">
        </div>
        <div style="font-size: 12px;">Low → High</div>
    </div>
</div>
"""

class AddChild(MacroElement):
    def __init__(self, html):
        super().__init__()
        self._template = Template(f"""
            {{% macro html(this, kwargs) %}}
                {html}
            {{% endmacro %}}
        """)

m.get_root().add_child(AddChild(title_html))
m.get_root().add_child(AddChild(legend_html))

# Popups
popup_df = df.drop(columns=["latitude", "longitude"])

for location, group in popup_df.groupby("Where did you scan the QR code?"):
    coords = locations.get(location)
    if not coords:
        continue

    summary_html = f"""
    <div style="padding: 5px; font-family: 'Public Sans', 'Arial', sans-serif;">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 3px;">📍 {location}</div>
        <div><strong>Total Entries:</strong> {len(group)}</div>
    </div>
    """

    html_table = group.to_html(index=False, classes='popup-table', escape=False)
    table_html = f"""
    <div style="max-height: 300px; overflow-y: auto; padding: 5px; border-top: 1px solid #ccc; font-family: 'Public Sans', 'Arial', sans-serif;">
        {html_table}
    </div>
    """

    full_popup_html = summary_html + table_html

    folium.Marker(
        location=coords,
        popup=folium.Popup(full_popup_html, max_width=450),
        tooltip=f"{len(group)} entr{'y' if len(group)==1 else 'ies'} here",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# MiniMap
MiniMap(toggle_display=True).add_to(m)

# Save
os.makedirs("output", exist_ok=True)
map_final_path = "output/heatmap_umich_final.html"
m.save(map_final_path)

map_final_path