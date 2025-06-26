import pandas as pd
from preswald import plotly
import plotly.express as px
from preswald import connect, get_df
from preswald import query
from preswald import table, text
from preswald import slider
    
connect()  # Initialize connection to preswald.toml data sources
df = get_df("weather_data")  # Load data
#df = pd.read_csv('data/weather_data.csv')

df["Humidity_pct"] = pd.to_numeric(df["Humidity_pct"], errors="coerce")
df["Temperature_C"] = pd.to_numeric(df["Temperature_C"], errors="coerce")
df["Wind_Speed_kmh"] = pd.to_numeric(df["Wind_Speed_kmh"], errors="coerce")
df["Precipitation_mm"] = pd.to_numeric(df["Precipitation_mm"], errors="coerce")

df["Date_Time"] = pd.to_datetime(df["Date_Time"], errors="coerce")
df["Month"] = df["Date_Time"].dt.month.astype(int)


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"
df["Season"] = df["Month"].apply(get_season)

text("# Exploring Weather Patterns & Predictions in 10 Locations.")
text("This data contains synthetic weather data generated for ten different locations, including New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia, San Antonio, San Diego, Dallas, and San Jose. The data includes information about temperature, humidity, precipitation, and wind speed, with 1 million data points generated for each parameter.")
text("""## Features
- Location: The city where the weather data was simulated.
- Date_Time: The date and time when the weather data was recorded.
- Temperature_C: The temperature in Celsius at the given location and time.
- Humidity_pct: The humidity in percentage at the given location and time.
- Precipitation_mm: The precipitation in millimeters at the given location and time.
- Wind_Speed_kmh: The wind speed in kilometers per hour at the given location and time.""")

text("## Filtered Weather Data Based on Humidity")
text("This table shows records where humidity exceeds 50%, highlighting conditions that may contribute to discomfort, rainfall likelihood, or reduced air quality in certain regions.")
sql = "SELECT * FROM weather_data WHERE CAST(Humidity_pct AS DOUBLE) > 50"
filtered_df = query(sql, "weather_data")
table(filtered_df, title="Filtered Data")

text("## Interactive Humidity Threshold Filter")
text("Use the slider to dynamically explore regions with humidity levels exceeding the selected threshold. This helps identify areas with consistently high moisture, which can influence weather-related planning, health advisories, or equipment performance.") 

# Create a slider for humidity threshold with default set to 70
threshold = slider("Humidity Threshold (%)", min_val=0, max_val=100, default=70)

# Filter the dataframe based on the slider threshold
filtered_df = df[df["Humidity_pct"] > threshold]

# Display the filtered results
table(
    filtered_df.copy().assign(Date_Time=filtered_df["Date_Time"].astype(str)),
    title=f"Data Where Humidity > {threshold}%"
)

text("## Temperature vs. Humidity by Location")
text("This scatter plot reveals the relationship between temperature and humidity across various locations. Larger point sizes indicate stronger wind speeds, helping uncover how wind dynamics may influence or correlate with localized climate conditions.")
scatter_df = filtered_df.dropna(subset=["Temperature_C", "Humidity_pct", "Wind_Speed_kmh"])
scatter_df["Temperature_C"] = pd.to_numeric(scatter_df["Temperature_C"], errors="coerce")
scatter_df["Humidity_pct"] = pd.to_numeric(scatter_df["Humidity_pct"], errors="coerce")
scatter_df["Wind_Speed_kmh"] = pd.to_numeric(scatter_df["Wind_Speed_kmh"], errors="coerce")

scatter = px.scatter(
    scatter_df,
    x="Temperature_C",
    y="Humidity_pct",
    color="Location",  
    size="Wind_Speed_kmh",  
    title="Temperature vs. Humidity by Location"
)
plotly(scatter)
text("""- High humidity levels (~50 to 90%) dominate across locations.
- Temperature varies widely (even negative), likely due to simulated cold seasons in cities like Chicago and New York.
- Bubble sizes (wind speed) reflect fluctuating weather conditions, adding atmospheric complexity across the U.S.""")


text("## Monthly Temperature Trends by Location")
text("This line plot illustrates the average monthly temperature variations across different locations. It highlights seasonal trends and helps compare how temperature patterns fluctuate throughout the year in diverse geographic regions.")
temp_monthly = df.dropna(subset=["Month", "Temperature_C", "Location"])
# Line plot
temp_line = px.line(
    temp_monthly.groupby(["Location", "Month"])["Temperature_C"].mean().reset_index(),
    x="Month",
    y="Temperature_C",
    color="Location",
    title="Monthly Temperature Trends by Location",
    markers=True
)
plotly(temp_line)
text("""- Most cities maintain stable temperatures (~15°C) across months.
- Dallas shows a drop to ~10°C during Jan to Feb, demonstrating realistic winter season simulation.
- This trend confirms the dataset effectively models seasonal shifts, especially for central U.S. regions.""")


text("## Seasonal Precipitation Distribution by Location")
text("This box plot displays how precipitation levels vary by season across different locations. It helps identify regions with high or low rainfall during specific times of the year, revealing seasonal weather patterns and climate variability.")
precip_seasonal = df.dropna(subset=["Season", "Precipitation_mm", "Location"])
# Box plot
precip_box = px.box(
    precip_seasonal,
    x="Season",
    y="Precipitation_mm",
    color="Location",
    title="Seasonal Precipitation Distribution by Location"
)
plotly(precip_box)
text("""- Only **Winter** and **Spring** are shown due to data covering months 1 to 6 only.
- Los Angeles and Phoenix exhibit greater precipitation variability, consistent with their seasonal climate shifts.
- Uniform box distributions across cities indicate consistent simulation logic and well-balanced data.""")


text("## Final Insights: Weather Data Analysis")
text("""✅ **Variability and Complexity**
The dataset simulates realistic seasonal dynamics:\n- **New York** shows higher temperatures and precipitation in summer, reflecting typical humid subtropical patterns.\n- **Phoenix** simulates cooler, wetter conditions in winter, consistent with its desert climate.
\n These variations enable nuanced climate analysis, making the dataset suitable for examining regional weather patterns and their seasonal behavior.""")
