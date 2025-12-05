from classes.Logger.LogManager import LogManager
from tools.document_schema import tool_document_schema
from tools.analyze_query import tool_analyze_query
from tools.execute_query import tool_execute_query
from tools.get_schema import tool_get_schema
from tools.nl_to_sql import tool_nl_to_sql
from fastmcp import FastMCP
import time

mcp = FastMCP("MCP para Bancos de Dados Relacionais")

# instancia o gerenciador de logs (cria o DB/tabela se necessário)
lm = LogManager()


@mcp.tool("document_schema")
def document_schema_tool(data):
    start_time = time.time()
    try:
        response = tool_document_schema(data)
    except Exception as e:
        raise
    finally:
        execution_time = time.time() - start_time
        lm.log_tool_execution(
            "document_schema",
            f"error: {str(e)}",
            execution_time,
            token="abdef",
        )
    return response


@mcp.tool("analyze_query")
def analyze_query_tool(data):
    start_time = time.time()
    try:
        response = tool_analyze_query(data)
    except Exception as e:
        raise
    finally:
        execution_time = time.time() - start_time
        lm.log_tool_execution(
            "analyze_query",
            f"error: {str(e)}",
            execution_time,
            token="abdef",
        )
    return response


@mcp.tool("execute_query")
def execute_query_tool(data):
    start_time = time.time()
    try:
        response = tool_execute_query(data)
    except Exception as e:
        raise
    finally:
        execution_time = time.time() - start_time
        lm.log_tool_execution(
            "execute_query",
            f"error: {str(e)}",
            execution_time,
            token="abdef",
        )
    return response


@mcp.tool("get_schema")
def get_schema_tool(data):
    start_time = time.time()
    try:
        response = tool_get_schema(data)
    except Exception as e:
        raise
    finally:
        execution_time = time.time() - start_time
        lm.log_tool_execution(
            "get_schema",
            f"error: {str(e)}",
            execution_time,
            token="abdef",
        )
    return response


@mcp.tool("nl_to_sql")
def nl_to_sql_tool(data):
    start_time = time.time()
    try:
        response = tool_nl_to_sql(data)
    except Exception as e:
        raise
    finally:
        execution_time = time.time() - start_time
        lm.log_tool_execution(
            "nl_to_sql",
            f"error: {str(e)}",
            execution_time,
            token="abdef",
        )
    return response


if __name__ == "__main__":
    mcp.run(transport="sse")
