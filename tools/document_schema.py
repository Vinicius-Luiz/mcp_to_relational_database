from typing import Dict, Any

def tool_document_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"documentation": "# Documentação do banco\n\nTabela: customers\n- id (int)\n- name (varchar)"}