from logs_manager import init_db, insert_log, get_logs
from fastapi.responses import JSONResponse
from tools.document_schema import document_schema
from tools.analyze_query import analyze_query
from tools.execute_query import execute_query
from tools.get_schema import get_schema
from tools.nl_to_sql import nl_to_sql
from fastapi import FastAPI, Request
import uvicorn
import json
import time

# ====== Carregar manifest.json ======
with open("manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)
init_db()


# ====== Inicializar servidor ======
app = FastAPI(
    title=manifest.get("name", "MCP Server"),
    description=manifest.get(
        "description",
        "Servidor MCP para integração, análise e documentação de bancos de dados relacionais",
    ),
    version=manifest.get("version", "0.1.0"),
)

# ====== Logs em memória (placeholder para persistência futura) ======
execution_logs = []


# ====== Mapeamento das ferramentas ======
tool_functions = {
    "execute_query": execute_query,
    "get_schema": get_schema,
    "analyze_query": analyze_query,
    "nl_to_sql": nl_to_sql,
    "document_schema": document_schema,
}


@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    if tool_name not in tool_functions:
        return JSONResponse(
            content={"erro": f"Ferramenta '{tool_name}' não encontrada."},
            status_code=404,
        )
    data = await request.json()
    start_time = time.time()
    result = tool_functions[tool_name](data)
    elapsed = (time.time() - start_time) * 1000
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tool": tool_name,
        "status": "success",
        "execution_time": round(elapsed, 2),
    }
    insert_log(log_entry)
    return JSONResponse(content=result)


# ====== Endpoint para consultar manifest ======
@app.get("/manifest")
async def get_manifest():
    return JSONResponse(content=manifest)


# ====== Endpoint para consultar logs ======
@app.get("/logs")
async def get_logs_endpoint():
    logs = get_logs()
    return {"logs": logs}



# ====== Inicialização ======
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
