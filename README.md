# Hydro Sense: IoT Hydroponic Reservoir Monitoring & Control

An end-to-end IoT system pairing an ESP32 edge controller with a serverless AWS cloud backend and a live Streamlit analytics dashboard. Developed by **TV Dhanush** and **Ephraim Chacko John** at Vellore Institute of Technology (VIT).

## 🚀 System Architecture
* **Sensing & Edge Node:** ESP32 microcontroller running non-blocking firmware (`millis()`), BME280 environmental monitoring, an LDR light sensor, a resistive water-level sensor, and an analog TDS probe utilizing a **30-sample median filtering algorithm** and temperature compensation.
* **Local Actuation:** Pulse-and-settle refill state machine (4s pump active, 2s settling phase) that operates independently of network connectivity.
* **Cloud Pipeline:** AWS API Gateway routing telemetry to an AWS Lambda function, which stores time-series data in **Amazon DynamoDB** and triggers automated low-level alerts via **Amazon SNS**.
* **Visualization:** A dark-themed **Streamlit** dashboard fetching real-time KPI metrics and historical trend charts.

---

## 📂 Repository Structure
* `firmware/` - Contains the Arduino C++ code for the ESP32 edge node.
* `lambda/` - Contains the Python serverless function code for AWS Lambda.
* `dashboard/` - Contains the Streamlit web application script (`app.py`).
* `docs/` - Contains the complete IEEE research paper (`Project_Final.pdf`).

---

## 🛠️ Tech Stack
* **Microcontroller:** ESP32 (Arduino IDE)
* **Sensors:** BME280, Resistive Water Level Sensor, Analog TDS Sensor, LDR
* **Cloud Services:** AWS API Gateway, AWS Lambda, Amazon DynamoDB, Amazon SNS
* **Dashboard:** Python, Streamlit, Pandas, Requests
