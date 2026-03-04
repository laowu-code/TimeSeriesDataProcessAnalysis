# 📊 Time Series Analysis Workstation

> **🌐 Language:** **English** | [简体中文](README.md)

A preliminary web-based data analysis platform designed specifically for time series data processing and analysis.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://laowu-code-timeseriesdataprocessanalysis-app-oyidri.streamlit.app/)
[![Python Version](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🌍 Online Demo
**Try the cloud version directly:** 👉 **[Time Series Data Analysis Workstation](https://laowu-code-timeseriesdataprocessanalysis-app-oyidri.streamlit.app/)**

---

## ✨ Core Features

### 1. 📥 Data I/O
- ✅ Support uploading **CSV/Excel** files
- ✅ **Auto-detect** datetime columns and numeric columns
- ✅ Export cleaned data as **CSV/XLSX**

### 2. 📋 Data Overview & Statistics (EDA)
- ✅ **Real-time preview**: Display first 5 rows and metadata (shape, data types)
- ✅ **Statistical description**: Auto-calculate 7 statistical metrics
  - Mean
  - Median
  - Std Dev (Standard Deviation)
  - Variance
  - Skewness
  - Kurtosis
  - Quartiles
- ✅ **Missing rate analysis**: Statistics and visualization of missing percentages

### 3. 🔍 Time Integrity Check & Interpolation (Data Cleaning)
- ✅ **Frequency detection**: Check if timestamps are continuous
- ✅ **Break identification**: Auto-detect gaps in time series
- ✅ **Smart interpolation**: 6 algorithm options
  - Linear
  - Polynomial
  - Spline (Cubic Spline)
  - Mean (Mean Filling)
  - FFill (Forward Fill)
  - BFill (Backward Fill)
- ✅ **Effect comparison**: Visualize before & after interpolation

### 4. 📈 Dynamic Visualization
- ✅ **Plotly Interactive Charts**
  - 3 chart types: Line, Area, Bar
  - **Zoom, Pan, Value Display** and other interactive features
- ✅ **Multi-variable comparison**
- ✅ **Moving Average (MA) preview**

### 5. ⚠️ Outlier Detection & Handling
- ✅ **Detection algorithms** (3 types):
  - **3σ Rule** (Z-Score)
  - **IQR** (Interquartile Range)
  - **Rolling Window Detection**
- ✅ **Visual marking**: Outliers highlighted in distinct colors/markers
- ✅ **Handling options**:
  - Delete outlier rows
  - Mark as missing and interpolate

### 6. 🔬 Advanced Analysis Extensions
- ✅ **STL Decomposition**: Separate trend, seasonal, and residual components
- ✅ **Correlation Analysis**:
  - Variable correlation heatmap
  - Top 10 strongly correlated pairs
- ✅ **Multi-column comparison**:
  - Support normalized display
  - Observe trends across different scales

---

## 🚀 Quick Start

### ☁️ Cloud Deployment (No Installation Required)
Visit our online version directly: [Streamlit Cloud Link](https://laowu-code-timeseriesdataprocessanalysis-app-oyidri.streamlit.app/)

### 💻 Local Installation
For processing sensitive data or large files locally, follow these steps:

#### Requirements
- Python 3.8 - 3.13
- pip (Python package manager)

#### Installation & Running

##### Step 1: Clone Repository
```bash
git clone https://github.com/laowu-code/TimeSeriesDataProcessAnalysis.git
cd TimeSeriesDataProcessAnalysis
```

##### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

##### Step 3: Launch Application
```bash
streamlit run app.py
```

The application will automatically open in your browser at: `http://localhost:8501`

---

## 📁 File Structure

```
DataPrecess/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                 # Chinese documentation
├── README_EN.md              # English documentation
└── sample_data.csv          # Sample data (optional)
```

---

## 📊 Use Cases

### 1. **Financial Time Series Analysis**
- Stock prices, exchange rates, cryptocurrency data
- Automatic anomaly detection in price movements

### 2. **IoT/Sensor Data**
- Temperature, humidity, pressure monitoring
- Handle sensor failures and missing data

### 3. **Energy Load Forecasting**
- Power consumption time series analysis
- Peak detection and anomaly alerting

### 4. **Meteorological Data Analysis**
- Temperature, precipitation analysis
- Seasonal pattern identification

### 5. **Industrial Equipment Monitoring**
- Vibration, temperature monitoring
- Predictive fault detection

---

## 🛠️ Technology Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| **Web Framework** | Streamlit | Rapid prototyping of data apps |
| **Data Processing** | Pandas, NumPy | Tabular data & numerical computation |
| **Statistical Analysis** | SciPy, Statsmodels | Statistical tests & time series decomposition |
| **Visualization** | Plotly | Interactive dynamic charts |
| **Excel Support** | Openpyxl | Read/write Excel files |

---

## 📝 Example Workflow

### Scenario: Analyzing Temperature Sensor Data

```
1. 📥 Data Import
   └─ Upload temperature_data.csv (timestamp column, temperature values)

2. 📋 Data Overview
   └─ Check shape, types, missing values
   └─ Display mean: 25.3°C, std: 3.2°C

3. 🔍 Time Integrity Check
   └─ Detect main frequency: 5 minutes per record
   └─ Find 3 time breaks (sensor failures)
   └─ Apply linear interpolation to repair gaps

4. 📈 Visualization
   └─ Plot temperature time series
   └─ Add 12-hour moving average
   └─ Observe daily temperature patterns

5. ⚠️ Outlier Detection
   └─ Use 3σ rule for detection
   └─ Find 5 anomalies (sensor errors/environment issues)
   └─ Mark and interpolate anomalies

6. 🔬 Advanced Analysis
   └─ STL decomposition shows 24-hour seasonality
   └─ Correlation analysis: temperature & humidity correlation = 0.85
   └─ Conclusion: Low humidity during high temperature periods

7. 💾 Export
   └─ Download cleaned data as CSV
```

---

## 🎨 Configuration Tips

### Optional Configuration Before Running app.py

#### Increase Upload File Size Limit
Edit `~/.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500
```

#### Customize Application Theme
Edit `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

---

## 🔧 FAQ

### Q1: Time column not auto-detected after upload?
**A**: Ensure the datetime column is in standard format (e.g., `YYYY-MM-DD`, `YYYY-MM-DD HH:MM:SS`)

### Q2: Data becomes NaN after interpolation?
**A**: This usually happens due to:
- Time series too short (less than 4 rows)
- All values are missing
- Try "mean" or "ffill" methods instead

### Q3: STL decomposition fails?
**A**: Check:
- Is data length sufficient (at least 4 periods)?
- Should seasonal period parameter be adjusted?

### Q4: How to handle multiple datetime columns?
**A**: The app auto-detects the first datetime column. Adjust column order in CSV if needed.

---

## 📖 Detailed Feature Explanations

### Interpolation Algorithm Comparison

| Algorithm | Pros | Cons | Best For |
|-----------|------|------|----------|
| **Linear** | Simple & fast | Ignores trends | Short gaps |
| **Polynomial** | Curve fitting | Overfitting risk | Smooth changes |
| **Spline** | Smooth continuous | Needs sufficient data | Complex trends |
| **Mean** | Preserves distribution | Loses time info | Random gaps |
| **FFill** | Keeps last value | May become outdated | Slow changes |
| **BFill** | Keeps next value | May be premature | Surge detection |

### Outlier Detection Algorithm Comparison

| Algorithm | Principle | Parameter | Best For |
|-----------|-----------|-----------|----------|
| **Z-Score** | Normal distribution deviation | σ multiplier (usually 3) | Approximately normal data |
| **IQR** | Interquartile range method | Fixed 1.5× IQR | Parameter-free, robust |
| **Rolling** | Rolling window deviation | Window size, σ multiplier | Non-stationary, local anomalies |

---

## 🎯 Future Enhancements

- [ ] Real-time data stream ingestion (WebSocket)
- [ ] Automatic anomaly alerting (Email/DingTalk)
- [ ] Integrated prediction models (ARIMA, Prophet)
- [ ] Batch processing multiple files
- [ ] Custom interpolation algorithms
- [ ] Direct database connections

---

## 📄 License

MIT License - Free to use and modify

---

## 💬 Feedback & Support

Have questions or suggestions? Feel free to open Issues or Discussions!

---

**Enjoy using the Time Series Analysis Workstation!** 📊✨
