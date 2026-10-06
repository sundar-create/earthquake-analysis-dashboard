# 🌍 Earthquake Analysis Dashboard

## 📌 Project Overview

This project analyzes **five years of earthquake data** obtained from the **USGS Earthquake API**. The project demonstrates an end-to-end data analytics workflow using **Python, Pandas, Regex, MySQL, SQL, and Streamlit**.

The earthquake data is retrieved from the USGS GeoJSON API, cleaned and transformed using Python and Pandas, stored in MySQL, analyzed using SQL, and presented through an interactive Streamlit dashboard.

The project focuses on identifying earthquake patterns related to **magnitude, depth, time, tsunami events, earthquake networks, event types, and data quality**.

---

## 🎯 Objectives

The main objectives of this project are:

* Retrieve earthquake data from the USGS Earthquake API.
* Collect and process five years of earthquake records.
* Clean and preprocess raw earthquake data using Python and Pandas.
* Handle missing values and convert data types appropriately.
* Extract useful information from nested GeoJSON data.
* Apply Regex for text-based data extraction.
* Create derived analytical columns such as year, month, day, and depth category.
* Store the cleaned dataset in MySQL.
* Perform analytical queries using SQL.
* Identify important earthquake trends and patterns.
* Build an interactive Streamlit dashboard for visualization.

---

## 🛠️ Technologies Used

| Technology       | Purpose                                  |
| ---------------- | ---------------------------------------- |
| Python           | Data extraction, cleaning and processing |
| Pandas           | Data manipulation and analysis           |
| NumPy            | Numerical operations                     |
| Regex            | Text extraction and transformation       |
| SQL              | Analytical queries                       |
| MySQL            | Data storage                             |
| SQLAlchemy       | Python–MySQL database connection         |
| PyMySQL          | MySQL database driver                    |
| Streamlit        | Interactive dashboard                    |
| Jupyter Notebook | Data exploration and analysis            |
| Git & GitHub     | Version control and project submission   |

---

## 📂 Project Structure

```text
earthquake-analysis-dashboard/
│
├── dashboard.py
│
├── usgs_project/
│   ├── app.py
│   ├── appy.py
│   ├── fetch_earthquakes.py
│   ├── fromthescratch.ipynb
│   ├── sample seismic.ipynb
│   └── seismic data analysis.ipynb
│
├── .gitignore
│
└── README.md
```

---

## 🌐 Data Source

The earthquake data was obtained from the **USGS Earthquake API** in GeoJSON format.

The API provides earthquake information including:

* Earthquake ID
* Timestamp
* Magnitude
* Magnitude type
* Location
* Latitude
* Longitude
* Depth
* Tsunami indicator
* Network information
* Station count
* Data quality measurements
* Event type
* Additional event metadata

The project processes the API response and converts the nested GeoJSON structure into a structured Pandas DataFrame.

---

## 🔄 Data Processing Workflow

The project follows this general workflow:

```text
USGS Earthquake API
        ↓
GeoJSON Data
        ↓
Python Data Extraction
        ↓
Pandas DataFrame
        ↓
Data Cleaning
        ↓
Data Transformation
        ↓
Derived Analytical Columns
        ↓
MySQL Database
        ↓
SQL Analysis
        ↓
Streamlit Dashboard
```

---

## 🧹 Data Cleaning & Preprocessing

The raw earthquake data was cleaned and transformed using Pandas.

Major preprocessing steps included:

### Timestamp conversion

USGS timestamps were provided in milliseconds and converted into readable datetime values.

```python
df["time"] = pd.to_datetime(df["time"], unit="ms")
df["updated"] = pd.to_datetime(df["updated"], unit="ms")
```

### Numeric conversion

Important numerical fields were converted using:

```python
pd.to_numeric(..., errors="coerce")
```

This allowed invalid or missing values to be represented as `NaN`.

### Missing-value handling

The dataset contains missing values in several fields. These were identified and handled appropriately during preprocessing rather than tr
