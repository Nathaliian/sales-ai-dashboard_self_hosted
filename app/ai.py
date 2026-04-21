import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# 🔹 Generate SQL from user question
def generate_sql(question: str):
    try:
        prompt = f"""
You are an expert SQL generator.

Database: CSV (converted from SQL Server)

Table name: store_sales_data_cleaned

Columns:
customer_id, customer_name, last_name, date_of_birth,
sales, year, outlet_type, city_type, category_of_goods,
region, country, segment, sales_date, order_id, order_date,
ship_date, ship_mode, state, postal_code, product_id,
sub_category, product_name, quantity, discount, profit,
shipping_days, age, Age_Group

Rules:
- Use ONLY the given columns
- Use correct SQL syntax
- Use SUM(sales) for total sales
- Use GROUP BY when needed
- Use TOP N for limits (not LIMIT)

Examples:
total sales → SELECT SUM(sales) AS total_sales FROM store_sales_data_cleaned
sales by region → SELECT region, SUM(sales) AS total_sales FROM store_sales_data_cleaned GROUP BY region

Question: {question}

Return ONLY SQL (no explanation).
"""

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        sql = response.text.strip()

        # Clean formatting
        sql = sql.replace("```sql", "").replace("```", "").strip()

        print("Generated SQL:", sql)

        return sql

    except Exception as e:
        return f"SQL generation error: {str(e)}"


# 🔹 Generate business insight from result
def explain_result(question, df):
    try:
        data_sample = df.head(10).to_string()

        prompt = f"""
You are a business analyst.

User question:
{question}

Query result:
{data_sample}

Instructions:
- Give a short insight (1–2 lines)
- Mention key numbers
- Keep it simple and clear
"""

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        return f"Insight error: {str(e)}"