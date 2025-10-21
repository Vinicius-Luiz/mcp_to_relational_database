import sys
from classes.UserAuth import UserAuth

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_mcp_key = sys.argv[1]
    else:
        api_mcp_key = input("Digite a nova api_mcp_key para registrar: ")
    user_id = UserAuth.add_user(api_mcp_key)
    print(f"Usuário registrado com id: {user_id}")
