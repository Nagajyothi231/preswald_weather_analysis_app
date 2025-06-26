# preswald_weather_analysis_app

This project is a data-driven weather visualization app built using **Preswald**, designed to explore and analyze synthetic weather data across ten U.S. cities. It provides visual insights into humidity, temperature, wind, and precipitation patterns using interactive charts and tables.

## 🔧 Tech Stack
- **Preswald** (Data app platform)
- **Python** (data preprocessing)
- **Plotly** (interactive visualizations)
- **SQL** (Preswald integrated queries)

---

## 1️⃣ Project Overview

This app visualizes a synthetic dataset containing 1 million records per feature for cities like New York, Chicago, San Jose, Phoenix, and others. Each record captures:

- `Location`
- `Date_Time`
- `Temperature_C`
- `Humidity_pct`
- `Precipitation_mm`
- `Wind_Speed_kmh`

We engineered additional features like:
- **Month**
- **Season**

---

## 2️⃣ Features Implemented

### 📌 Filtered Weather Data
- Used SQL queries in Preswald to filter humidity levels above 50%.
- Displayed interactive tables for further exploration.

### 🔘 Interactive Humidity Threshold
- Set a default threshold (70%) to display high-humidity records.
- Table updates dynamically based on the defined logic.

### 📈 Temperature vs. Humidity by Location
- Built a bubble chart using Plotly.
- X-axis: Temperature, Y-axis: Humidity.
- Bubble size: Wind Speed.
- Color: City.

### 📅 Monthly Temperature Trends
- Created a line plot of average monthly temperatures.
- Helps visualize seasonal variation by city.

### 📦 Seasonal Precipitation Distribution
- Built a box plot showing precipitation by season.
- Useful to identify rainfall concentration by time and location.

---

## 📤 Deployment & Export Notes

- The app was developed and tested locally using the Preswald dev environment.
