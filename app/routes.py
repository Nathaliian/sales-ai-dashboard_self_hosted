from fastapi import APIRouter
from pydantic import BaseModel

from app.ai import generate_sql, explain_result
from app.db import run_query

# ✅ DEFINE router FIRST
router = APIRouter()


class QueryRequest(BaseModel):
    question: str


def is_safe_query(query: str):
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    return not any(word in query.upper() for word in forbidden)


# ✅ NOW use decorator
@router.post("/query")
def query_data(request: QueryRequest):
    try:
        sql = generate_sql(request.question)

        if not is_safe_query(sql):
            return {
                "success": False,
                "error": "Unsafe query generated",
                "sql": sql
            }

        result = run_query(sql)

        # ⚡ faster: skip explanation for now
        explanation = "Result generated successfully"

        return {
            "success": True,
            "data": {
                "question": request.question,
                "sql": sql,
                "rows": result,
                "explanation": explanation
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }