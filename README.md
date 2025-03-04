# Air Quality Application with LightningChart Python & Open-Meteo

## Introduction
Based on the importance of air pollution in our life and its impact on health, It is essential to monitor air quality in real-time. This project, "Air Quality Application with LightningChart Python & Open-Meteo," focuses on creating a real-time air quality monitoring dashboard using Python. This application gets data from Open-Meteo’s Air Quality API and uses LightningChart Python for visualization.

## About the Dataset and Open-Meteo
Open-Meteo is a free weather API that provides historical, real-time, and forecast data on weather conditions, air quality, and environmental parameters. The dataset used in this project includes:
- PM10 (Particulate Matter 10)
- PM2.5 (Particulate Matter 2.5)
- Nitrogen Dioxide (NO₂)
- Ozone (O₃)
- Carbon Monoxide (CO)
- Sulfur Dioxide (SO₂)
- UV Index
- Temperature, Humidity, and Wind Direction

By integrating Open-Meteo's API, we can fetch past, current, and future air quality conditions and visualize them using interactive dashboards.

## LightningChart Python
LightningChart Python is a high-performance data visualization library that offers real-time and different interactive charting. It allows the creation of 2D and 3D visualizations that makies it ideal for real-time air quality monitoring.

### Features and Chart Types Used
In this project, we used several LightningChart components:
- **Line Charts**: To show air quality trends over time.
- **Bar Charts**: For displaying historical, current and forecasted pollutant concentrations.
- **Polar Charts**: To analyze PM2.5 by wind direction.
- **Radar Charts**: For comparing multiple air quality parameters in real-time.
- **Gauge Charts**: To display UV index levels.
- **3D Charts**: To visualize weather and air quality conditions.

### Performance Characteristics
LightningChart Python provides:
- Low CPU and memory usage which improves dashboard responsiveness.
- Real-time updates which makes it ideal for monitoring live weather changes.
- GPU acceleration that enables smooth visualization even with large datasets.

## Setting Up the Python Environment
To start working on this project, we need to set up the Python environment with necessary libraries.

### Installing Python and Required Libraries
Before running the project, install Python and the other required libraries using:
```bash
pip install requests pandas pytz lightningchart
```

### Overview of Libraries Used
- **NumPy**: For handling and processing weather data.
- **Pandas**: For handling time-series air quality data
- **Requests**: To fetch data from the Open-Meteo API.
- **Pytz**: For handling timezone conversions
- **Trimesh**: For 3D weather condition models.
- **LightningChart**: To create interactive visualizations.

### Setting Up the Development Environment
1. Set up a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
2. Use **Visual Studio Code (VSCode)** for a streamlined development experience.

---

## Loading and Processing Data
### Fetching Data from Open-Meteo API
We fetch the weather data using the following code:
```python
import requests
import pandas as pd

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 60.1699,
    "longitude": 24.9384,
    "hourly": "pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide",
    "past_days": 1,
    "forecast_days": 1,
    "timezone": "auto"
}
response = requests.get(API_URL, params=params)
data = response.json()
```

### Handling and Preprocessing Data
After fetching data, it is moved into a DataFrame for easier analysis and visualization.
```python
df = pd.DataFrame(data["hourly"])
df["time"] = pd.to_datetime(df["time"])
```

## Visualizing Data with LightningChart
### Creating the Charts
Here are some examples that shows how we created key visualizations:

#### **line chart to display PM10 trends**
```python
import lightningchart as lc

dashboard = lc.Dashboard(rows=6, columns=8, theme=lc.Themes.Dark)
chart = dashboard.ChartXY(column_index=0, row_index=0, column_span=8, row_span=4)
chart.set_title("PM10 Levels Over Time")

series = chart.add_line_series(data_pattern="ProgressiveX")
for index, row in df.iterrows():
    series.add([row["time"].timestamp() * 1000], [row["pm10"]])

dashboard.open()
```

#### **Polar Chart (PM2.5 by Wind Directio**
```python
# Create a dashboard
dashboard = lc.Dashboard(rows=1, columns=1)

# Create a Polar Chart
polar_chart = dashboard.PolarChart(column_index=0, row_index=0)
polar_chart.set_title("PM2.5 Concentration by Wind Direction (Scaled)")

# Generate random wind direction and PM2.5 concentration data
for i in range(8):
    sector = polar_chart.add_sector()
    wind_direction = i * 45  # Simulated wind directions
    pm2_5_val = random.uniform(5, 50)  # Simulated PM2.5 values
    sector.set_name(f"PM2.5 {pm2_5_val:.1f} μg/m³")
    sector.set_amplitude_start(0)
    sector.set_amplitude_end(pm2_5_val / 5)  # Scaled
    sector.set_angle_start(wind_direction - 10)
    sector.set_angle_end(wind_direction + 10)
    sector.set_color(lc.Color(0, 207, 255))
    sector.set_stroke(color=lc.Color(0, 161, 255), thickness=1)

dashboard.open()
```

#### **Radar (Spider) Chart (European Air Quality Indicators)**
```python
# Create a dashboard
dashboard = lc.Dashboard(rows=1, columns=1)

# Create Radar Chart
radar_chart = dashboard.SpiderChart(column_index=0, row_index=0)
radar_chart.set_title("European Air Quality Indicators")

# Define AQI Components
aqi_components = {
    "PM2.5": 30,
    "PM10": 22,
    "NO₂": 15,
    "O₃": 18,
    "SO₂": 10
}

# Add axis labels
for key in aqi_components.keys():
    radar_chart.add_axis(key)

# Add data series
series_radar = radar_chart.add_series()
series_radar.set_name("Current AQI Data")
series_radar.add_points([{"axis": key, "value": value} for key, value in aqi_components.items()])

dashboard.open()
```

#### **Gauge Chart (UV Index)**
```python
# Create a dashboard
dashboard = lc.Dashboard(rows=1, columns=1)

# Create Gauge Chart
gauge_chart = dashboard.GaugeChart(column_index=0, row_index=0)
gauge_chart.set_title("Current UV Index")

# Configure gauge properties
gauge_chart.set_angle_interval(start=225, end=-45)
gauge_chart.set_interval(start=0, end=12)
gauge_chart.set_bar_thickness(15)
gauge_chart.set_value(5)  # Example value
gauge_chart.set_value_indicators([
    {"start": 0, "end": 2, "color": lc.Color("green")},
    {"start": 2, "end": 5, "color": lc.Color("yellow")},
    {"start": 5, "end": 7, "color": lc.Color("orange")},
    {"start": 7, "end": 10, "color": lc.Color("red")},
    {"start": 10, "end": 12, "color": lc.Color("darkred")},
])

dashboard.open()
```

#### **Bar Chart (Air Quality Components like PM10, PM2.5, NO2)**
```python
# Create a dashboard
dashboard = lc.Dashboard(rows=1, columns=1)

# Create a Bar Chart
bar_chart = dashboard.BarChart(column_index=0, row_index=0, vertical=True)
bar_chart.set_title("PM2.5 and PM10 Levels")

# Sample data
categories = ["PM2.5", "PM10", "NO2", "O3", "CO"]
values = [random.uniform(5, 50) for _ in categories]

# Add data to bar chart
data_list = [{"category": cat, "value": val} for cat, val in zip(categories, values)]
bar_chart.set_data(data_list)

dashboard.open()
```

#### **3D Chart (Air Quality Models)**
```python
# Create a dashboard
dashboard = lc.Dashboard(rows=1, columns=1)

# Create 3D Chart
chart_3d = dashboard.Chart3D(row_index=0, column_index=0)
chart_3d.set_title("Air Quality 3D Visualization")

# Load a 3D model (Example: air quality model)
object_air_quality = trimesh.load("path/to/air_quality.obj")  # Replace with actual file path

# Extract model geometry
vertices = object_air_quality.vertices.flatten().tolist()
indices = object_air_quality.faces.flatten().tolist()
normals = object_air_quality.vertex_normals.flatten().tolist()

# Add model to the 3D chart
model_air_quality = chart_3d.add_mesh_model()
model_air_quality.set_model_geometry(vertices=vertices, indices=indices, normals=normals)
model_air_quality.set_scale(1.5).set_model_location(0, 0.3, 0)

dashboard.open()
```

### Customizing Visualizations
LightningChart allows customization such as:
- **Color Palettes**: Used different gradient colors to show better data intensities.
- **Legends & Labels**: Improved readability of weather parameters.

## Conclusion
This project demonstrates how to integrate Open-Meteo’s Air Quality API with LightningChart Python to create real-time environmental monitoring dashboard. By visualizing historical, real-time and forecasted data, users can track air quality trends and make decisions about outdoor activities based on pollution control dashboard.
