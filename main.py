from mcp_manager import init_db, insert_log, get_logs
from fastapi.responses import JSONResponse
from tools.document_schema import document_schema
from classes.UserAuth import UserAuth
from tools.analyze_query import analyze_query
from tools.execute_query import execute_query
from tools.get_schema import get_schema
from tools.nl_to_sql import nl_to_sql
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import json
import time

# Sessão simples em memória (para exemplo, uma produção usaria JWT ou outro mecanismo mais robusto)
SESSIONS = {}

# ====== Carregar manifest.json ======
with open("manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)
init_db()


# ====== Inicializar servidor ======
app = FastAPI(
    title=manifest.get("name"),
    description=manifest.get("description"),
    version=manifest.get("version"),
)


# ====== Mapeamento das ferramentas ======
tool_functions = {
    "execute_query": execute_query,
    "get_schema": get_schema,
    "analyze_query": analyze_query,
    "nl_to_sql": nl_to_sql,
    "document_schema": document_schema,
}


# ====== Endpoint para chamar ferramentas ======
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
    insert_log(
        {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tool": tool_name,
            "status": "success",
            "execution_time": round(elapsed, 2),
        }
    )
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


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    api_mcp_key = data.get("api_mcp_key")
    if not api_mcp_key:
        raise HTTPException(status_code=422, detail="Chave ausente.")
    user_id = UserAuth.login(api_mcp_key)
    if user_id:
        SESSIONS[api_mcp_key] = user_id
        return {"message": "Login realizado com sucesso."}
    else:
        return JSONResponse(status_code=401, content={"erro": "API MCP Key inválida."})


@app.post("/add_connection")
async def add_connection(request: Request):
    data = await request.json()
    api_mcp_key = data.get("api_mcp_key")
    dbms = data.get("dbms")
    connection_string = data.get("connection_string")
    if not api_mcp_key or not dbms or not connection_string:
        raise HTTPException(status_code=422, detail="Campos obrigatórios ausentes.")
    user_id = SESSIONS.get(api_mcp_key) or UserAuth.login(api_mcp_key)
    if not user_id:
        return JSONResponse(status_code=401, content={"erro": "Não autenticado."})
    UserAuth.add_connection(user_id, dbms, connection_string)
    return {"message": "Credencial adicionada com sucesso."}


@app.post("/remove_connection")
async def remove_connection(request: Request):
    data = await request.json()
    api_mcp_key = data.get("api_mcp_key")
    dbms = data.get("dbms")
    if not api_mcp_key or not dbms:
        raise HTTPException(status_code=422, detail="Campos obrigatórios ausentes.")
    user_id = SESSIONS.get(api_mcp_key) or UserAuth.login(api_mcp_key)
    if not user_id:
        return JSONResponse(status_code=401, content={"erro": "Não autenticado."})
    UserAuth.remove_connection(user_id, dbms)
    if api_mcp_key in SESSIONS:
        del SESSIONS[api_mcp_key]
    return {"message": "Conexão removida e usuário deslogado."}


# ====== Inicialização ======
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
