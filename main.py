from log_manager import init_db, insert_log
from tools.document_schema import tool_document_schema
from tools.analyze_query import tool_analyze_query
from tools.execute_query import tool_execute_query
from tools.get_schema import tool_get_schema
from tools.nl_to_sql import tool_nl_to_sql
from fastmcp import FastMCP

mcp = FastMCP("MCP para Bancos de Dados Relacionais")


@mcp.tool("document_schema")
def document_schema_tool(data):
    return tool_document_schema(data)


@mcp.tool("analyze_query")
def analyze_query_tool(data):
    return tool_analyze_query(data)


@mcp.tool("execute_query")
def execute_query_tool(data):
    return tool_execute_query(data)


@mcp.tool("get_schema")
def get_schema_tool(data):
    return tool_get_schema(data)


@mcp.tool("nl_to_sql")
def nl_to_sql_tool(data):
    return tool_nl_to_sql(data)


if __name__ == "__main__":
    mcp.run(transport="sse")
