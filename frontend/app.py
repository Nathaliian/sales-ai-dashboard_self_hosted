import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales AI Dashboard", layout="wide")

# 🎨 Styling
st.markdown("""
<style>
.kpi-card {
    background: #111827;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
.kpi-title {
    font-size: 14px;
    opacity: 0.7;
}
.kpi-value {
    font-size: 26px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 🧭 Sidebar
st.sidebar.title("⚙️ Sales AI")
question = st.sidebar.text_input("Ask your question")
run = st.sidebar.button("Run Query")

# 🏠 Header
st.title("📊 Sales AI Dashboard")
st.caption("Natural language → SQL → Insights")

# 🔁 API call function (clean separation)
def fetch_data(question):
    try:
        res = requests.post(
            "http://127.0.0.1:8000/query",
            json={"question": question},
            timeout=60
        )
        return res.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# 🚀 Main logic
if run and question:

    with st.spinner("🤖 Thinking... Generating insights"):
        data = fetch_data(question)

    if not data.get("success"):
        st.error(f"Error: {data.get('error', data)}")

    else:
        response = data["data"]
        df = pd.DataFrame(response["rows"])

        # 🧠 SQL
        with st.expander("🧠 Generated SQL"):
            st.code(response["sql"], language="sql")

        # 💡 KPIs
        if not df.empty:
            st.subheader("📌 Key Metrics")

            col1, col2, col3 = st.columns(3)

            numeric_cols = df.select_dtypes(include=['number']).columns

            if len(numeric_cols) > 0:
                main_metric = df[numeric_cols[0]].sum()

                col1.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total</div>
                    <div class="kpi-value">{main_metric:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)

                col2.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Average</div>
                    <div class="kpi-value">{df[numeric_cols[0]].mean():,.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            col3.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Records</div>
                <div class="kpi-value">{len(df)}</div>
            </div>
            """, unsafe_allow_html=True)

        # 📈 Visualization
        if not df.empty and len(df.columns) >= 2:
            st.subheader("📈 Visualization")

            x_col = df.columns[0]
            numeric_cols = df.select_dtypes(include=['number']).columns

            if len(numeric_cols) > 0:
                y_col = numeric_cols[0]

                # 🔄 Smart chart selection
                if "date" in x_col.lower():
                    fig = px.line(df, x=x_col, y=y_col, title="Trend Analysis")
                elif len(df) <= 10:
                    fig = px.pie(df, names=x_col, values=y_col, title="Distribution")
                else:
                    fig = px.bar(df, x=x_col, y=y_col, title="Comparison")

                st.plotly_chart(fig, use_container_width=True)

        # 📋 Table
        st.subheader("📋 Data")
        st.dataframe(df, use_container_width=True)

        # 💡 Insight
        if response.get("explanation"):
            st.subheader("💡 Insight")
            st.success(response["explanation"])

else:
    st.info("👈 Enter a query from the sidebar to begin")