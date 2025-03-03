import pandas as pd
import folium
from folium.plugins import HeatMap

df = pd.read_csv('data/form1_responses.csv')

# Dictionary to map locations to coordinates
locations = {
    "Diag": [42.2770, -83.7382],
    "M36 Coffee Roasters": [42.2803, -83.7463],
    "East Hall": [42.2803, -83.7382],
    "Shapiro Undergraduate Library": [42.2753, -83.7340],
    "West Quadrangle": [42.2803, -83.7382],
}

df["latitude"] = df["Where did you scan the QR code?"].map(lambda loc: locations.get(loc, (None, None))[0])
df["longitude"] = df["Where did you scan the QR code?"].map(lambda loc: locations.get(loc, (None, None))[1])

print(df.head())

# Create a base heatmap centered at The Diag
m = folium.Map(location=locations["Diag"], zoom_start=15)

# Prepare heatmap data
heat_data = df[["latitude", "longitude"]].values.tolist()

# Add heatmap layer
HeatMap(heat_data).add_to(m)

# Save the map
m.save("output/heatmap.html")
