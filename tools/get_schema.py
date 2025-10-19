from typing import Dict, Any

def get_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tables": [
            {
                "table_name": "customers",
                "columns": [
                    {"name": "id", "type": "int", "nullable": False},
                    {"name": "name", "type": "varchar", "nullable": False}
                ]
            }
        ]
    }