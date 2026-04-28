import ollama
import re

# 🔒 Your exact schema (do NOT change unless DB changes)
SCHEMA = """
Table: dbo.store_sales_data_cleaned

Columns:
customer_id
customer_name
last_name
date_of_birth
sales
year
outlet_type
city_type
category_of_goods
region
country
segment
sales_date
order_id
order_date
ship_date
ship_mode
state
postal_code
product_id
sub_category
product_name
quantity
profit
shipping_days
age
Age_Group
discount
"""


# 🚀 MAIN FUNCTION: Generate SQL
def generate_sql(question: str):
    prompt = f"""
You are a highly strict SQL Server query generator.

Your task is to convert a natural language question into a VALID SQL Server query.

━━━━━━━━━━━
DATABASE CONTEXT
━━━━━━━━━━━
{SCHEMA}

━━━━━━━━━━━
STRICT RULES (MUST FOLLOW)
━━━━━━━━━━━
1. Use ONLY this table: dbo.store_sales_data_cleaned
2. Use ONLY the columns listed above
3. DO NOT invent tables or columns
4. ALWAYS use proper SQL Server syntax
5. ALWAYS include GROUP BY when using aggregation with non-aggregated columns
6. Use SUM(), AVG(), COUNT(), etc. correctly
7. Use TOP instead of LIMIT
8. Always alias aggregated columns clearly
9. Do NOT include explanations, comments, or markdown
10. Return ONLY the SQL query (plain text)

━━━━━━━━━━━
INTELLIGENT BEHAVIOR RULES
━━━━━━━━━━━
- "total" → SUM()
- "average" → AVG()
- "count" → COUNT()
- "top N" → SELECT TOP N ... ORDER BY ... DESC
- "by category/region/etc." → GROUP BY
- Use order_date or sales_date for time-based queries

━━━━━━━━━━━
EXAMPLES
━━━━━━━━━━━

Q: total sales
SELECT SUM(sales) AS total_sales
FROM dbo.store_sales_data_cleaned;

Q: total profit by region
SELECT region, SUM(profit) AS total_profit
FROM dbo.store_sales_data_cleaned
GROUP BY region;

Q: top 5 products by sales
SELECT TOP 5 product_name, SUM(sales) AS total_sales
FROM dbo.store_sales_data_cleaned
GROUP BY product_name
ORDER BY total_sales DESC;

━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━
Return ONLY SQL. No explanation.

━━━━━━━━━━━
USER QUESTION
━━━━━━━━━━━
{question}
"""

    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_sql = response["message"]["content"]

        # 🧹 Clean SQL output
        cleaned_sql = clean_sql(raw_sql)

        return cleaned_sql

    except Exception as e:
        raise Exception(f"AI SQL generation failed: {str(e)}")


# 🧹 CLEANING FUNCTION (VERY IMPORTANT)
def clean_sql(sql: str) -> str:
    # Remove markdown ```sql ```
    sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE)

    # Remove "SQL:" prefix if present
    sql = re.sub(r"^SQL\s*:\s*", "", sql, flags=re.IGNORECASE)

    # Keep only first SQL statement (avoid explanations after ;)
    if ";" in sql:
        sql = sql.split(";")[0] + ";"

    return sql.strip()


# 💬 EXPLANATION FUNCTION
def explain_result(result: str):
    prompt = f"""
Explain this SQL query result in simple business terms.

Rules:
- Be concise
- Do NOT assume currency
- Use numbers from the result
- Make it dashboard-friendly

Result:
{result}
"""

    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return f"Explanation failed: {str(e)}"