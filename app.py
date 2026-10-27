import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

API_URL = "https://qlkais3b69.execute-api.us-east-1.amazonaws.com/default/ProcessHydroponicsData"

st.set_page_config(page_title="Smart Hydroponics Monitoring System", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .kpi-container {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 6px;
        text-align: center;
    }
    h3, h4, p {
        color: #C9D1D9 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Smart Hydroponics Monitoring System")

# --- LIVE STATUS BAR PLACEHOLDER ---
status_bar = st.empty()
status_bar.info("🔄 Fetching latest telemetry from AWS...")

# Sidebar Controls for Actuation
st.sidebar.markdown("### System Controls")
refresh_rate = st.sidebar.slider("Refresh rate (seconds)", 5, 60, 5)
auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Actuator Override")
if st.sidebar.button("🟢 Turn Pump ON"):
    try:
        requests.post(API_URL, json={"command": "PUMP_ON"})
        st.sidebar.success("Command sent: PUMP_ON")
    except Exception as e:
        st.sidebar.error(f"Failed: {e}")

if st.sidebar.button("🔴 Turn Pump OFF"):
    try:
        requests.post(API_URL, json={"command": "PUMP_OFF"})
        st.sidebar.success("Command sent: PUMP_OFF")
    except Exception as e:
        st.sidebar.error(f"Failed: {e}")

def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                df = pd.DataFrame(data)
                for col in ['water_cm', 'temp', 'humidity', 'light_percent', 'tds_ppm']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Convert timestamps safely to UTC
                df['timestamp'] = df['timestamp'].apply(lambda x: pd.to_datetime(x, utc=True, errors='coerce'))
                df = df.dropna(subset=['timestamp'])
                df = df.sort_values('timestamp')
                return df
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
    return pd.DataFrame()

# Fetch data from AWS
df = fetch_data()

if not df.empty:
    # Update Status Bar with exact completion timestamp
    current_time = datetime.now().strftime("%H:%M:%S")
    status_bar.success(f"✅ Dashboard Updated at {current_time}!")

    latest = df.iloc[-1]
    
    st.markdown("### KPI First Row")
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f'<div class="kpi-container"><p>Water Level</p><h2 style="color: #FF4B4B;">{latest.get("water_cm", 0)} cm</h2></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-container"><p>Temperature</p><h2 style="color: #FF4B4B;">{latest.get("temp", 0):.1f} °C</h2></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-container"><p>Humidity</p><h2 style="color: #FF4B4B;">{latest.get("humidity", 0):.1f} %</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### KPI Second Row")
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1:
        st.markdown(f'<div class="kpi-container"><p>Water Level</p><h3 style="color: #FFDF00;">{latest.get("water_cm", 0)}</h3></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="kpi-container"><p>Temperature</p><h3 style="color: #FFDF00;">{latest.get("temp", 0):.1f}</h3></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="kpi-container"><p>Humidity</p><h3 style="color: #FFDF00;">{latest.get("humidity", 0):.1f}</h3></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="kpi-container"><p>Light Level</p><h3 style="color: #FFDF00;">{latest.get("light_percent", 0)}</h3></div>', unsafe_allow_html=True)
    with s5:
        st.markdown(f'<div class="kpi-container"><p>TDS Value</p><h3 style="color: #FFDF00;">{latest.get("tds_ppm", 0)}</h3></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Chart Layout")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Humidity vs Time**")
        st.line_chart(df.set_index('timestamp')['humidity'])
    with c2:
        st.markdown("**Temperature vs Time**")
        st.line_chart(df.set_index('timestamp')['temp'])
    with c3:
        st.markdown("**Light vs Time**")
        st.line_chart(df.set_index('timestamp')['light_percent'])
else:
    status_bar.warning("⚠️ Waiting for telemetry data from DynamoDB...")

if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()