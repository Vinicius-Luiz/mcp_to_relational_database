from typing import Dict, Any

def tool_nl_to_sql(data: Dict[str, Any]) -> Dict[str, Any]:
    question = data.get("question")
    query = f"SELECT * FROM vendas WHERE descricao ILIKE '%{question}%';"
    return {"query": query, "confidence": 0.85}