import streamlit as st
import pandas as pd
import sqlite3
import json
import os
import plotly.express as px

# Page setup
st.set_page_config(page_title="Layoff Analysis App", layout="wide")
st.title("Layoff Analysis Dashboard")

# Connect to database
conn = sqlite3.connect("layoff.db")

# Dropdown: Category
categories = {
    "Layoff Trends": "layoff_trends.json",
    "Company-Specific Insights": "company_insights.json",
    "High-Risk Segments": "high_risk_segments.json"
}
selected_category = st.selectbox("Select Analysis Category", list(categories.keys()))
st.markdown(f"**You selected: `{selected_category}`**")

# Load JSON for selected category
json_path = os.path.join("json_data", categories[selected_category])
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Select main question
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

# Run main query
try:
    df = pd.read_sql_query(query, conn)
    st.subheader("Result")
    st.dataframe(df)

    # View SQL button
    with st.expander("View SQL Query"):
        st.code(query, language="sql")

    # Export CSV
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, file_name="result.csv", mime="text/csv")

    # Graph logic
    if len(df) > 1 and len(df.columns) >= 2 and df[df.columns[1]].dtype in ["int64", "float64"]:
        time_keywords = ["month", "year", "date"]
        x_col = df.columns[0].lower()
        if any(key in x_col for key in time_keywords):
            fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Trend Over Time")
        else:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Graphical Representation")
        st.plotly_chart(fig)

    # Reasoning + Conclusion
    st.info("💡 Insight: " + question_data.get("insight", "No insight provided."))
    st.success("✅ Conclusion: " + question_data.get("conclusion", "No conclusion provided."))

except Exception as e:
    st.error(f"Error: {e}")

# Follow-up Section
follow_ups = question_data.get("follow_ups", [])
if follow_ups:
    st.markdown("---")
    st.markdown("### Follow-Up Questions")
    for i, follow in enumerate(follow_ups):
        with st.expander(follow.get("question", f"Follow-Up {i+1}")):

            # Always show textual parts
            answer = follow.get("answer", "").strip()
            if answer:
                st.markdown("*Answer:*")
                st.write(answer)

            # Try to show SQL/graph if query exists
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

                    # Insight + Conclusion (Optional)
                    st.info("💡 Insight: " + follow.get("insight", "No insight provided."))
                    st.success("✅ Conclusion: " + follow.get("conclusion", "No conclusion provided."))

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
