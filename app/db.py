import pyodbc

# 🔹 Update ONLY this
SERVER = "JARVIS"          # from your SSMS screenshot
DATABASE = "store_sale_data"  # ⚠️ change this


def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")


def run_query(query: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        # If it's SELECT → fetch results
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))

        else:
            # For non-select queries
            conn.commit()
            result = {"message": "Query executed successfully"}

        cursor.close()
        conn.close()

        return result

    except Exception as e:
        raise Exception(f"Query failed: {str(e)}")