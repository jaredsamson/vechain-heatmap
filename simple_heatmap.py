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
    "Diag": [42.276726, -83.738263],
    "Mason Hall": [42.276963, -83.739479],
    "Hatcher Graduate Library": [42.275745, -83.738663],
    "Shapiro Undergraduate Library": [42.274990, -83.738327],
    "Michigan Union": [42.274360, -83.740810],
    "Angell Hall": [42.276908, -83.737503],
    "West Quadrangle": [42.274849, -83.742630],
    "East Hall": [42.278873, -83.735191],
    "LSA Building": [42.275394, -83.737816],
    "Ross School of Business": [42.273746, -83.735672],
    "North Quad": [42.279320, -83.738121],
    "M36 Coffee Roasters": [42.280220, -83.746384],
    "Chemistry Building": [42.275837, -83.736076],
    "School of Social Work": [42.274593, -83.734856],
    "Hill Auditorium": [42.279964, -83.738190],
    "Law Library": [42.273796, -83.738953],
    "Central Campus Transit Center": [42.275181, -83.735100],
    "Central Campus Classroom Building": [42.274788, -83.734177],
    "Mosher-Jordan Hall": [42.276524, -83.731506],
    "Biological Sciences Building": [42.277725, -83.738571],
    "Michigan League": [42.279217, -83.738808],
    "East Quadrangle": [42.273621, -83.734863],
    "School of Kinesiology": [42.276367, -83.741882],  # Kraus Building
    "South Quadrangle": [42.273281, -83.741264],
    "Pierpont Commons": [42.292473, -83.716690],
    "Duderstadt Center": [42.292141, -83.715233],
    "North Campus Recreation Building (NCRB)": [42.291588, -83.713600],
    "GG Brown Laboratory": [42.292526, -83.710793],
    "Francois-Xavier Bagnoud (FXB) Building": [42.293434, -83.711227],
    "Beyster Building (CSE)": [42.292698, -83.712914],
    "Bob and Betty Beyster Building": [42.293190, -83.713020],
    "Gerald R. Ford Robotics Building": [42.296223, -83.710457],
    "Stamps School of Art & Design": [42.293674, -83.716011],
    "Earl V. Moore Music Building": [42.292355, -83.717819],
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
HeatMap(
    
    heat_data,
    radius=45,         # Increase spread outward
    blur=40,           # Softens the heat edges
    min_opacity=0.4,   # Keeps faint data visible
    max_zoom=17,
    gradient={
    "0.2": 'blue',
    "0.4": 'lime',
    "0.6": 'yellow',
    "0.8": 'orange',
    "1.0": 'red'
}                # So it still works when zoomed in
).add_to(m)


# We need to implement layers for greencart, mugshot, cleanify. 
# Should be simple but we need to update csv file by adding a column for which initiative is this for




title_html = """
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap" rel="stylesheet">
<div style="
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(to right, #ffffff, #f7f9fc);
    padding: 28px 35px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    font-family: 'Public Sans', sans-serif;
    z-index: 9999;
    text-align: center;
    max-width: 1100px;
    width: 95%;
    border: 1px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: space-between;
">

    <!-- Left: Stylized M -->
    <div style="font-family: 'Montserrat', sans-serif; font-size: 60px; font-weight: 800; color: #FFCB05; margin-right: 30px;">
        M
    </div>

    <!-- Center: Text Block -->
    <div style="flex: 1; text-align: center;">
        <h1 style="margin: 0; font-size: 30px; color: #00274C; font-weight: 700;">
            VeBetter Engagement @ University of Michigan
        </h1>
        <p style="margin: 8px 0 0; font-size: 17px; color: #444;">
            Visualizing sustainable action with <strong>VeChain</strong> & <strong>BCG</strong> — powered by <strong>Folium</strong>
        </p>
        <p style="margin: 6px 0 0; font-size: 16px; color: #555;">
            Developed by <strong>Alex Yesilyurt</strong> & <strong>Jared Samson</strong>
        </p>
    </div>

    <!-- Right: Logos -->
    <div style="display: flex; align-items: center; gap: 16px; margin-left: 30px;">
        <a href="https://www.vechain.org/" target="_blank" title="VeChain">
            <img src="https://cdn0.iconfinder.com/data/icons/blockchain-classic/256/VeChain-1024.png" alt="VeChain Logo" style="height: 40px;" />
        </a>
        <a href="https://www.bcg.com/" target="_blank" title="Boston Consulting Group">
            <img src="https://logodix.com/logo/1185315.png" alt="BCG Logo" style="height: 40px;" />
        </a>
    </div>
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

for location, coords in locations.items():
    group = popup_df[popup_df["Where did you scan the QR code?"] == location]

    summary_html = f"""
    <div style="padding: 5px; font-family: 'Public Sans', 'Arial', sans-serif;">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 3px;">📍 {location}</div>
        <div><strong>Total Entries:</strong> {len(group)}</div>
    </div>
    """

    if len(group) > 0:
        html_table = group.to_html(index=False, classes='popup-table', escape=False)
        table_html = f"""
        <div style="max-height: 300px; overflow-y: auto; padding: 5px; border-top: 1px solid #ccc; font-family: 'Public Sans', 'Arial', sans-serif;">
            {html_table}
        </div>
        """
        full_popup_html = summary_html + table_html
    else:
        full_popup_html = summary_html + "<div style='padding: 5px;'>No responses yet.</div>"

    folium.Marker(
        location=coords,
        popup=folium.Popup(full_popup_html, max_width=450),
        tooltip=f"{len(group)} entr{'y' if len(group) == 1 else 'ies'} here",
        icon=folium.Icon(color='gray' if len(group) == 0 else 'blue', icon='info-sign')
    ).add_to(m)


# MiniMap
MiniMap(toggle_display=True).add_to(m)

# Save
map_final_path = "index.html"
m.save(map_final_path)

map_final_path