import lightningchart as lc
import requests
import pandas as pd
import pytz
import time
from datetime import datetime

lc.set_license("my-license-key")

LATITUDE = 60.1699
LONGITUDE = 24.9384
local_tz = pytz.timezone("Europe/Helsinki")


# API Parameters for PM2.5 (Historical & Forecast)

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
API_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "pm2_5",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast PM2.5 data from API
response = requests.get(API_URL, params=API_PARAMS)
response.raise_for_status()
data = response.json()

# Convert PM2.5 API response to DataFrame
df = pd.DataFrame(data.get("hourly", {}))
df["Time"] = pd.to_datetime(df["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
df["Date"] = df["Time"].dt.date
df = df.groupby("Date")["pm2_5"].mean().reset_index()
df = df.dropna(subset=["pm2_5"])
df["Date"] = df["Date"].astype(str)

# ---- Fetch current real-time PM2.5 value ----
REALTIME_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "pm2_5",
    "timezone": "auto",
}
rt_response = requests.get(API_URL, params=REALTIME_PARAMS)
rt_response.raise_for_status()
rt_data = rt_response.json()
current_pm25 = rt_data.get("current", {}).get("pm2_5", None)
print(f"Real-time PM2.5: {current_pm25}")

# Replace today's value (if available) with the current reading.
today_str = str(datetime.now(local_tz).date())
if current_pm25 is not None:
    df.loc[df["Date"] == today_str, "pm2_5"] = current_pm25


# API Parameters for PM10 (Historical & Forecast)
API_PARAMS_PM10 = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "pm10",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast PM10 data from API
response_pm10 = requests.get(API_URL, params=API_PARAMS_PM10)
response_pm10.raise_for_status()
data_pm10 = response_pm10.json()

# Convert PM10 API response to DataFrame
df_pm10 = pd.DataFrame(data_pm10.get("hourly", {}))
df_pm10["Time"] = (
    pd.to_datetime(df_pm10["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
)
df_pm10["Date"] = df_pm10["Time"].dt.date
df_pm10 = df_pm10.groupby("Date")["pm10"].mean().reset_index()
df_pm10 = df_pm10.dropna(subset=["pm10"])
df_pm10["Date"] = df_pm10["Date"].astype(str)

# ---- Fetch current real-time PM10 value ----
REALTIME_PARAMS_PM10 = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "pm10",
    "timezone": "auto",
}
rt_response_pm10 = requests.get(API_URL, params=REALTIME_PARAMS_PM10)
rt_response_pm10.raise_for_status()
rt_data_pm10 = rt_response_pm10.json()
current_pm10 = rt_data_pm10.get("current", {}).get("pm10", None)
print(f"Real-time PM10: {current_pm10}")

if current_pm10 is not None:
    df_pm10.loc[df_pm10["Date"] == today_str, "pm10"] = current_pm10


# API Parameters for nitrogen_dioxide (Historical & Forecast)

API_PARAMS_NO2 = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "nitrogen_dioxide",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast data for nitrogen_dioxide
response_no2 = requests.get(API_URL, params=API_PARAMS_NO2)
response_no2.raise_for_status()
data_no2 = response_no2.json()

# Convert API response to DataFrame for nitrogen_dioxide
df_no2 = pd.DataFrame(data_no2.get("hourly", {}))
df_no2["Time"] = (
    pd.to_datetime(df_no2["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
)
df_no2["Date"] = df_no2["Time"].dt.date
df_no2 = df_no2.groupby("Date")["nitrogen_dioxide"].mean().reset_index()
df_no2 = df_no2.dropna(subset=["nitrogen_dioxide"])
df_no2["Date"] = df_no2["Date"].astype(str)

# ---- Fetch current real-time nitrogen_dioxide value ----
REALTIME_PARAMS_NO2 = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "nitrogen_dioxide",
    "timezone": "auto",
}
rt_response_no2 = requests.get(API_URL, params=REALTIME_PARAMS_NO2)
rt_response_no2.raise_for_status()
rt_data_no2 = rt_response_no2.json()
current_no2 = rt_data_no2.get("current", {}).get("nitrogen_dioxide", None)
print(f"Real-time NO2: {current_no2}")

# Replace today's value (if available) with the current reading.
today_str = str(datetime.now(local_tz).date())
if current_no2 is not None:
    df_no2.loc[df_no2["Date"] == today_str, "nitrogen_dioxide"] = current_no2


# API Parameters for Ozone (Historical & Forecast)
API_PARAMS_OZONE = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "ozone",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast data for ozone
response_ozone = requests.get(API_URL, params=API_PARAMS_OZONE)
response_ozone.raise_for_status()
data_ozone = response_ozone.json()

# Convert API response to DataFrame for ozone
df_ozone = pd.DataFrame(data_ozone.get("hourly", {}))
df_ozone["Time"] = (
    pd.to_datetime(df_ozone["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
)
df_ozone["Date"] = df_ozone["Time"].dt.date
df_ozone = df_ozone.groupby("Date")["ozone"].mean().reset_index()
df_ozone = df_ozone.dropna(subset=["ozone"])
df_ozone["Date"] = df_ozone["Date"].astype(str)

# ---- Fetch current real-time ozone value ----
REALTIME_PARAMS_OZONE = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "ozone",
    "timezone": "auto",
}
rt_response_ozone = requests.get(API_URL, params=REALTIME_PARAMS_OZONE)
rt_response_ozone.raise_for_status()
rt_data_ozone = rt_response_ozone.json()
current_ozone = rt_data_ozone.get("current", {}).get("ozone", None)
print(f"Real-time Ozone: {current_ozone}")

# Replace today's ozone value with the current reading if available.
if current_ozone is not None:
    df_ozone.loc[df_ozone["Date"] == today_str, "ozone"] = current_ozone


# API Parameters for carbon_monoxide (Historical & Forecast)

API_PARAMS_CO = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "carbon_monoxide",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast data for carbon_monoxide
response_co = requests.get(API_URL, params=API_PARAMS_CO)
response_co.raise_for_status()
data_co = response_co.json()

# Convert API response to DataFrame for carbon_monoxide
df_co = pd.DataFrame(data_co.get("hourly", {}))
df_co["Time"] = (
    pd.to_datetime(df_co["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
)
df_co["Date"] = df_co["Time"].dt.date
df_co = df_co.groupby("Date")["carbon_monoxide"].mean().reset_index()
df_co = df_co.dropna(subset=["carbon_monoxide"])
df_co["Date"] = df_co["Date"].astype(str)

# ---- Fetch current real-time carbon_monoxide value ----
REALTIME_PARAMS_CO = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "carbon_monoxide",
    "timezone": "auto",
}
rt_response_co = requests.get(API_URL, params=REALTIME_PARAMS_CO)
rt_response_co.raise_for_status()
rt_data_co = rt_response_co.json()
current_co = rt_data_co.get("current", {}).get("carbon_monoxide", None)
print(f"Real-time CO: {current_co}")

# Replace today's value (if available) with the current reading.
today_str = str(datetime.now(local_tz).date())
if current_co is not None:
    df_co.loc[df_co["Date"] == today_str, "carbon_monoxide"] = current_co

# API Parameters for sulphur_dioxide (Historical & Forecast)

API_PARAMS_SO2 = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "sulphur_dioxide",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast data for sulphur_dioxide
response_so2 = requests.get(API_URL, params=API_PARAMS_SO2)
response_so2.raise_for_status()
data_so2 = response_so2.json()

# Convert API response to DataFrame for sulphur_dioxide
df_so2 = pd.DataFrame(data_so2.get("hourly", {}))
df_so2["Time"] = (
    pd.to_datetime(df_so2["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
)
df_so2["Date"] = df_so2["Time"].dt.date
df_so2 = df_so2.groupby("Date")["sulphur_dioxide"].mean().reset_index()
df_so2 = df_so2.dropna(subset=["sulphur_dioxide"])
df_so2["Date"] = df_so2["Date"].astype(str)

# ---- Fetch current real-time sulphur_dioxide value ----
REALTIME_PARAMS_SO2 = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "sulphur_dioxide",
    "timezone": "auto",
}
rt_response_so2 = requests.get(API_URL, params=REALTIME_PARAMS_SO2)
rt_response_so2.raise_for_status()
rt_data_so2 = rt_response_so2.json()
current_so2 = rt_data_so2.get("current", {}).get("sulphur_dioxide", None)
print(f"Real-time SO₂: {current_so2}")

# Replace today's value with the current reading if available.
today_str = str(datetime.now(local_tz).date())
if current_so2 is not None:
    df_so2.loc[df_so2["Date"] == today_str, "sulphur_dioxide"] = current_so2

# API Parameters for uv_index (Historical & Forecast)
API_PARAMS_UV = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "uv_index",
    "past_days": 7,
    "forecast_days": 7,
    "timezone": "auto",
}

# Fetch historical & forecast data for uv_index
response_uv = requests.get(API_URL, params=API_PARAMS_UV)
response_uv.raise_for_status()
data_uv = response_uv.json()

# Convert API response to DataFrame for uv_index
df_uv = pd.DataFrame(data_uv.get("hourly", {}))
df_uv["Time"] = (
    pd.to_datetime(df_uv["time"]).dt.tz_localize("UTC").dt.tz_convert(local_tz)
)
df_uv["Date"] = df_uv["Time"].dt.date
df_uv = df_uv.groupby("Date")["uv_index"].mean().reset_index()
df_uv = df_uv.dropna(subset=["uv_index"])
df_uv["Date"] = df_uv["Date"].astype(str)

# ---- Fetch current real-time uv_index value ----
REALTIME_PARAMS_UV = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "uv_index",
    "timezone": "auto",
}
rt_response_uv = requests.get(API_URL, params=REALTIME_PARAMS_UV)
rt_response_uv.raise_for_status()
rt_data_uv = rt_response_uv.json()
current_uv = rt_data_uv.get("current", {}).get("uv_index", None)
print(f"Real-time uv_index: {current_uv}")

# Replace today's value with the current reading if available.
today_str = str(datetime.now(local_tz).date())
if current_uv is not None:
    df_uv.loc[df_uv["Date"] == today_str, "uv_index"] = current_uv

dashboard = lc.Dashboard(rows=8, columns=6, theme=lc.Themes.Dark)


# Create Bar Chart for PM2.5 (Row 1)
chart = dashboard.BarChart(
    column_index=0,
    row_index=1,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart.set_title("")
chart.set_sorting("disabled")


# Create a new ChartXY in row 1, column 5 to show min and max PM2.5
min_max_pm25_chart = dashboard.ChartXY(
    column_index=5,
    row_index=1,
    column_span=1,
    row_span=1,
).set_title("PM2.5 Min/Max")
min_max_pm25_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
min_max_pm25_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)

# Create a text box that shows "Min: --" on the first line and "Max: --" on the second.
min_max_pm25_textbox = (
    min_max_pm25_chart.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


# Create European AQI Box (Row 1, Column 0)

european_aqi_box = dashboard.ChartXY(
    column_index=0,
    row_index=0,
    column_span=1,
    row_span=1,
).set_title("European AQI Index")
european_aqi_box.get_default_x_axis().set_interval(
    0, 1, stop_axis_after=True
).set_tick_strategy("Empty")
european_aqi_box.get_default_y_axis().set_interval(
    0, 1, stop_axis_after=True
).set_tick_strategy("Empty")
european_aqi_box_series = european_aqi_box.add_rectangle_series()
european_aqi_box_series.add(0, 0, 1, 1).set_color(lc.Color("green"))
european_aqi_textbox = european_aqi_box.add_textbox("0", 0.5, 0.5).set_text_font(
    60, weight="bold"
)
european_aqi_box.add_point_series().add(0.5, 0.5).set_point_image_style(
    "Image/Stormclouds.jpg"
)


def update_pm2_5_minmax_box():
    # Here we compute overall min and max:
    min_pm = df["pm2_5"].min()
    max_pm = df["pm2_5"].max()
    min_max_pm25_textbox.set_text(f"Min: {min_pm:.1f}\nMax: {max_pm:.1f}").set_stroke(
        color=lc.Color("black"), thickness=0
    )


# --- New: City, Date & Time Text Box in First Row, Second Column ---
city_date_time_chart = dashboard.ChartXY(
    column_index=1,  # Second column (0-indexed)
    row_index=0,  # First row (0-indexed)
    column_span=5,
    row_span=1,
).set_title("")
city_date_time_chart.add_point_series().add(0.5, 0.5).set_point_image_style(
    "Image/Stormclouds.jpg"
)
# Remove axis lines and ticks for a clean look.
city_date_time_chart.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
city_date_time_chart.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)

# Create a text box that shows "Helsinki, Finland" along with the current day, date and time.
city_date_time_textbox = (
    city_date_time_chart.add_textbox(
        "",
        0.45,
        0.5,
    )
    .set_text(
        f"Helsinki, Finland - {datetime.now(local_tz).strftime('%A, %Y-%m-%d %H:%M:%S')}"
    )
    .set_stroke(thickness=0, color=lc.Color("black"))
    .set_text_font(60, weight="bold")
)


# NEW: Create PM10 Bar Chart (Row 2) and a Min/Max PM10 Text Box

chart_pm10 = dashboard.BarChart(
    column_index=0,
    row_index=2,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart_pm10.set_title("")
chart_pm10.set_sorting("disabled")

pm10_minmax_box = dashboard.ChartXY(
    column_index=5,
    row_index=2,
    column_span=1,
    row_span=1,
).set_title("PM10 Min/Max")
pm10_minmax_box.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
pm10_minmax_box.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
pm10_minmax_textbox = (
    pm10_minmax_box.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


def update_pm10_minmax_box():
    min_pm10 = df_pm10["pm10"].min()
    max_pm10 = df_pm10["pm10"].max()
    pm10_minmax_textbox.set_text(
        f"Min: {min_pm10:.1f}\nMax: {max_pm10:.1f}"
    ).set_stroke(color=lc.Color("black"), thickness=0)


# Create Bar Chart for Nitrogen Dioxide (Row 3)

chart_no2 = dashboard.BarChart(
    column_index=0,
    row_index=3,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart_no2.set_title("")
chart_no2.set_sorting("disabled")

# Create a new ChartXY for min/max nitrogen_dioxide values in row 3, column 5
no2_minmax_box = dashboard.ChartXY(
    column_index=5,
    row_index=3,
    column_span=1,
    row_span=1,
).set_title("NO₂ Min/Max")
no2_minmax_box.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
no2_minmax_box.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
no2_minmax_textbox = (
    no2_minmax_box.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


def update_no2_minmax_box():
    min_no2 = df_no2["nitrogen_dioxide"].min()
    max_no2 = df_no2["nitrogen_dioxide"].max()
    no2_minmax_textbox.set_text(f"Min: {min_no2:.1f}\nMax: {max_no2:.1f}").set_stroke(
        color=lc.Color("black"), thickness=0
    )


# Create Bar Chart for Ozone (Row 4)

chart_ozone = dashboard.BarChart(
    column_index=0,
    row_index=4,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart_ozone.set_title("")
chart_ozone.set_sorting("disabled")

# Create a new ChartXY for min/max ozone values in row 4, column 5
ozone_minmax_box = dashboard.ChartXY(
    column_index=5,
    row_index=4,
    column_span=1,
    row_span=1,
).set_title("Ozone Min/Max")
ozone_minmax_box.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
ozone_minmax_box.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
ozone_minmax_textbox = (
    ozone_minmax_box.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


def update_ozone_minmax_box():
    min_ozone = df_ozone["ozone"].min()
    max_ozone = df_ozone["ozone"].max()
    ozone_minmax_textbox.set_text(
        f"Min: {min_ozone:.1f}\nMax: {max_ozone:.1f}"
    ).set_stroke(color=lc.Color("black"), thickness=0)


# Create Bar Chart for Carbon Monoxide (Row 5)

chart_co = dashboard.BarChart(
    column_index=0,
    row_index=5,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart_co.set_title("")
chart_co.set_sorting("disabled")

# Create a new ChartXY for min/max carbon_monoxide values in row 5, column 5
co_minmax_box = dashboard.ChartXY(
    column_index=5,
    row_index=5,
    column_span=1,
    row_span=1,
).set_title("CO Min/Max")
co_minmax_box.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
co_minmax_box.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
co_minmax_textbox = (
    co_minmax_box.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


def update_co_minmax_box():
    min_co = df_co["carbon_monoxide"].min()
    max_co = df_co["carbon_monoxide"].max()
    co_minmax_textbox.set_text(f"Min: {min_co:.1f}\nMax: {max_co:.1f}").set_stroke(
        color=lc.Color("black"), thickness=0
    )


# Create Bar Chart for Sulphur Dioxide (Row 6)

chart_so2 = dashboard.BarChart(
    column_index=0,
    row_index=6,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart_so2.set_title("")
chart_so2.set_sorting("disabled")

# Create a new ChartXY for min/max sulphur_dioxide values in row 6, column 5
so2_minmax_box = dashboard.ChartXY(
    column_index=5,
    row_index=6,
    column_span=1,
    row_span=1,
).set_title("SO₂ Min/Max")
so2_minmax_box.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
so2_minmax_box.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
so2_minmax_textbox = (
    so2_minmax_box.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


def update_so2_minmax_box():
    min_so2 = df_so2["sulphur_dioxide"].min()
    max_so2 = df_so2["sulphur_dioxide"].max()
    so2_minmax_textbox.set_text(f"Min: {min_so2:.1f}\nMax: {max_so2:.1f}").set_stroke(
        color=lc.Color("black"), thickness=0
    )


# Create Bar Chart for uv_index (Row 7)

chart_uv = dashboard.BarChart(
    column_index=0,
    row_index=7,
    column_span=5,
    row_span=1,
    vertical=True,
    axis_type="linear",
)
chart_uv.set_title("")
chart_uv.set_sorting("disabled")

uv_minmax_box = dashboard.ChartXY(
    column_index=5,
    row_index=7,
    column_span=1,
    row_span=1,
).set_title("UV Min/Max")
uv_minmax_box.get_default_x_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
uv_minmax_box.get_default_y_axis().set_tick_strategy("Empty").set_interval(
    0, 1, stop_axis_after=True
)
uv_minmax_textbox = (
    uv_minmax_box.add_textbox("Min: --\nMax: --", 0.5, 0.5)
    .set_text_font(20, weight="bold")
    .set_stroke(thickness=0, color=lc.Color("black"))
)


def update_uv_minmax_box():
    min_uv = df_uv["uv_index"].min()
    max_uv = df_uv["uv_index"].max()
    uv_minmax_textbox.set_text(f"Min: {min_uv:.1f}\nMax: {max_uv:.1f}").set_stroke(
        color=lc.Color("black"), thickness=0
    )


def stream_pm25_data():
    data_list = []
    for index, row in df.iterrows():
        pm_value = row["pm2_5"]
        date_label = row["Date"]

        if pm_value <= 12:
            bar_color = lc.Color("green")
        elif 12 < pm_value <= 35:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": pm_value})
        chart.set_data(data_list)
        chart.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - PM2.5: {pm_value:.1f} µg/m³")
        # Update European AQI box
        update_european_aqi_box()
        update_pm2_5_minmax_box()
        time.sleep(0.2)


def update_european_aqi_box():
    realtime_params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "european_aqi",
        "timezone": "auto",
    }
    try:
        response = requests.get(API_URL, params=realtime_params)
        response.raise_for_status()
        data = response.json()
        current_eaqi = data.get("current", {}).get("european_aqi", 0)
    except Exception as e:
        print(f"Error fetching European AQI: {e}")
        current_eaqi = 0

    european_aqi_textbox.set_text(f"{current_eaqi}").set_stroke(
        color=lc.Color("black"), thickness=0
    )

    if current_eaqi <= 20:
        color = lc.Color("green")
    elif 21 <= current_eaqi <= 40:
        color = lc.Color("yellow")
    else:
        color = lc.Color("red")

    european_aqi_box_series.clear()
    european_aqi_box_series.add(0, 0, 1, 1).set_color(color)


def stream_pm10_data():
    data_list = []
    for index, row in df_pm10.iterrows():
        pm_value = row["pm10"]
        date_label = row["Date"]

        if pm_value <= 12:
            bar_color = lc.Color("green")
        elif pm_value <= 35:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": pm_value})
        chart_pm10.set_data(data_list)
        chart_pm10.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - PM10: {pm_value:.1f} µg/m³")
        update_pm10_minmax_box()
        time.sleep(0.2)


def stream_no2_data():
    data_list = []
    for index, row in df_no2.iterrows():
        no2_value = row["nitrogen_dioxide"]
        date_label = row["Date"]

        if no2_value <= 40:
            bar_color = lc.Color("green")
        elif no2_value <= 100:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": no2_value})
        chart_no2.set_data(data_list)
        chart_no2.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - NO₂: {no2_value:.1f} µg/m³")
        update_no2_minmax_box()
        time.sleep(0.2)


def stream_ozone_data():
    data_list = []
    for index, row in df_ozone.iterrows():
        ozone_value = row["ozone"]
        date_label = row["Date"]

        if ozone_value <= 70:
            bar_color = lc.Color("green")
        elif ozone_value <= 100:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": ozone_value})
        chart_ozone.set_data(data_list)
        chart_ozone.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - Ozone: {ozone_value:.1f}")
        update_ozone_minmax_box()
        time.sleep(0.2)


def stream_co_data():
    data_list = []
    for index, row in df_co.iterrows():
        co_value = row["carbon_monoxide"]
        date_label = row["Date"]
        if co_value <= 10000:
            bar_color = lc.Color("green")
        elif co_value <= 40000:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": co_value})
        chart_co.set_data(data_list)
        chart_co.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - CO: {co_value:.1f} ppm")
        update_co_minmax_box()
        time.sleep(0.2)


def stream_so2_data():
    data_list = []
    for index, row in df_so2.iterrows():
        so2_value = row["sulphur_dioxide"]
        date_label = row["Date"]

        if so2_value <= 10:
            bar_color = lc.Color("green")
        elif so2_value <= 30:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": so2_value})
        chart_so2.set_data(data_list)
        chart_so2.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - SO₂: {so2_value:.1f} µg/m³")
        update_so2_minmax_box()
        time.sleep(0.2)


def stream_uv_data():
    data_list = []
    for index, row in df_uv.iterrows():
        uv_value = row["uv_index"]
        date_label = row["Date"]

        if uv_value <= 2:
            bar_color = lc.Color("green")
        elif uv_value <= 5:
            bar_color = lc.Color("yellow")
        else:
            bar_color = lc.Color("red")

        data_list.append({"category": date_label, "value": uv_value})
        chart_uv.set_data(data_list)
        chart_uv.set_bar_color(date_label, bar_color)
        print(f"Updated {date_label} - UV Index: {uv_value:.1f}")
        update_uv_minmax_box()
        time.sleep(0.2)


dashboard.open(live=True)
stream_pm25_data()
stream_pm10_data()
stream_no2_data()
stream_ozone_data()
stream_co_data()
stream_so2_data()
stream_uv_data()
