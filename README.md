# Layoff Analysis Streamlit App

This interactive Streamlit web application enables HR professionals, data analysts, and business users to explore patterns in tech industry layoffs through user-friendly, SQL-powered insights.

---

## Features

- Organized analysis by category:
  - Layoff Trends
  - Company-Specific Insights
  - High-Risk Segments
  - Employee Metrics
  - Department-Wise Insights
  - Time-Based Trends
  - Funding & Stage Impact
- Smart dropdown system to select main category and follow-up questions
- SQL-based insights with the option to view underlying queries
- Data visualizations using bar and line charts
- Export filtered results to CSV
- Dynamic filters and recommendations based on selection
- Chat-style user interface powered by JSON configuration

---

## Technologies Used

- Python
- Streamlit
- SQLite (layoff.db)
- Pandas
- Altair / Matplotlib
- JSON (for dynamic questions and follow-ups)

---

## Folder Structure

layoff-analysis-app/
├── app.py
├── layoff.db
├── README.md
├── json_data/
│   ├── company_insights.json
│   ├── high_risk_segments.json
│   ├── layoff_trends.json
│   ├── startup_stability.json
│   └── time_based_trends.json


## How to Run the Project Locally

1. **Clone the repository:**

```bash
git clone https://github.com/lylols/layoff-analysis-app.git
cd layoff-analysis-app
