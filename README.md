

# 🌦️ Weather Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive-orange?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker\&logoColor=white)](https://www.docker.com/)


---

## 📌 Summary

An **interactive bilingual (FA/EN) weather dashboard** built with **Python and Streamlit**.
Users can enter a **WeatherAPI key**, add **multiple locations**, view **current weather** and **3-day forecasts**, and export data to **Excel**.

---

## 📌 داشبورد وضعیت آب و هوا

یک **داشبورد تعاملی دو زبانه (FA/EN) برای آب و هوا** با استفاده از **Python و Streamlit**.
کاربر می‌تواند **کلید API از WeatherAPI** وارد کند، **چندین مکان** اضافه کند، وضعیت **لحظه‌ای هوا** و **پیش‌بینی سه روزه** را مشاهده کرده و داده‌ها را **در قالب اکسل دانلود کند**.



---

## 🚀 Online Demos

* **Streamlit Cloud:** [🔗 Live Demo](https://weather-dashboard-ajaqdrdqkqwcfr54n4jvw3.streamlit.app)
* **Dockerized Demo:** [🐳 Live Demo](https://huggingface.co/spaces/amin704/weather-dashboard)
---


## 🛠️ Built With

* **Python 3.11**
* **Libraries:** `streamlit`, `pandas`, `requests`, `openpyxl`
* **API:** [WeatherAPI.com](https://www.weatherapi.com/)
* **Docker:** Containerized deployment for consistent execution

---

## ⚙️ Local Setup 

### 1️⃣ Clone the repository 

```bash
git clone https://github.com/username/weather-dashboard.git
cd weather-dashboard
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the dashboard locally 

```bash
streamlit run streamlit_weather_dashboard_v2.py
```

### 4️⃣ Open in browser 

Visit `http://localhost:8501`.

---
---
## 🐳 Docker Setup 

### 1️⃣ Build Docker image 

```bash
docker build -t weather-dashboard .
```

### 2️⃣ Run the container 

```bash
docker run -p 8501:8501 weather-dashboard
```

### 3️⃣ Open dashboard 

Visit `http://localhost:8501` or your server IP if deployed remotely.

---
## 📊 Features 

* **Bilingual interface** (English & Persian)
* **Multiple locations** (city name or coordinates)
* **Current weather**: temperature, humidity, wind, pressure, cloud cover, UV index
* **3-day forecast**: max/min/avg temperature, humidity, wind, chance of rain/snow, sunrise/sunset
* **Excel export** of forecast data
* **Unit selection**: Metric (°C, kph) / Imperial (°F, mph)
* **Optional emoji-enhanced labels** for better UX

---

## 📝 Notes

1. API key is stored **only for the current session**.
2. Data export supports Excel, with option to **remove emojis** if desired.
3. Dashboard uses caching to reduce repeated API calls.
4. Ready for **cloud deployment via Streamlit Cloud or Docker Streamlit Cloud**.