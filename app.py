import streamlit as st
import pandas as pd
import sqlite3
import json
import os
import plotly.express as px
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Layoff Analysis App", layout="wide")
st.title("Layoff Analysis Dashboard")

# Connect to database
conn = sqlite3.connect("layoff.db")

# Dropdown: Category
categories = {
    "Layoff Trends": "layoff_trends.json",
    "Company-Specific Insights": "company_insights.json",
    "High-Risk Segments": "high_risk_segments.json",
    "Funding & Stage Impact": "startup_stability.json",
    "Time-Based Trends": None  # Handled manually
}

selected_category = st.selectbox("Select Analysis Category", list(categories.keys()))
st.markdown(f"**You selected: `{selected_category}`**")

# ---------- TIME-BASED TRENDS SECTION ----------
if selected_category == "Time-Based Trends":
    st.markdown("### ⏳ Time-Based Layoff Trends")

    # Time Range Filter
    min_date = "2019-01"
    max_date = "2024-12"
    year_range = st.slider("Select Year Range", 2019, 2024, (2019, 2024))
    start_year, end_year = year_range

    # Main SQL Query
    query = f"""
        SELECT strftime('%Y-%m', Date) AS Month, COUNT(*) AS Layoff_Count
        FROM layoffs
        WHERE CAST(strftime('%Y', Date) AS INTEGER) BETWEEN {start_year} AND {end_year}
        GROUP BY Month
        ORDER BY Month;
    """
    try:
        df = pd.read_sql_query(query, conn)
        st.subheader("Layoffs Over Time")
        st.plotly_chart(px.bar(df, x="Month", y="Layoff_Count", title="Layoffs per Month"))
        st.dataframe(df)

        with st.expander("View SQL Query"):
            st.code(query, language="sql")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, file_name="time_trends.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error: {e}")

    # ---- Static Topics: COVID Impact & Peak Year ----
    st.markdown("---")
    st.markdown("### 🦠 COVID Impact on Layoffs")

    covid_phases = {
        "Pre-COVID (Before March 2020)": "Date < '2020-03-01'",
        "During COVID (Mar 2020 to Dec 2021)": "Date BETWEEN '2020-03-01' AND '2021-12-31'",
        "Post-COVID (2022 Onwards)": "Date >= '2022-01-01'"
    }

    covid_data = []
    for phase, condition in covid_phases.items():
        query = f"""
            SELECT strftime('%Y-%m', Date) AS Month, COUNT(*) AS Layoff_Count
            FROM layoffs
            WHERE {condition}
            GROUP BY Month
            ORDER BY Month;
        """
        try:
            df_phase = pd.read_sql_query(query, conn)
            if not df_phase.empty:
                df_phase["Phase"] = phase
                covid_data.append(df_phase)
        except:
            continue

    if covid_data:
        full_df = pd.concat(covid_data)
        st.plotly_chart(px.bar(full_df, x="Month", y="Layoff_Count", color="Phase", title="COVID Phase-wise Layoffs"))
        st.markdown("""
        - This graph shows how layoffs evolved across three COVID phases.
        - A significant surge is visible during the COVID period in many companies.
        - The post-COVID phase shows whether companies recovered or continued layoffs.
        - Such breakdowns help understand economic impact on employment.
        """)

    # Peak Year Analysis
    st.markdown("---")
    st.markdown("### 📈 Peak Layoff Year")

    try:
        peak_query = """
            SELECT strftime('%Y', Date) AS Year, COUNT(*) AS Layoff_Count
            FROM layoffs
            GROUP BY Year
            ORDER BY Layoff_Count DESC
            LIMIT 5;
        """
        df_peak = pd.read_sql_query(peak_query, conn)
        st.plotly_chart(px.bar(df_peak, x="Year", y="Layoff_Count", title="Top 5 Years with Most Layoffs"))
        st.dataframe(df_peak)
        st.markdown("""
        - The above chart shows peak years with maximum layoffs.
        - This helps identify economic downturns or global events that led to massive job cuts.
        - Often aligns with events like COVID or industry crashes.
        """)
    except Exception as e:
        st.error(f"Peak year error: {e}")

# ---------- OTHER JSON-BASED CATEGORIES ----------
else:
    json_path = os.path.join("json_data", categories[selected_category])
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Select question
        questions = []
        for category in data:
            for q in category["questions"]:
                questions.append(q["question"])
        selected_question = st.selectbox("Select a Question", questions)

        # Get selected question's data
        question_data = next(
            q for cat in data for q in cat["questions"] if q["question"] == selected_question
        )
        query = question_data.get("sql_query")

        df = pd.read_sql_query(query, conn)
        st.subheader("Result")
        st.dataframe(df)

        with st.expander("View SQL Query"):
            st.code(query, language="sql")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, file_name="result.csv", mime="text/csv")

        # Graph
        if len(df) > 1 and len(df.columns) >= 2 and df[df.columns[1]].dtype in ["int64", "float64"]:
            x_col = df.columns[0].lower()
            if any(key in x_col for key in ["month", "year", "date"]):
                fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Trend Over Time")
            else:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Graphical Representation")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")

    # Follow-up Section
    try:
        follow_ups = question_data.get("follow_ups", [])
    except NameError:
        follow_ups = []

    if follow_ups:
        st.markdown("---")
        st.markdown("### Follow-Up Questions")
        for i, follow in enumerate(follow_ups):
            with st.expander(follow.get("question", f"Follow-Up {i+1}")):
                answer = follow.get("answer", "").strip()
                if answer:
                    st.markdown("*Answer:*")
                    st.write(answer)

                f_query = follow.get("sql_query")
                if f_query:
                    try:
                        f_df = pd.read_sql_query(f_query, conn)
                        st.dataframe(f_df)

                        with st.expander("View SQL Query"):
                            st.code(f_query, language="sql")

                        if not f_df.empty:
                            f_csv = f_df.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                "Download Follow-up CSV", f_csv,
                                file_name=f"followup_{i}.csv", mime="text/csv"
                            )

                        if len(f_df) > 1 and len(f_df.columns) >= 2 and f_df[f_df.columns[1]].dtype in ["int64", "float64"]:
                            x_col = f_df.columns[0].lower()
                            if any(key in x_col for key in ["month", "year", "date"]):
                                fig = px.line(f_df, x=f_df.columns[0], y=f_df.columns[1], title="Trend Over Time")
                            else:
                                fig = px.bar(f_df, x=f_df.columns[0], y=f_df.columns[1], title="Follow-up Graph")
                            st.plotly_chart(fig)

                    except Exception as e:
                        st.error(f"Follow-up query error: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 14px;'>"
    "Created by Shraddha • Powered by Streamlit • GitHub: <a href='https://github.com/lylols/LayoffAnalysisApp' target='_blank'>View Repo</a>"
    "</div>",
    unsafe_allow_html=True
)
