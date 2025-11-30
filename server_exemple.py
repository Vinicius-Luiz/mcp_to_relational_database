from fastmcp import FastMCP
import wikipedia

# Configuração inicial do Wikipedia
wikipedia.set_lang("pt")

mcp = FastMCP("Wikipedia Server")


@mcp.tool("buscar_wikipedia")
def buscar_wikipedia(termo: str):
    """
    Busca um resumo no Wikipedia com base no termo fornecido.
    Retorna título, resumo e URL.
    """
    try:
        resultados = wikipedia.search(termo)
        if not resultados:
            return {"erro": f"Nenhum resultado encontrado para '{termo}'."}

        titulo = resultados[0]
        pagina = wikipedia.page(titulo)
        resumo = wikipedia.summary(titulo, sentences=7)

        return {"titulo": titulo, "resumo": resumo, "url": pagina.url}

    except wikipedia.exceptions.DisambiguationError as e:
        return {"erro": f"Termo ambíguo. Opções possíveis: {e.options[:5]}"}

    except wikipedia.exceptions.PageError:
        return {"erro": f"Nenhuma página encontrada para '{termo}'."}

    except Exception as e:
        return {"erro": f"Ocorreu um erro: {str(e)}"}


@mcp.tool("contar_palavras")
def contar_palavras(resumo: str) -> int:
    """
    Conta o número de palavras no texto fornecido.
    """
    return len(resumo.split())


if __name__ == "__main__":
    mcp.run(transport="sse")
