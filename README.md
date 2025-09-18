# Layoff Analysis Streamlit App

This interactive Streamlit web application enables HR professionals, data analysts, and business users to explore patterns in tech industry layoffs through user-friendly, SQL-powered insights.

---
Check it out: https://layoffanalysisapp-dashboard.streamlit.app/

## Features

- Organized analysis by category:
  - Layoff Trends
  - Company-Specific Insights
  - High-Risk Segments
  - Time-Based Trends
  - Funding & Stage Impact
- Smart dropdown system to select main categoryamong the forthmentioned
- Questions related to the selected category alongwith 2-3 follow up questions covering a total of 45+ questions
- SQL-based insights with the option to view underlying queries
- Data visualizations using bar and line charts
- Export filtered results to CSV
- Dynamic filters and recommendations based on selection
- Clean user Interface using streamlit 

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

- app.py: Main Streamlit application

- layoff.db: SQLite database containing layoff data

- README.md: Project documentation

- json_data/: Contains JSON files for each analysis category:

    - company_insights.json

    - high_risk_segments.json

    - layoff_trends.json

    - startup_stability.json

    - time_based_trends.json

## How to Run the Project Locally

### 1. Clone the GitHub repository
git clone https://github.com/lylols/layoff-analysis-app.git
cd layoff-analysis-app

### 2. (Optional but recommended) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # For Windows
### source venv/bin/activate  # For macOS/Linux

### 3. Install the dependencies
pip install -r requirements.txt

### 4. Run the Streamlit app
streamlit run app.py

The app will open in your browser at http://localhost:8501
