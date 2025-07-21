import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime
import os

# Paths
json_path = os.path.join("json_data", "layoff_trends.json")
db_path = "layoff.db"

# Load JSON
with open(json_path, "r") as file:
    trends_data = json.load(file)

# Connect to SQLite DB
conn = sqlite3.connect(db_path)

# App layout
st.set_page_config(page_title="Layoff Trends Analysis", layout="wide")
st.title("📉 Layoff Trends Dashboard")
st.markdown("---")

# Dropdown for main questions
main_question_titles = [q["question"] for q in trends_data]
selected_main = st.selectbox("🔍 Select a main analysis question:", main_question_titles)

# Get selected question
main_q = next(q for q in trends_data if q["question"] == selected_main)

# Run main query
try:
    df = pd.read_sql_query(main_q["sql_query"], conn)

    # Show result smartly
    if "Month" in df.columns and len(df) == 1 and df.select_dtypes(include='number').shape[1] == 1:
        month_val = df["Month"].iloc[0]
        formatted = datetime.strptime(month_val, "%Y-%m").strftime("%B %Y")
        st.write(f"📊 **Top Layoff Month**: {formatted}")
    elif len(df) == 1 and df.shape[1] == 1:
        col = df.columns[0]
        val = df.iloc[0, 0]
        st.write(f"📊 **Result**: {col} = {val}")
    else:
        st.dataframe(df)

        # Visuals
        if len(df) > 2 and df.select_dtypes(include='number').shape[1] == 1:
            metric_col = df.select_dtypes(include='number').columns[0]
            st.bar_chart(df.set_index(df.columns[0])[metric_col])

    # CSV Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Export to CSV", csv, file_name="main_query_result.csv", mime='text/csv')

    # SQL query
    with st.expander("🧠 View SQL Query"):
        st.code(main_q["sql_query"], language="sql")

    # Reasoning + Conclusion
    st.info("💡 Insight: " + main_q.get("insight", "No insight provided."))
    st.success("✅ Conclusion: " + main_q.get("conclusion", "No conclusion provided."))

except Exception as e:
    st.error(f"Error in main question: {e}")

# Follow-up Section
if "follow_ups" in main_q:
    st.markdown("---")
    st.subheader("📌 Select a Follow-Up Question")

    follow_titles = [f["question"] for f in main_q["follow_ups"]]
    selected_follow = st.selectbox("Follow-up Analysis:", follow_titles)

    follow_q = next(f for f in main_q["follow_ups"] if f["question"] == selected_follow)

    try:
        df = pd.read_sql_query(follow_q["sql_query"], conn)

        if "Month" in df.columns and len(df) == 1 and df.select_dtypes(include='number').shape[1] == 1:
            month_val = df["Month"].iloc[0]
            formatted = datetime.strptime(month_val, "%Y-%m").strftime("%B %Y")
            st.write(f"📊 **Top Layoff Month**: {formatted}")
        elif len(df) == 1 and df.shape[1] == 1:
            col = df.columns[0]
            val = df.iloc[0, 0]
            st.write(f"📊 **Result**: {col} = {val}")
        else:
            st.dataframe(df)

            if len(df) > 2 and df.select_dtypes(include='number').shape[1] == 1:
                metric_col = df.select_dtypes(include='number').columns[0]
                st.bar_chart(df.set_index(df.columns[0])[metric_col])

        csv_follow = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Export Follow-up Result", csv_follow, file_name="followup_result.csv", mime='text/csv')

        with st.expander("🧠 View SQL Query"):
            st.code(follow_q["sql_query"], language="sql")

        st.info("💡 Insight: " + follow_q.get("insight", "No insight provided."))
        st.success("✅ Conclusion: " + follow_q.get("conclusion", "No conclusion provided."))

    except Exception as e:
        st.error(f"Error in follow-up: {e}")

# Footer
st.markdown("""
---
<div style="text-align: center; font-size: 0.9em; color: gray;">
    Layoff Trends Analysis App | Built by Shraddha Shrivastava
</div>
""", unsafe_allow_html=True)
