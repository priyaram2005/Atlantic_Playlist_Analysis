# 🎵 United States Top 50 Playlist Performance and Song Popularity Trend Analysis

## 📌 Overview

This project analyzes the historical performance of songs in the **United States Top 50 Playlist**. The objective is to understand playlist trends, artist dominance, song popularity, ranking stability, and other important factors affecting music performance.

The project was completed as part of the **Data Science Internship at Unified Mentor Pvt. Ltd.**

---

## 📂 Dataset

**Dataset Name:**
Atlantic_United_States.csv

### Dataset Features

- Date
- Position
- Song
- Artist
- Popularity
- Duration (ms)
- Album Type
- Total Tracks
- Explicit Content

---

## 🎯 Objectives

- Analyze playlist ranking trends.
- Study artist dominance.
- Measure song popularity.
- Calculate chart longevity.
- Compare album and single performance.
- Analyze explicit vs non-explicit songs.
- Build an interactive analytics dashboard.

---

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Plotly Express
- Streamlit
- VS Code

---

## 📊 Feature Engineering

The following features were created:

- Days on Chart
- Average Rank
- Best Rank
- Rank Volatility Index
- Popularity Trend Score
- Duration in Minutes
- Artist Dominance Index

---

## 📈 Dashboard Features

The Streamlit dashboard includes:

- KPI Cards
- Date Range Filter
- Artist Filter
- Song Filter
- Album Type Filter
- Rank Filter
- Playlist Rank Distribution
- Popularity Trend
- Song Ranking Timeline
- Artist Analysis
- Business Insights
- Correlation Heatmap
- Download Filtered Dataset

---

## 📊 Key Insights

- Songs with longer playlist presence generally maintain higher popularity.
- Artist dominance is determined by repeated playlist appearances.
- Rank volatility helps identify stable and unstable songs.
- Album type and explicit content influence popularity trends.
- Interactive dashboards simplify business decision-making.

---

## 📁 Project Structure

```
Atlantic_Playlist_Analysis/

│── app.py
│── requirements.txt
│── README.md

│
├── data/
│      playlist_feature_engineered.csv
│
├── research_paper/
│      Research_Paper.pdf
│
└── images/
       dashboard.png
```

---

## ▶️ Run the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run app.py
```

---

## 📌 Internship

**Organization:** Unified Mentor Pvt. Ltd.

**Domain:** Data Science

---

## 👩‍💻 Developed By

**Priya**

Data Science Intern

Unified Mentor Pvt. Ltd.
