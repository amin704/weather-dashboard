# streamlit_weather_dashboard_v2.py
# -*- coding: utf-8 -*-
"""
Bilingual (FA/EN) Streamlit Weather Dashboard for WeatherAPI.com
"""

import io
import time
from datetime import datetime
from collections import defaultdict

import requests
import pandas as pd
import streamlit as st

# TRANSLATION DICTIONARY
T = {
    "en": {
        "title": "🌦️ Weather Dashboard",
        "about": "Enter your API key (from WEATHERAPI.COM), add one or more locations, then fetch current weather and a 3-day forecast. Export forecast to Excel.",
        "api_key": "API Key", "api_key_help": "Your WeatherAPI.com key will be kept only in this session.",
        "units": "Units", "units_metric": "Metric (°C, kph)", "units_imperial": "Imperial (°F, mph)",
        "fields_current": "Select Fields (Current)", "fields_forecast": "Select Fields (Forecast)",
        "fetch": "🌤️ Get Weather", "current": "Current Weather",
        "forecast": "3-Day Forecast (Daily)", "download": "📥 Download Forecast to Excel",
        "error_api": "Please enter a valid API key in the sidebar.",
        "error_no_locs": "Please add at least one location.", "error_fetch": "Fetch error",
        "error_401_key": "Invalid API Key. Please check it in the sidebar.",
        "error_400_loc": "Location not found. Please check the name.",
        "error_connect": "Connection error. Please check your internet connection.",
        "error_http": "HTTP Error",
        "error_unexpected": "An unexpected error occurred",
        "add_row": "➕ Add New Location",
        "col_city": "🏙️ City", "col_region": "Region", "col_country": "Country", "col_lat": "Lat", "col_lon": "Lon",
        "col_temp": "🌡️ Temp", "col_feels": "Feels Like", "col_hum": "💧 Humidity (%)",
        "col_wind": "🌬️ Wind", "col_press": "Pressure (mb)", "col_clouds": "☁️ Cloud Cover (%)",
        "col_cond": "⛅ Condition", "col_dt": "Local Time", "col_sunrise": "🌅 Sunrise",
        "col_sunset": "🌇 Sunset", "col_visibility": "Visibility (km)", "col_uv": "UV Index",
        "fc_date": "Date", "fc_tmax": "🌡️ T-max", "fc_tmin": "🌡️ T-min",
        "fc_tavg": "🌡️ T-avg", "fc_hum": "💧 Avg Humidity (%)", "fc_wind": "🌬️ Max Wind",
        "fc_rain": "🌧️ Chance of Rain (%)", "fc_snow": "❄️ Chance of Snow (%)",
        "tbl_name": "Name (city)", "tbl_saved": "Locations",
        "tip_mix": "Tip: enter city name or coordinates.",
    },
    "fa": {
        "title": "🌦️ داشبورد آب‌ وهوا",
        "about": "کلید API را وارد کنید (از سایت weatherapi.com)، مکان‌ها را اضافه کنید، سپس وضعیت کنونی و پیش‌بینی ۳ روزه را دریافت کرده و خروجی اکسل دانلود کنید.",
        "api_key": "کلید API", "api_key_help": "کلید شما فقط در همین نشست نگه‌داری می‌شود.",
        "units": "واحد", "units_metric": "متریک (°C، kph)", "units_imperial": "امپریال (°F، mph)",
        "fields_current": "اطلاعات (لحظه‌ای)", "fields_forecast": "اطلاعات (پیش‌بینی)",
        "fetch": "🌤️ دریافت اطلاعات", "current": "وضعیت هوا در این لحظه",
        "forecast": "پیش‌بینی ۳ روزه (روزانه)", "download": "📥 دانلود پیش‌بینی (اکسل)",
        "error_api": "لطفاً یک کلید API معتبر در سایدبار وارد کنید.",
        "error_no_locs": "لطفاً حداقل یک مکان اضافه کنید.", "error_fetch": "خطا در دریافت",
        "error_401_key": "کلید API نامعتبر است. لطفاً آن را در سایدبار بررسی کنید.",
        "error_400_loc": "مکان وارد شده پیدا نشد. لطفاً نام آن را بررسی کنید.",
        "error_connect": "خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید.",
        "error_http": "خطای HTTP",
        "error_unexpected": "یک خطای پیش‌بینی نشده رخ داد",
        "add_row": "➕ افزودن مکان جدید",
        "col_city": "🏙️ شهر", "col_region": "منطقه", "col_country": "کشور", "col_lat": "عرض", "col_lon": "طول",
        "col_temp": "🌡️ دما", "col_feels": "دمای احساسی", "col_hum": "💧 رطوبت (%)",
        "col_wind": "🌬️ باد", "col_press": "فشار (mb)", "col_clouds": "☁️ پوشش ابر (%)",
        "col_cond": "⛅ وضعیت", "col_dt": "ساعت محلی", "col_sunrise": "🌅 طلوع",
        "col_sunset": "🌇 غروب", "col_visibility": "میزان دید (کیلومتر)", "col_uv": "شاخص UV",
        "fc_date": "تاریخ", "fc_tmax": "🌡️ بیشینه دما", "fc_tmin": "🌡️ کمینه دما",
        "fc_tavg": "🌡️ میانگین دما", "fc_hum": "💧 میانگین رطوبت (%)", "fc_wind": "🌬️ بیشینه باد",
        "fc_rain": "🌧️ احتمال باران (%)", "fc_snow": "❄️ احتمال برف (%)",
        "tbl_name": "نام (شهر)", "tbl_saved": "مکان‌ها",
        "tip_mix": "نکته: نام شهر یا مختصات را وارد کنید.",
    },
}





WEATHERAPI_BASE = "http://api.weatherapi.com/v1"

@st.cache_data(ttl=600, show_spinner=False)
def fetch_forecast(api_key: str, q: str):
    url = f"{WEATHERAPI_BASE}/forecast.json"
    params = {"key": api_key, "q": q, "days": 3}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def parse_current_row(lang: str, js: dict, units: str):
    t = T[lang]
    loc = js.get("location", {})
    cur = js.get("current", {})
    
    row = {
        t["col_city"]: loc.get("name"),
        t["col_region"]: loc.get("region"),
        t["col_country"]: loc.get("country"),
        t["col_lat"]: loc.get("lat"),
        t["col_lon"]: loc.get("lon"),
        t["col_temp"]: cur.get("temp_c") if units == "metric" else cur.get("temp_f"),
        t["col_feels"]: cur.get("feelslike_c") if units == "metric" else cur.get("feelslike_f"),
        t["col_hum"]: cur.get("humidity"),
        t["col_wind"]: cur.get("wind_kph") if units == "metric" else cur.get("wind_mph"),
        t["col_press"]: cur.get("pressure_mb"),
        t["col_clouds"]: cur.get("cloud"),
        t["col_cond"]: cur.get("condition", {}).get("text"),
        t["col_visibility"]: cur.get("vis_km") if units == "metric" else cur.get("vis_miles"),
        t["col_uv"]: cur.get("uv"),
        t["col_dt"]: loc.get("localtime"),
    }
    return row

def parse_daily_forecast(lang: str, js: dict, units: str):
    t = T[lang]
    loc = js.get("location", {})
    forecast_days = js.get("forecast", {}).get("forecastday", [])
    
    rows = []
    for day_data in forecast_days:
        day = day_data.get("day", {})
        astro = day_data.get("astro", {})
        row = {
            t["col_city"]: loc.get("name"),
            t["fc_date"]: day_data.get("date"),
            t["fc_tmax"]: day.get("maxtemp_c") if units == "metric" else day.get("maxtemp_f"),
            t["fc_tmin"]: day.get("mintemp_c") if units == "metric" else day.get("mintemp_f"),
            t["fc_tavg"]: day.get("avgtemp_c") if units == "metric" else day.get("avgtemp_f"),
            t["fc_hum"]: day.get("avghumidity"),
            t["fc_wind"]: day.get("maxwind_kph") if units == "metric" else day.get("maxwind_mph"),
            t["fc_rain"]: day.get("daily_chance_of_rain"),
            t["fc_snow"]: day.get("daily_chance_of_snow"),
            t["col_sunrise"]: astro.get("sunrise"),
            t["col_sunset"]: astro.get("sunset"),
            t["col_cond"]: day.get("condition", {}).get("text"),
        }
        rows.append(row)
    return rows

def update_language():
    st.session_state.lang = st.session_state.lang_selector
    
    if 'current_rows' in st.session_state:
        del st.session_state['current_rows']
    if 'forecast_rows' in st.session_state:
        del st.session_state['forecast_rows']
    if 'errors' in st.session_state:
        del st.session_state['errors']


st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.markdown("""<style>@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
html, body, [class*="st-"], [class*="css-"] { font-family: 'Vazirmatn', sans-serif; }
h1 { font-size: 32px !important; }
h2 { font-size: 26px !important; }
h3 { font-size: 20px !important; }
p, div, label { font-size: 16px !important; }
</style>""", unsafe_allow_html=True)

FA_RTL = """<style>
div[data-testid="stAppViewContainer"] > section > div[data-testid="block-container"] { direction: rtl; }
div[data-testid="stAppViewContainer"] h1, h2, h3, p, label { direction: rtl; text-align: right; }
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input { direction: ltr !important; text-align: left !important; }
</style>"""

if 'lang' not in st.session_state:
    st.session_state.lang = 'fa'
    st.session_state.lang_selector = 'fa'
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "rows" not in st.session_state:
    st.session_state.rows = [{"name": "", "lat": None, "lon": None}]

# HEADER 

t = T[st.session_state.lang]
st.radio("Language / زبان", options=["en", "fa"], key='lang_selector', on_change=update_language, horizontal=True)

st.title(t["title"])
st.write("##")
st.caption(t["about"])
if st.session_state.lang == "fa":
    st.markdown(FA_RTL, unsafe_allow_html=True)


# SIDEBAR 
with st.sidebar:
    st.subheader(t["api_key"])
    api_key = st.text_input("API Key", value=st.session_state.api_key, type="password", help=t["api_key_help"], label_visibility="collapsed")
    st.session_state.api_key = api_key

st.divider()
c1, c2, c3 = st.columns([2, 3, 3]) 

# FEATURES
with c1:
    with st.container(border=True, height=280):
        st.subheader(t["units"])
        unit_label = st.radio("Units", [t["units_metric"], t["units_imperial"]], label_visibility="collapsed")
        units = "metric" if unit_label == t["units_metric"] else "imperial"

with c2:
    with st.container(border=True, height=280):
        st.subheader(t["fields_current"])
        all_current_fields = [
            t["col_temp"], t["col_feels"], t["col_hum"], t["col_wind"], t["col_press"],
            t["col_clouds"], t["col_cond"], t["col_visibility"], t["col_uv"], t["col_dt"]
        ]
        default_current_fields = [t["col_temp"], t["col_feels"], t["col_hum"], t["col_wind"], t["col_cond"]]
        selected_current_fields = st.multiselect("current_fields", all_current_fields, default_current_fields, label_visibility="collapsed")

with c3:
    with st.container(border=True, height=280):
        st.subheader(t["fields_forecast"])
        all_forecast_fields = [
            t["fc_tmax"], t["fc_tmin"], t["fc_tavg"], t["fc_hum"], t["fc_wind"],
            t["fc_rain"], t["fc_snow"], t["col_sunrise"], t["col_sunset"], t["col_cond"]
        ]
        default_forecast_fields = [t["fc_tmax"], t["fc_tmin"], t["fc_hum"], t["fc_wind"], t["fc_rain"], t["col_cond"]]
        selected_forecast_fields = st.multiselect("forecast_fields", all_forecast_fields, default_forecast_fields, label_visibility="collapsed")

st.divider()

# DYNAMIC LOCATION INPUTS 

st.subheader(t["tbl_saved"])
st.caption(t["tip_mix"])

for i, row in enumerate(st.session_state.rows):
    proportions = [4, 2, 2, 1]
    name_col, lat_col, lon_col, del_col = st.columns(proportions)
    if st.session_state.lang == 'fa':
        del_col, lon_col, lat_col, name_col = st.columns(proportions[::-1])

    with name_col:
        name_val = st.text_input(f"name_{i}", value=row.get("name", ""), label_visibility="collapsed", placeholder=t["tbl_name"])
    with lat_col:
        lat_val = st.number_input(f"lat_{i}", value=row.get("lat"), label_visibility="collapsed", placeholder=t["col_lat"], format="%.4f", step=0.0001)
    with lon_col:
        lon_val = st.number_input(f"lon_{i}", value=row.get("lon"), label_visibility="collapsed", placeholder=t["col_lon"], format="%.4f", step=0.0001)
    
    with del_col:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.rows.pop(i)
            st.rerun()
    
    if row.get("name") != name_val or row.get("lat") != lat_val or row.get("lon") != lon_val:
        st.session_state.rows[i] = {"name": name_val.strip(), "lat": lat_val, "lon": lon_val}

st.write("######")
if st.button(t["add_row"]):
    st.session_state.rows.append({"name": "", "lat": None, "lon": None})
    st.rerun()

def row_to_query(row: dict) -> str:
    name = (row.get("name") or "").strip()
    lat, lon = row.get("lat"), row.get("lon")
    if name: return name
    if lat is not None and lon is not None: return f"{lat},{lon}"
    return ""
st.write("###")

if st.button(t["fetch"], type="primary", use_container_width=True):
    if not st.session_state.api_key:
        st.error(t["error_api"])
    elif not any(row_to_query(r) for r in st.session_state.rows):
        st.error(t["error_no_locs"])
    else:
        current_rows, forecast_rows, errors = [], [], []
        
        if 'errors' in st.session_state:
            st.session_state.errors = []
            
        with st.spinner("Fetching..."):
            for row in st.session_state.rows:
                q = row_to_query(row)
                if not q: continue
                
                label = row.get("name") or f'{row.get("lat")},{row.get("lon")}' or "(row)"
                
                try:
                    js = fetch_forecast(st.session_state.api_key, q)
                    current_rows.append(parse_current_row(st.session_state.lang, js, units))
                    forecast_rows.extend(parse_daily_forecast(st.session_state.lang, js, units))
                
                except requests.exceptions.HTTPError as http_err:
                    status_code = http_err.response.status_code
                    if status_code == 401:
                        error_message = t["error_401_key"]
                    elif status_code == 400:
                        error_message = t["error_400_loc"]
                    else:
                        error_message = f'{t["error_http"]}: {status_code}' 
                    errors.append((label, error_message))

                except requests.exceptions.RequestException:
                    error_message = t["error_connect"]  
                    errors.append((label, error_message))
                
                except Exception as e:
                    error_message = f'{t["error_unexpected"]}: {e}'
                    errors.append((label, error_message))
                time.sleep(0.2)
        
        st.session_state.current_rows = current_rows
        st.session_state.forecast_rows = forecast_rows
        st.session_state.errors = errors
        st.rerun()



if 'current_rows' in st.session_state and st.session_state.current_rows:
    df_cur = pd.DataFrame(st.session_state.current_rows)
    base_cols = [t["col_city"], t["col_region"], t["col_lat"], t["col_lon"]]
    cols_to_show = base_cols + [c for c in selected_current_fields if c in df_cur.columns]
    st.subheader(t["current"])
    st.dataframe(df_cur[cols_to_show], use_container_width=True)

if 'forecast_rows' in st.session_state and st.session_state.forecast_rows:
    df_fc = pd.DataFrame(st.session_state.forecast_rows)
    base_cols = [t["col_city"], t["fc_date"]]
    cols_to_show = base_cols + [c for c in selected_forecast_fields if c in df_fc.columns]
    st.subheader(t["forecast"])
    st.dataframe(df_fc[cols_to_show], use_container_width=True)

if 'errors' in st.session_state and st.session_state.errors:
    for label, msg in st.session_state.errors:
        st.warning(f"{t['error_fetch']}: {label} → {msg}")
if 'forecast_rows' in st.session_state and st.session_state.forecast_rows:
    
    df_fc_dl = pd.DataFrame(st.session_state.get('forecast_rows', []))
    
    df_fc_dl_clean = df_fc_dl.copy()
    
    df_fc_dl_clean.columns = df_fc_dl_clean.columns.str.replace(r'[^\x00-\x7F]+', '', regex=True).str.strip()

    def clean_string_series(series):
        if series.dtype == 'object':
            return series.astype(str).str.replace(r'[^\x00-\x7F]+', '', regex=True).str.strip()
        return series

    df_fc_dl_clean = df_fc_dl_clean.apply(clean_string_series)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_fc_dl_clean.to_excel(writer, index=False, sheet_name="ForecastDaily")
        
    st.download_button(
        label=t["download"],
        data=buffer.getvalue(),
        file_name="weather_forecast_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )