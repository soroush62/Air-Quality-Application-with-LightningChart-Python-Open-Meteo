import requests
import pandas as pd
import time
import lightningchart as lc
from datetime import datetime, timedelta
import pytz
import os
import trimesh

lc.set_license("my-license-key")

LATITUDE = 60.1699
LONGITUDE = 24.9384

AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WIND_API_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
TEMP_API_URL = "https://api.open-meteo.com/v1/forecast"

AIR_QUALITY_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": (
        "pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,"
        "european_aqi,european_aqi_pm2_5,european_aqi_pm10,"
        "european_aqi_nitrogen_dioxide,european_aqi_ozone,european_aqi_sulphur_dioxide,"
        "uv_index,uv_index_clear_sky"
    ),
    "past_days": 1,
    "forecast_days": 1,
    "timezone": "auto",
}

WIND_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "wind_direction_10m",
    "past_days": 1,
    "forecast_days": 1,
    "timezone": "auto",
}

# Weather API for weather_code
WEATHER_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "weather_code,relative_humidity_2m",
    "past_days": 1,
    "forecast_days": 1,
    "timezone": "auto",
}

TEMP_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m",
    "past_days": 1,
    "forecast_days": 1,
    "timezone": "auto",
}

# Set local timezone
local_tz = pytz.timezone("Europe/Helsinki")


# Data Fetching Functions


def fetch_past_air_quality():
    response = requests.get(AIR_QUALITY_API_URL, params=AIR_QUALITY_PARAMS)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data.get("hourly", {}))
    df.rename(columns={"time": "Time"}, inplace=True)
    df["Time"] = (
        pd.to_datetime(df["Time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
    )
    return df


def fetch_past_wind_data():
    response = requests.get(WIND_API_URL, params=WIND_PARAMS)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data.get("hourly", {}))
    df.rename(columns={"time": "Time"}, inplace=True)
    df["Time"] = (
        pd.to_datetime(df["Time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
    )
    return df


def fetch_past_weather_data():
    response = requests.get(WEATHER_API_URL, params=WEATHER_PARAMS)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data.get("hourly", {}))
    df.rename(columns={"time": "Time"}, inplace=True)
    df["Time"] = (
        pd.to_datetime(df["Time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
    )
    return df


def fetch_past_temperature():
    response = requests.get(TEMP_API_URL, params=TEMP_PARAMS)
    response.raise_for_status()
    data = response.json()

    if "hourly" not in data:
        raise ValueError("Unexpected API response: 'hourly' key missing")

    df = pd.DataFrame(data.get("hourly", {}))

    if df.empty:
        raise ValueError("Temperature data is empty")

    df.rename(columns={"time": "Time"}, inplace=True)
    df["Time"] = (
        pd.to_datetime(df["Time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
    )

    print("fetch_past_temperature() returned DataFrame successfully")
    return df


def fetch_real_time_air_quality():
    real_time_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,european_aqi",
        "timezone": "auto",
    }
    response = requests.get(AIR_QUALITY_API_URL, params=real_time_params)
    response.raise_for_status()
    data = response.json()

    # Debugging: Print API response
    print("Real-time air quality response:", data)

    return data.get("current", {})


def fetch_real_time_uv():
    real_time_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "uv_index",
        "timezone": "auto",
    }
    response = requests.get(AIR_QUALITY_API_URL, params=real_time_params)
    response.raise_for_status()
    data = response.json()

    # Debugging: Print API response
    print("Real-time UV API response:", data)

    return data.get("current", {}).get("uv_index", 0.0)


def fetch_real_time_wind():
    real_time_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "wind_direction_10m",
        "timezone": "auto",
    }
    response = requests.get(WIND_API_URL, params=real_time_params)
    response.raise_for_status()
    data = response.json()

    # Debugging: Print API response
    print("Real-time Wind API response:", data)

    return data.get("current", {}).get("wind_direction_10m", 0)


def fetch_real_time_weather():
    real_time_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "weather_code",
        "timezone": "auto",
    }
    response = requests.get(WEATHER_API_URL, params=real_time_params)
    response.raise_for_status()
    data = response.json()

    # Debugging: Print API response
    print("Real-time Weather API response:", data)

    return data.get("current", {}).get("weather_code", 3)


def fetch_real_time_temperature():
    """Fetch real-time temperature and store it by day."""
    real_time_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "temperature_2m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "auto",
    }
    response = requests.get(TEMP_API_URL, params=real_time_params)
    response.raise_for_status()
    data = response.json()

    # Extract hourly temperature data
    hourly_temps = data.get("hourly", {}).get("temperature_2m", [])
    timestamps = data.get("hourly", {}).get("time", [])

    if not hourly_temps or not timestamps:
        return 0.0, 0.0, 0.0

    # Convert timestamps to datetime objects
    date_objects = [datetime.strptime(t, "%Y-%m-%dT%H:%M") for t in timestamps]

    # Group temperatures by day
    temp_by_day = {}
    for i, date_obj in enumerate(date_objects):
        day_str = date_obj.strftime("%Y-%m-%d")
        if day_str not in temp_by_day:
            temp_by_day[day_str] = []
        temp_by_day[day_str].append(hourly_temps[i])

    # Get today's date and ensure we have temperature data for it
    today_str = datetime.now(local_tz).strftime("%Y-%m-%d")
    today_temps = temp_by_day.get(today_str, [])

    if not today_temps:
        return 0.0, 0.0, 0.0  # Default in case today's data is missing

    min_temp, max_temp = min(today_temps), max(today_temps)
    current_temp = today_temps[-1]
    return current_temp, max_temp, min_temp


def fetch_real_time_humidity():
    """Fetch real-time humidity from the API."""
    real_time_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "relative_humidity_2m",
        "timezone": "auto",
    }
    response = requests.get(WEATHER_API_URL, params=real_time_params)
    response.raise_for_status()
    data = response.json()

    # Debugging: Print API response
    print("Real-time Humidity API response:", data)

    return data.get("current", {}).get(
        "relative_humidity_2m", 0.0
    )  # Default to 0.0 if missing


# We use these parameters for the multi-line chart as well as for the radar chart.
pollutants = {
    "pm10": "PM10 (μg/m³)",
    "pm2_5": "PM2.5 (μg/m³)",
    "nitrogen_dioxide": "NO2 (μg/m³)",
    "ozone": "O3 (μg/m³)",
    "carbon_monoxide": "CO (mg/m³)",
}


# Create Dashboard and Charts

dashboard = lc.Dashboard(rows=12, columns=16, theme=lc.Themes.CyberSpace)

# --- Chart 1: Polar Chart for PM2.5 by Wind Direction ---
polar_chart = dashboard.PolarChart(
    column_index=0, row_index=6, row_span=3, column_span=3
)
polar_chart.set_title("PM2.5 Concentration by Wind Direction (Scaled / 5)")

# --- Chart 2: Multi-line Chart for Air Quality Trends ---
line_chart = dashboard.ChartXY(column_index=8, row_index=0, row_span=6, column_span=8)
line_chart.set_title("Air Quality Trends")
line_chart.get_default_y_axis().dispose()
line_chart.get_default_x_axis().set_tick_strategy("DateTime")
legend_line = line_chart.add_legend().set_dragging_mode("draggable")
series_map_line = {}
for i, (key, label) in enumerate(pollutants.items()):
    y_axis = line_chart.add_y_axis(stack_index=i)
    series = line_chart.add_line_series(
        y_axis=y_axis, data_pattern="ProgressiveX"
    ).set_name(label)
    series_map_line[key] = series
    legend_line.add(series)

# --- Chart 3: Area Chart for European AQI Components ---
chart_aqi = dashboard.ChartXY(column_index=3, row_index=6, row_span=6, column_span=5)
chart_aqi.set_title("European AQI Components Over Time")
chart_aqi.get_default_y_axis().dispose()
chart_aqi.get_default_x_axis().set_title("Time").set_tick_strategy("DateTime")
legend_aqi = chart_aqi.add_legend(title="AQI Components").set_dragging_mode("draggable")
series_map_aqi = {}

# AQI components with shorter names for the radar chart
aqi_components = {
    "european_aqi_pm2_5": "PM2.5",
    "european_aqi_pm10": "PM10",
    "european_aqi_nitrogen_dioxide": "NO₂",
    "european_aqi_ozone": "O₃",
    "european_aqi_sulphur_dioxide": "SO₂",
}


for i, (key, label) in enumerate(aqi_components.items()):
    y_axis = chart_aqi.add_y_axis(stack_index=i)
    series = chart_aqi.add_area_series(
        y_axis=y_axis, data_pattern="ProgressiveX"
    ).set_name(label)
    series_map_aqi[key] = series
    legend_aqi.add(series)

# --- Chart 4: Radar (Spider) Chart for Air Pollution Monitoring ---
radar_chart = dashboard.SpiderChart(
    column_index=4, row_index=0, row_span=6, column_span=4
)
radar_chart.set_title("European Air Quality Indicators")
radar_chart.set_axis_label_font(weight="bold", size=12)
legend_radar = radar_chart.add_legend()

# Add shorter axis names
for key, label in aqi_components.items():
    radar_chart.add_axis(label)

series_radar = radar_chart.add_series()
series_radar.set_name("Real-Time Air Quality Data")
# legend_radar.add(data=series_radar)


# --- Chart 5: Guage Chart for European AQI ---
gauge_chart = dashboard.GaugeChart(
    column_index=0, row_index=9, row_span=3, column_span=3
)
gauge_chart.set_title("").add_legend(title="Current UV Index").set_margin(
    right=110, bottom=240
)
gauge_chart.set_angle_interval(start=225, end=-45).set_rounded_edges(False)
gauge_chart.set_unit_label_font(16, weight="bold").set_value_label_font(
    25, weight="bold"
).set_tick_font(23, weight="bold")
gauge_chart.set_interval(start=0, end=12).set_needle_length(30).set_needle_thickness(8)
gauge_chart.set_value_indicators(
    [
        {"start": 0, "end": 2, "color": lc.Color("green")},  # Blue
        {"start": 2, "end": 5, "color": lc.Color("yellow")},  # Cyan
        {"start": 5, "end": 7, "color": lc.Color("orange")},  # Green
        {"start": 7, "end": 10, "color": lc.Color("red")},  # Yellow
        {"start": 10, "end": 12, "color": lc.Color("darkred")},  # Red
    ]
)
gauge_chart.set_value(0).set_bar_thickness(15).set_needle_thickness(7)

# --- Chart 6: Additional Weather Info ChartXY (New) ---
chart_xy = dashboard.ChartXY(row_index=0, column_index=0, column_span=4, row_span=2)
chart_xy.set_title("Weather Info")
chart_xy.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
chart_xy.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
chart_xy.add_point_series().add(0.5, 0.5).set_point_image_style("Image/Stormclouds.jpg")

# Create textboxes and store their references for later updates
location_textbox = (
    chart_xy.add_textbox("Helsinki, Finland", 0.5, 0.75)
    .set_text_font(30, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
date_textbox = (
    chart_xy.add_textbox(datetime.now(local_tz).strftime("%Y-%m-%d"), 0.5, 0.48)
    .set_text_font(26, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
day_textbox = (
    chart_xy.add_textbox(datetime.now(local_tz).strftime("%A"), 0.45, 0.22)
    .set_text_font(17, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
wc_hour_textbox = (
    chart_xy.add_textbox(datetime.now(local_tz).strftime("%H:%M:%S"), 0.58, 0.22)
    .set_text_font(17, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)

# --- Chart 7: 3D Weather Model ---
chart_3d = dashboard.Chart3D(
    row_index=2, column_index=2, column_span=2, row_span=2
).set_title("Weather Condition")

chart_3d.get_default_x_axis().set_tick_strategy("Empty")
chart_3d.get_default_y_axis().set_tick_strategy("Empty")
chart_3d.get_default_z_axis().set_tick_strategy("Empty")
chart_3d.set_camera_location(0, 1, 5)


# --- Chart 8: 3D Temperature Model ---
chart_temp = dashboard.ChartXY(row_index=2, column_index=0, column_span=2, row_span=2)
chart_temp.set_title("Temperature Overview")

# Temperature Labels (High, Low, Current)
high_temp_text = (
    chart_temp.add_textbox("High: --°C", 0.5, 0.8)
    .set_text_font(15, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
low_temp_text = (
    chart_temp.add_textbox("Low: --°C", 0.5, 0.2)
    .set_text_font(15, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
current_temp_text = (
    chart_temp.add_textbox("Current: --°C", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)

# Remove Axis Lines and Labels
chart_temp.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
chart_temp.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)

# --- Chart 9: Air Quality Overview (PM10, PM2.5, AQI) ---
chart_air_quality = dashboard.ChartXY(
    row_index=4, column_index=0, column_span=2, row_span=2
)
chart_air_quality.set_title("Air Quality Overview")

# Air Quality Labels
pm10_text = (
    chart_air_quality.add_textbox("PM10: -- μg/m³", 0.5, 0.8)
    .set_text_font(15, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
pm2_5_text = (
    chart_air_quality.add_textbox("PM2.5: -- μg/m³", 0.5, 0.5)
    .set_text_font(15, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)
aqi_text = (
    chart_air_quality.add_textbox("European AQI: --", 0.5, 0.2)
    .set_text_font(15, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)

# Remove Axis Lines and Labels
chart_air_quality.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
chart_air_quality.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)

# --- Chart 10: 3D Air Quality Model ---
chart_air_quality_3d = dashboard.Chart3D(
    row_index=4, column_index=2, column_span=2, row_span=2
).set_title("Air Quality Condition")

chart_air_quality_3d.get_default_x_axis().set_tick_strategy("Empty")
chart_air_quality_3d.get_default_y_axis().set_tick_strategy("Empty")
chart_air_quality_3d.get_default_z_axis().set_tick_strategy("Empty")
chart_air_quality_3d.set_camera_location(0, 1, 5)

forcasting_text = dashboard.ChartXY(
    row_index=6, column_index=8, row_span=1, column_span=2
).set_title("")
forcasting_text.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
forcasting_text.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
forcasting_text.add_textbox("Hourly Forecast", 0.5, 0.5).set_text_font(
    "20", weight="bold"
).set_stroke(thickness=0, color=lc.Color("black"))

chart_3d_weather = dashboard.Chart3D(
    row_index=7, column_index=8, row_span=1, column_span=1
).set_title("")
object_weather = trimesh.load(
    "D:/Computer Aplication/WorkPlacement/Projects/Project20/Objects/Weekly dash/airquality.obj"
)
chart_3d_weather.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_weather.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_weather.get_default_z_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_weather.set_camera_location(0, 1, 5)
vertices_weather = object_weather.vertices.flatten().tolist()
indices_weather = object_weather.faces.flatten().tolist()
normals_weather = object_weather.vertex_normals.flatten().tolist()
model_weather = chart_3d_weather.add_mesh_model().set_color(lc.Color("white"))
model_weather.set_model_geometry(
    vertices=vertices_weather, indices=indices_weather, normals=normals_weather
)
model_weather.set_scale(20).set_model_location(1, 0.3, 0).set_model_rotation(0, 0, 0)

chart_text_weather = dashboard.ChartXY(
    row_index=7, column_index=9, row_span=1, column_span=1
).set_title("")
chart_text_weather.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_text_weather.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_text_weather.add_textbox("Air Quality", 0.5, 0.5).set_text_font(
    "16", weight="bold"
).set_stroke(thickness=0, color=lc.Color("black"))

# Alert Chart (3D icon for visual alert)
chart_3d_alert = dashboard.Chart3D(
    row_index=10, column_index=8, row_span=1, column_span=1
).set_title("")
object_alert = trimesh.load(
    "D:/Computer Aplication/WorkPlacement/Projects/Project20/Objects/Weekly dash/PM.obj"
)
chart_3d_alert.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_alert.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_alert.get_default_z_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_alert.set_camera_location(0, 1, 5)
vertices_alert = object_alert.vertices.flatten().tolist()
indices_alert = object_alert.faces.flatten().tolist()
normals_alert = object_alert.vertex_normals.flatten().tolist()
model_alert = chart_3d_alert.add_mesh_model().set_color(lc.Color("red"))
model_alert.set_model_geometry(
    vertices=vertices_alert, indices=indices_alert, normals=normals_alert
)
model_alert.set_scale(1.5).set_model_location(1, 0.3, 0).set_model_rotation(90, 0, 0)
chart_alert_alert = dashboard.ChartXY(
    row_index=10, column_index=9, row_span=1, column_span=1
).set_title("")
chart_alert_alert.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_alert.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_alert.add_textbox("PM10", 0.5, 0.5).set_text_font(
    "20", weight="bold"
).set_stroke(thickness=0, color=lc.Color("black"))

# Temperature Chart (3D icon)
chart_3d_temp = dashboard.Chart3D(
    row_index=8, column_index=8, row_span=1, column_span=1
).set_title("")
object_temp = trimesh.load(
    "D:/Computer Aplication/WorkPlacement/Projects/Project20/Objects/Weekly dash/Snowflake.obj"
)
chart_3d_temp.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_temp.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_temp.get_default_z_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_temp.set_camera_location(0, 1, 5)
vertices_temp = object_temp.vertices.flatten().tolist()
indices_temp = object_temp.faces.flatten().tolist()
normals_temp = object_temp.vertex_normals.flatten().tolist()
model_temp = chart_3d_temp.add_mesh_model().set_color(lc.Color("white"))
model_temp.set_model_geometry(
    vertices=vertices_temp, indices=indices_temp, normals=normals_temp
)
model_temp.set_scale(0.4).set_model_location(1, 0.3, 0).set_model_rotation(90, 0, 0)
chart_alert_temp = dashboard.ChartXY(
    row_index=8, column_index=9, row_span=1, column_span=1
).set_title("")
chart_alert_temp.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_temp.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_temp.add_textbox("Temperature", 0.5, 0.5).set_text_font(
    "14", weight="bold"
).set_stroke(thickness=0, color=lc.Color("black"))

# Humidity Chart (3D icon)
chart_3d_humidity = dashboard.Chart3D(
    row_index=9, column_index=8, row_span=1, column_span=1
).set_title("")
object_humidity = trimesh.load(
    "D:/Computer Aplication/WorkPlacement/Projects/Project20/Objects/Weekly dash/humidity.obj"
)
chart_3d_humidity.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_humidity.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_humidity.get_default_z_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_humidity.set_camera_location(0, 1, 5)
vertices_humidity = object_humidity.vertices.flatten().tolist()
indices_humidity = object_humidity.faces.flatten().tolist()
normals_humidity = object_humidity.vertex_normals.flatten().tolist()
model_humidity = chart_3d_humidity.add_mesh_model().set_color(lc.Color(102, 178, 255))
model_humidity.set_model_geometry(
    vertices=vertices_humidity, indices=indices_humidity, normals=normals_humidity
)
model_humidity.set_scale(0.4).set_model_location(1, 0.3, 0).set_model_rotation(0, 0, 0)
chart_alert_humidity = dashboard.ChartXY(
    row_index=9, column_index=9, row_span=1, column_span=1
).set_title("")
chart_alert_humidity.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_humidity.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_humidity.add_textbox("Humidity", 0.5, 0.5).set_text_font(
    "17", weight="bold"
).set_stroke(thickness=0, color=lc.Color("black"))

# Pressure Chart (3D icon)
chart_3d_pressure = dashboard.Chart3D(
    row_index=11, column_index=8, row_span=1, column_span=1
).set_title("")
object_pressure = trimesh.load(
    "D:/Computer Aplication/WorkPlacement/Projects/Project20/Objects/Weekly dash/PM.obj"
)
chart_3d_pressure.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_pressure.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_pressure.get_default_z_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_3d_pressure.set_camera_location(0, 1, 5)
vertices_pressure = object_pressure.vertices.flatten().tolist()
indices_pressure = object_pressure.faces.flatten().tolist()
normals_pressure = object_pressure.vertex_normals.flatten().tolist()
model_pressure = chart_3d_pressure.add_mesh_model().set_color(lc.Color("yellow"))
model_pressure.set_model_geometry(
    vertices=vertices_pressure, indices=indices_pressure, normals=normals_pressure
)
model_pressure.set_scale(0.9).set_model_location(1, 0.3, 0).set_model_rotation(
    90, 0, 30
)
chart_alert_pressure = dashboard.ChartXY(
    row_index=11, column_index=9, row_span=1, column_span=1
).set_title("")
chart_alert_pressure.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_pressure.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    start=0, end=1, stop_axis_after=True
)
chart_alert_pressure.add_textbox("PM2.5", 0.5, 0.5).set_text_font(
    "20", weight="bold"
).set_stroke(thickness=0, color=lc.Color("black"))
current_air_quality_model = None

# ====== Step X: Add Next 6 Hours Text Boxes ======
next_hours_textboxes = []

# Get the current time (for the update; you can update these periodically if needed)
current_dt = datetime.now(local_tz)

for i in range(6):
    hour_chart = dashboard.ChartXY(
        row_index=6, column_index=10 + i, row_span=1, column_span=1
    )
    hour_chart.set_title("")  # No title
    # Remove axis lines and ticks
    hour_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )
    hour_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )

    # Calculate the time for this textbox: next hour, next+1 hour, etc.
    hour_dt = current_dt + timedelta(hours=i + 1)
    hour_textbox = (
        hour_chart.add_textbox(hour_dt.strftime("%H:%M"), 0.5, 0.5)
        .set_text_font(20, weight="bold")
        .set_stroke(thickness=0, color=lc.Color("black"))
    )
    next_hours_textboxes.append(hour_textbox)

# ====== Step X: Create Six Mesh Models for Next 6 Hours AQI ======
next_air_quality_models = []

# Create six 3D charts (Row 7, Columns 10-15)
for i in range(6):
    chart_3d_aqi = dashboard.Chart3D(
        row_index=7, column_index=10 + i, row_span=1, column_span=1
    ).set_title("")
    chart_3d_aqi.get_default_x_axis().set_tick_strategy("Empty")
    chart_3d_aqi.get_default_y_axis().set_tick_strategy("Empty")
    chart_3d_aqi.get_default_z_axis().set_tick_strategy("Empty")
    chart_3d_aqi.set_camera_location(0, 1, 5)

    # Initialize empty model
    model = chart_3d_aqi.add_mesh_model()
    next_air_quality_models.append(model)

# ====== Step X: Create Six Text Boxes for Next 6 Hours Temperature ======
next_temperature_textboxes = []

# Create six text boxes (Row 8, Columns 10-15)
for i in range(6):
    temp_chart = dashboard.ChartXY(
        row_index=8, column_index=10 + i, row_span=1, column_span=1
    )
    temp_chart.set_title("")  # No title
    # Remove axis lines and ticks
    temp_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )
    temp_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )

    # Create a placeholder textbox
    temp_textbox = (
        temp_chart.add_textbox(" -- °C", 0.5, 0.5)
        .set_text_font(20, weight="bold")
        .set_stroke(thickness=0, color=lc.Color("black"))
    )
    next_temperature_textboxes.append(temp_textbox)

# ====== Step X: Create Six Text Boxes for Next 6 Hours Humidity ======
next_humidity_textboxes = []

# Create six text boxes (Row 9, Columns 10-15)
for i in range(6):
    humidity_chart = dashboard.ChartXY(
        row_index=9, column_index=10 + i, row_span=1, column_span=1
    )
    humidity_chart.set_title("")
    # Remove axis lines and ticks
    humidity_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )
    humidity_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )

    # Create a placeholder textbox
    humidity_textbox = (
        humidity_chart.add_textbox(" -- %", 0.5, 0.5)
        .set_text_font(20, weight="bold")
        .set_stroke(thickness=0, color=lc.Color("black"))
    )
    next_humidity_textboxes.append(humidity_textbox)

# ====== Step X: Create Six Text Boxes for Next 6 Hours PM10 ======
next_pm10_textboxes = []

# Create six text boxes (Row 10, Columns 10-15)
for i in range(6):
    pm10_chart = dashboard.ChartXY(
        row_index=10, column_index=10 + i, row_span=1, column_span=1
    )
    pm10_chart.set_title("")  # No title
    # Remove axis lines and ticks
    pm10_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )
    pm10_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )

    # Create a placeholder textbox
    pm10_textbox = (
        pm10_chart.add_textbox(" -- μg/m³", 0.5, 0.5)
        .set_text_font(20, weight="bold")
        .set_stroke(thickness=0, color=lc.Color("black"))
    )
    next_pm10_textboxes.append(pm10_textbox)

# ====== Step X: Create Six Text Boxes for Next 6 Hours PM2.5 ======
next_pm2_5_textboxes = []

# Create six text boxes (Row 11, Columns 10-15)
for i in range(6):
    pm2_5_chart = dashboard.ChartXY(
        row_index=11, column_index=10 + i, row_span=1, column_span=1
    )
    pm2_5_chart.set_title("")  # No title
    # Remove axis lines and ticks
    pm2_5_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )
    pm2_5_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
        0, 1, stop_axis_after=True
    )

    # Create a placeholder textbox
    pm2_5_textbox = (
        pm2_5_chart.add_textbox(" -- μg/m³", 0.5, 0.5)
        .set_text_font(20, weight="bold")
        .set_stroke(thickness=0, color=lc.Color("black"))
    )
    next_pm2_5_textboxes.append(pm2_5_textbox)


def load_mesh_model_air_quality(file_name):
    """Load the 3D mesh model for air quality (happy, sad, smile)."""
    obj_path = f"Objects/air quality/{file_name}"
    if not os.path.exists(obj_path):
        print(f"Missing model file: {obj_path}")
        return None, None, None

    try:
        scene = trimesh.load(obj_path)
        mesh = (
            scene.dump(concatenate=True) if isinstance(scene, trimesh.Scene) else scene
        )
        vertices, indices, normals = (
            mesh.vertices.flatten().tolist(),
            mesh.faces.flatten().tolist(),
            mesh.vertex_normals.flatten().tolist(),
        )
        return vertices, indices, normals
    except Exception as e:
        print(f"Error loading {obj_path}: {e}")
        return None, None, None


def update_next_6_hour_air_quality(aqi_values):
    """Update the six 3D models based on AQI values for the next 6 hours."""
    model_mapping = {
        "happy": "happy.obj",
        "smile": "smile.obj",
        "sad": "sad.obj",
    }

    for i, aqi in enumerate(aqi_values):
        if aqi <= 20:
            model_file = model_mapping["happy"]
            model_color = lc.Color("green")
        elif 21 <= aqi <= 40:
            model_file = model_mapping["smile"]
            model_color = lc.Color("yellow")
        else:
            model_file = model_mapping["sad"]
            model_color = lc.Color("red")

        # Load or reuse the model
        if model_file in mesh_models:
            vertices, indices, normals = mesh_models[model_file]
        else:
            vertices, indices, normals = load_mesh_model_air_quality(model_file)
            if vertices and indices and normals:
                mesh_models[model_file] = (vertices, indices, normals)

        # Update the model in the corresponding chart
        if vertices and indices and normals:
            next_air_quality_models[i].set_model_geometry(
                vertices=vertices, indices=indices, normals=normals
            )
            next_air_quality_models[i].set_scale(1.5).set_model_location(0, 0, 0)
            next_air_quality_models[i].set_color(model_color)

            print(f"Updated Next 6 Hours AQI Model {i + 1}: {model_file} (AQI: {aqi})")
        else:
            print(f"Failed to load 3D model for AQI {aqi} at position {i + 1}")


def update_next_hours(base_time):
    # Round base_time to the start of the hour
    base_time = base_time.replace(minute=0, second=0, microsecond=0)
    for i, tb in enumerate(next_hours_textboxes):
        new_time = (base_time + timedelta(hours=i + 1)).strftime("%H:%M")
        tb.set_text(new_time)


def update_air_quality_3d_model(european_aqi):
    global current_air_quality_model  # Track the current air quality model

    # Select model and color based on AQI range
    if european_aqi <= 20:
        model_file = "happy.obj"
        model_color = lc.Color("green")  # Green for Good Air Quality
    elif 21 <= european_aqi <= 40:
        model_file = "smile.obj"
        model_color = lc.Color("yellow")  # Yellow for Moderate Air Quality
    else:
        model_file = "sad.obj"
        model_color = lc.Color("red")  # Red for Poor Air Quality

    # Check if we already have the model cached
    if model_file in mesh_models:
        vertices, indices, normals = mesh_models[model_file]
    else:
        vertices, indices, normals = load_mesh_model_air_quality(model_file)
        if vertices and indices and normals:
            mesh_models[model_file] = (vertices, indices, normals)  # Cache model

    if vertices and indices and normals:
        if current_air_quality_model is not None:
            current_air_quality_model.dispose()  # Remove old model

        # Create and display new model with color
        current_air_quality_model = chart_air_quality_3d.add_mesh_model()
        current_air_quality_model.set_model_geometry(
            vertices=vertices, indices=indices, normals=normals
        )
        current_air_quality_model.set_scale(0.6).set_model_location(0, 0, 0)

        # Apply selected color
        current_air_quality_model.set_color(model_color)

        print(f"Updated Air Quality Model: {model_file} (AQI: {european_aqi})")
    else:
        print(f"Failed to load 3D model for AQI {european_aqi}")


# Dictionary to Store Loaded Mesh Models
mesh_models = {}


# Function to Load Mesh Model from File
def load_mesh_model(file_name):
    obj_path = f"Objects/weather/{file_name}"  # Change path if necessary
    if not os.path.exists(obj_path):
        print(f"Missing model file: {obj_path}")
        return None, None, None

    try:
        import trimesh  # Ensure trimesh is installed: pip install trimesh

        scene = trimesh.load(obj_path)
        mesh = (
            scene.dump(concatenate=True) if isinstance(scene, trimesh.Scene) else scene
        )
        vertices, indices, normals = (
            mesh.vertices.flatten().tolist(),
            mesh.faces.flatten().tolist(),
            mesh.vertex_normals.flatten().tolist(),
        )
        return vertices, indices, normals
    except Exception as e:
        print(f"Error loading {obj_path}: {e}")
        return None, None, None


def update_next_6_hour_temperatures(temp_values):
    """Update the six temperature text boxes with forecasted values."""
    for i, temp in enumerate(temp_values):
        if isinstance(temp, (int, float)):
            next_temperature_textboxes[i].set_text(f"{temp:.1f} °C")
        else:
            next_temperature_textboxes[i].set_text("-- °C")

    print(f"Updated Next 6 Hours Temperature: {temp_values}")


def update_next_6_hour_humidity(humidity_values):
    """Update the six humidity text boxes with forecasted values."""
    for i, humidity in enumerate(humidity_values):
        if isinstance(humidity, (int, float)):
            next_humidity_textboxes[i].set_text(f"{humidity:.1f} %")
        else:
            next_humidity_textboxes[i].set_text("-- %")

    print(f"Updated Next 6 Hours Humidity: {humidity_values}")


def update_next_6_hour_pm10(pm10_values):
    """Update the six PM10 text boxes with forecasted values."""
    for i, pm10 in enumerate(pm10_values):
        if isinstance(pm10, (int, float)):
            next_pm10_textboxes[i].set_text(f"{pm10:.1f} μg/m³")
        else:
            next_pm10_textboxes[i].set_text("-- μg/m³")

    print(f"Updated Next 6 Hours PM10: {pm10_values}")


def update_next_6_hour_pm2_5(pm2_5_values):
    """Update the six PM2.5 text boxes with forecasted values."""
    for i, pm2_5 in enumerate(pm2_5_values):
        if isinstance(pm2_5, (int, float)):
            next_pm2_5_textboxes[i].set_text(f"{pm2_5:.1f} μg/m³")
        else:
            next_pm2_5_textboxes[i].set_text("-- μg/m³")

    print(f"Updated Next 6 Hours PM2.5: {pm2_5_values}")


# Dictionary Mapping Weather Codes to Models
weather_mapping = {
    0: "Clear sky.obj",
    1: "Mainly clear.obj",
    2: "Partly cloudy.obj",
    3: "Overcast.obj",
    45: "Overcast.obj",
    48: "Overcast.obj",
    51: "drizzle.obj",
    53: "drizzle.obj",
    55: "drizzle.obj",
    56: "drizzle.obj",
    57: "drizzle.obj",
    61: "rainy.obj",
    63: "rainy.obj",
    65: "rainy.obj",
    66: "rainy.obj",
    67: "rainy.obj",
    80: "rainy.obj",
    81: "rainy.obj",
    82: "rainy.obj",
    71: "snow.obj",
    73: "snow.obj",
    75: "snow.obj",
    77: "snow.obj",
    85: "snow.obj",
    86: "snow.obj",
    95: "thunderstorm.obj",
    96: "thunderstorm.obj",
    99: "thunderstorm.obj",
}


# Function to Update 3D Model in Chart3D
def update_weather_3d_model(weather_code):
    global current_3d_model  # Ensure we can update it dynamically

    model_file = weather_mapping.get(weather_code, "Overcast.obj")  # Default: Overcast

    if model_file in mesh_models:
        vertices, indices, normals = mesh_models[model_file]  # Use Cached Model
    else:
        vertices, indices, normals = load_mesh_model(model_file)
        if vertices and indices and normals:
            mesh_models[model_file] = (vertices, indices, normals)  # Store for Reuse

    if vertices and indices and normals:
        if current_3d_model is not None:
            current_3d_model.dispose()  # Remove old model

        # Create and Update New Model
        current_3d_model = chart_3d.add_mesh_model()
        current_3d_model.set_model_geometry(
            vertices=vertices, indices=indices, normals=normals
        )
        current_3d_model.set_scale(1.7).set_model_location(0, 0, 0)
    else:
        print(f"Failed to load 3D model for weather code {weather_code}")


current_3d_model = None


# Historical Data Processing

# Fetch historical data first
past_air_data = fetch_past_air_quality()
past_wind_data = fetch_past_wind_data()
past_weather_data = fetch_past_weather_data()
past_temp_data = fetch_past_temperature()

# Perform sequential merges with a consistent Time column
past_data = (
    past_air_data.merge(past_wind_data, on="Time", how="inner")
    .merge(past_weather_data, on="Time", how="inner")
    .merge(past_temp_data, on="Time", how="inner")
)


def stream_historical_data():
    """Stream historical data hour by hour up to the current time,
    updating charts and the next 6 hours and Weather Condition hour display."""
    last_time = past_data.iloc[0]["Time"]
    current_time = datetime.now(local_tz)
    current_date = current_time.date()
    # current_hour = current_time.hour

    # Group historical temperatures by day for display purposes
    past_data["Date"] = past_data["Time"].dt.date
    temp_by_day = past_data.groupby("Date")["temperature_2m"].apply(list).to_dict()

    # Compute min & max temperatures per day
    min_temps = {date: min(temps) for date, temps in temp_by_day.items()}
    max_temps = {date: max(temps) for date, temps in temp_by_day.items()}

    # Set initial min/max for the first date
    min_temp = min_temps.get(current_date, "N/A")
    max_temp = max_temps.get(current_date, "N/A")

    if isinstance(max_temp, (int, float)):
        high_temp_text.set_text(f"High: {max_temp:.1f}°C")
    else:
        high_temp_text.set_text("High: --°C")
    if isinstance(min_temp, (int, float)):
        low_temp_text.set_text(f"Low: {min_temp:.1f}°C")
    else:
        low_temp_text.set_text("Low: --°C")

    for index, row in past_data.iterrows():
        row_time = row["Time"]
        row_date = row_time.date()
        row_hour = row_time.hour

        # Ensure we iterate fully through yesterday
        if row_date == current_date - timedelta(days=1):
            if row_hour > 23:
                continue

        # Stop processing once we reach the current time
        if row_time >= current_time:
            print("Finished streaming historical data. Switching to real-time updates.")
            return

        # Simulate waiting until this row's timestamp
        while last_time < row_time:
            print(f"Historical Time: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
            last_time += timedelta(hours=1)
            time.sleep(1)

        # If a new day has started, update temperature displays
        if row_date != current_date:
            current_date = row_date
            min_temp = min_temps.get(current_date, "N/A")
            max_temp = max_temps.get(current_date, "N/A")
            if isinstance(max_temp, (int, float)):
                high_temp_text.set_text(f"High: {max_temp:.1f}°C")
            else:
                high_temp_text.set_text("High: --°C")
            if isinstance(min_temp, (int, float)):
                low_temp_text.set_text(f"Low: {min_temp:.1f}°C")
            else:
                low_temp_text.set_text("Low: --°C")
            print(f"Updated Historical High: {max_temp:.1f}°C, Low: {min_temp:.1f}°C")

        # Update current temperature and air quality displays
        temperature = row.get("temperature_2m", None)
        if temperature is not None:
            current_temp_text.set_text(f"Current: {temperature:.1f}°C")
        else:
            current_temp_text.set_text("Current: --°C")

        pm10 = row.get("pm10", "N/A")
        pm2_5 = row.get("pm2_5", "N/A")
        european_aqi = row.get("european_aqi", "N/A")

        if isinstance(pm10, (int, float)):
            pm10_text.set_text(f"PM10: {pm10:.1f} μg/m³")
        else:
            pm10_text.set_text("PM10: -- μg/m³")
        if isinstance(pm2_5, (int, float)):
            pm2_5_text.set_text(f"PM2.5: {pm2_5:.1f} μg/m³")
        else:
            pm2_5_text.set_text("PM2.5: -- μg/m³")
        if isinstance(european_aqi, (int, float)):
            aqi_text.set_text(f"European AQI: {european_aqi}")
        else:
            aqi_text.set_text("European AQI: --")

        # Update Polar Chart
        wind_direction = row["wind_direction_10m"]
        pm2_5_val = row["pm2_5"]
        if wind_direction < 100:
            sector = polar_chart.add_sector()
            sector.set_name(f"PM2.5 {pm2_5_val:.1f} μg/m³")
            sector.set_amplitude_start(0)
            sector.set_amplitude_end(pm2_5_val / 5)
            sector.set_angle_start(260 + wind_direction)
            sector.set_angle_end(290 + wind_direction)
            sector.set_color(lc.Color(0, 207, 255))
            sector.set_stroke(color=lc.Color(0, 161, 255), thickness=1)
        elif wind_direction >= 100:
            sector = polar_chart.add_sector()
            sector.set_name(f"PM2.5 {pm2_5_val:.1f} μg/m³")
            sector.set_amplitude_start(0)
            sector.set_amplitude_end(pm2_5_val / 5)
            sector.set_angle_start(-80 + wind_direction)
            sector.set_angle_end(-100 + wind_direction)
            sector.set_color(lc.Color(0, 207, 255))
            sector.set_stroke(color=lc.Color(0, 161, 255), thickness=1)

        # Update Multi-line Chart
        timestamp = int(row["Time"].timestamp() * 1000)
        for key, series in series_map_line.items():
            if key in row:
                series.add([timestamp], [row[key]])
        line_chart.get_default_x_axis().fit()

        # Update AQI Area Chart
        for key, series in series_map_aqi.items():
            if key in row:
                series.add([timestamp], [row[key]])
        chart_aqi.get_default_x_axis().fit()

        # Update Radar Chart
        radar_data = []
        for key, label in aqi_components.items():
            value = row.get(key, 0)
            radar_data.append({"axis": label, "value": value})
        series_radar.add_points(radar_data)

        # Update UV Index gauge
        uv = row["uv_index"]
        gauge_chart.set_value(uv)

        # Update date, day, and Weather Condition hour display
        date_textbox.set_text(row["Time"].strftime("%Y-%m-%d"))
        day_textbox.set_text(row["Time"].strftime("%A"))
        wc_hour_textbox.set_text(row["Time"].strftime("%H:%M"))

        # Update 3D Weather Model and Air Quality 3D Model
        weather_code = int(row.get("weather_code", 3))
        update_weather_3d_model(weather_code)
        european_aqi_val = int(row.get("european_aqi", 0))
        update_air_quality_3d_model(european_aqi_val)

        print(f"Historical Time: {row['Time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Wind Direction: {wind_direction}, Temp: {temperature:.1f}°C")
        time.sleep(1)
        sector.dispose()

        # Update the "next 6 hours" text boxes using this row's time as the base.
        update_next_hours(row["Time"])

        # Extract the next 6 hours AQI values
        future_aqi_values = [row.get("european_aqi", 0) for _ in range(6)]
        update_next_6_hour_air_quality(future_aqi_values)

        # Extract the next 6 hours temperature values
        future_temp_values = [row.get("temperature_2m", 0) for _ in range(6)]
        update_next_6_hour_temperatures(future_temp_values)

        # Extract the next 6 hours humidity values from historical data
        future_humidity_values = [row.get("relative_humidity_2m", 0) for _ in range(6)]
        update_next_6_hour_humidity(future_humidity_values)

        # Extract the next 6 hours PM10 values from historical data
        future_pm10_values = [row.get("pm10", 0) for _ in range(6)]
        update_next_6_hour_pm10(future_pm10_values)

        # Extract the next 6 hours PM2.5 values from historical data
        future_pm2_5_values = [row.get("pm2_5", 0) for _ in range(6)]
        update_next_6_hour_pm2_5(future_pm2_5_values)

        last_time = row["Time"]


# Global variable to store the current polar sector
current_sector = None
current_radar_series = None


def update_real_time_data():
    global current_sector, current_radar_series

    real_time_air = fetch_real_time_air_quality()
    real_time_uv = fetch_real_time_uv()
    current_temp, high_temp, low_temp = fetch_real_time_temperature()
    real_time_weather = fetch_real_time_weather()
    # print("Real-time air quality data:", real_time_air)
    current_time = datetime.now(local_tz)
    timestamp = int(current_time.timestamp() * 1000)

    # Update date, day, and Weather Condition hour display using the real-time base
    date_textbox.set_text(current_time.strftime("%Y-%m-%d"))
    day_textbox.set_text(current_time.strftime("%A"))
    wc_hour_textbox.set_text(current_time.strftime("%H:%M:%S"))

    try:
        pm10 = float(real_time_air.get("pm10", 0))
        pm2_5 = float(real_time_air.get("pm2_5", 0))
        european_aqi = int(real_time_air.get("european_aqi", 0))
        wind_direction = float(real_time_air.get("wind_direction_10m", 0))
    except (KeyError, ValueError, TypeError):
        pm10, pm2_5, european_aqi, wind_direction = 0, 0, 0, 0

    pm10_text.set_text(f"PM10: {pm10:.1f} μg/m³")
    pm2_5_text.set_text(f"PM2.5: {pm2_5:.1f} μg/m³")
    aqi_text.set_text(f"European AQI: {european_aqi}")

    if current_sector is None:
        current_sector = polar_chart.add_sector()
        # legend_polar.add(current_sector)
    if wind_direction < 100:
        current_sector.set_name(f"PM2.5 {pm2_5:.1f} μg/m³")
        current_sector.set_amplitude_start(0)
        current_sector.set_amplitude_end(pm2_5 / 5)
        current_sector.set_angle_start(wind_direction + 260)
        current_sector.set_angle_end(wind_direction + 290)
        current_sector.set_color(lc.Color(255, 0, 0, 128))
        current_sector.set_stroke(color=lc.Color("white"), thickness=1)
    elif wind_direction >= 100:
        current_sector.set_name(f"PM2.5 {pm2_5:.1f} μg/m³")
        current_sector.set_amplitude_start(0)
        current_sector.set_amplitude_end(pm2_5 / 5)
        current_sector.set_angle_start(-80 + wind_direction)
        current_sector.set_angle_end(-100 + wind_direction)
        current_sector.set_color(lc.Color(255, 0, 0, 128))
        current_sector.set_stroke(color=lc.Color("white"), thickness=1)

    for key, series in series_map_line.items():
        value = float(real_time_air.get(key, 0))
        series.add([timestamp], [value])
    line_chart.get_default_x_axis().fit()

    for key, series in series_map_aqi.items():
        value = float(real_time_air.get(key, 0))
        series.add([timestamp], [value])
    chart_aqi.get_default_x_axis().fit()

    if current_radar_series is None:
        current_radar_series = radar_chart.add_series()
        current_radar_series.set_name("Real-Time Air Quality Data")
        # legend_radar.add(data=current_radar_series)
    # Real-time data update for radar chart with shorter names
    radar_data = []
    for key, label in aqi_components.items():
        value = float(real_time_air.get(key, 0))
        radar_data.append({"axis": label, "value": value})
    series_radar.add_points(radar_data)

    try:
        uv = float(real_time_uv)
    except (KeyError, ValueError, TypeError):
        uv = 0.0
    # print(f"Extracted Real-Time UV Index: {uv}")
    gauge_chart.set_value(uv)

    try:
        weather_code = int(real_time_weather)
    except (KeyError, ValueError, TypeError):
        weather_code = 3
    update_weather_3d_model(weather_code)

    current_temp_text.set_text(f"Current: {current_temp:.1f}°C")
    high_temp_text.set_text(f"High: {high_temp:.1f}°C")
    low_temp_text.set_text(f"Low: {low_temp:.1f}°C")

    print(f"Updated Real-Time Data at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    # print(
    #     f"Wind Direction: {wind_direction}, PM10: {pm10}, PM2.5: {pm2_5}, AQI: {european_aqi}"
    # )

    update_air_quality_3d_model(european_aqi)

    # Update the "next 6 hours" text boxes using the current time as the base.
    update_next_hours(current_time)

    # Generate next 6 hours AQI values using real-time base AQI
    future_aqi_values = [european_aqi for _ in range(6)]
    update_next_6_hour_air_quality(future_aqi_values)

    # Generate next 6 hours temperature values using real-time base temperature
    future_temp_values = [current_temp for _ in range(6)]
    update_next_6_hour_temperatures(future_temp_values)

    # Generate next 6 hours humidity values using real-time base humidity
    real_time_humidity = fetch_real_time_humidity()  # Now we have the function!
    future_humidity_values = [real_time_humidity for _ in range(6)]
    update_next_6_hour_humidity(future_humidity_values)

    # Generate next 6 hours PM10 values using real-time base PM10
    future_pm10_values = [pm10 for _ in range(6)]
    update_next_6_hour_pm10(future_pm10_values)

    # Generate next 6 hours PM2.5 values using real-time base PM2.5
    future_pm2_5_values = [pm2_5 for _ in range(6)]
    update_next_6_hour_pm2_5(future_pm2_5_values)


dashboard.open(live=True)

# Stream historical data until current time:
stream_historical_data()

# Start real-time updates:
while True:
    update_real_time_data()
    time.sleep(0.1)
