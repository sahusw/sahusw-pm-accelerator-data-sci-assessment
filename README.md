PM Accelerator Mission:
"Our mission is to break down financial barriers and achieve educational fairness. With the goal of establishing 200 schools worldwide over the next 20 years, we aim to empower more kids for a better future in their life and career, simultaneously fostering a diverse landscape in the tech industry."*

---

Project Description:
This project analyzes the Global Weather Repository dataset from Kaggle to demonstrate data science skills through both basic and advanced techniques. The analysis includes:
    - Advanced EDA with anomaly detection
    - Multiple forecasting models with ensemble methods
    - Unique analyses covering climate patterns, air quality, and geographical trends

---

How to Run:
1. Make sure Python 3.8 or higher is installed
2. Download the Dataset
    1. Go to [Kaggle - Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)
    2. Click "Download" to get the dataset
    3. Extract the ZIP file
    4. Place GlobalWeatherRepository.csv (from the ) in the same folder as the Python scripts
3. Download all files from Github
4. Cd into the folder with all of the files
5. Enter a virtual environment by running the following commands:
    1. python3 -m venv venv
    2. source venv/bin/activate
6. Install Required Packages (can try putting sudo in front of command): pip install -r requirements.txt
7. Run in the terminal (will take 1-2 minutes): python weather_forecast_analysis.py 
8. Generate the PDF Report: python generate_pdf_report.py

---

What the Analysis Does:
1. Data Cleaning
    - Loads 130,978 weather observations
    - Handles missing values using median imputation
    - Extracts time features (hour, day, month)
2. Anomaly Detection
    - Uses Isolation Forest algorithm
    - Identifies 5% of data as anomalous
    - Anomalies show extreme weather events
3. Forecasting Models: Five models are built and compared:
    - Linear Regression
    - Ridge Regression
    - Random Forest ← Best performer!
    - Gradient Boosting
    - Ensemble (Average)
4. Feature Importance: Shows which weather features matter most:
    1. Latitude (37.3%)
    2. UV Index (32.6%)
    3. Pressure (13.4%)
5. Climate & Air Quality Analysis
    - Compares tropical vs temperate zones
    - Analyzes air quality correlations
    - Identifies cities with best/worst air quality
