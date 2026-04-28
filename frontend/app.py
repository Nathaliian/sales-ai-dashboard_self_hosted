import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales AI Dashboard", layout="wide")

st.title("📊 Sales AI Dashboard")

question = st.text_input("Ask your sales question")

if st.button("Ask"):

    if question:
        try:
            # ✅ FIX: Use POST + correct endpoint
            res = requests.post(
                "http://127.0.0.1:8000/query",
                json={"question": question}
            )

            data = res.json()

            # ✅ Handle backend format
            if not data.get("success"):
                st.error(data.get("error", "Unknown error"))
            else:
                response = data["data"]

                # 💡 Explanation
                if response.get("explanation"):
                    st.subheader("💡 Insight")
                    st.success(response["explanation"])

                # 🧠 SQL
                st.subheader("🧠 Generated SQL")
                st.code(response["sql"], language="sql")

                # 📋 Table
                rows = response.get("rows", [])
                df = pd.DataFrame(rows)

                st.subheader("📋 Result")
                st.dataframe(df)

                # 📈 Chart (auto-detect numeric)
                if not df.empty and len(df.columns) >= 2:
                    st.subheader("📈 Chart")

                    # smarter column selection
                    x_col = df.columns[0]

                    # pick first numeric column
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        y_col = numeric_cols[0]
                    else:
                        y_col = df.columns[1]

                    fig, ax = plt.subplots()
                    ax.bar(df[x_col].astype(str), df[y_col])
                    plt.xticks(rotation=45)

                    st.pyplot(fig)

        except Exception as e:
            st.error(str(e))