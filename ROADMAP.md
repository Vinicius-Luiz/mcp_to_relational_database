# 🧭 Roadmap Técnico – MCP para Bancos de Dados Relacionais

---

## **Fase 1 – Núcleo do MCP**  
> Objetivo: criar o servidor MCP básico e suas primeiras ferramentas.

- [ ] Instalar dependências (`fastmcp`, drivers de bancos etc.)
- [ ] Criar servidor base `FastMCP("DB Server")`
- [ ] Definir ferramentas iniciais via `@mcp.tool`
  - [ ] `testar_conexao`
  - [ ] `executar_query` (versão simples)
  - [ ] `listar_bancos`
- [ ] Rodar MCP com `mcp.run(transport="sse")`

---

## **Fase 1.1 – Logs e Auditoria**
> Implementar observabilidade sem mexer na camada HTTP (FastMCP cuida disso).

- [ ] Criar módulo de logs
- [ ] Criar tabela de auditoria (`logs_mcp`)
- [ ] Registrar logs em cada tool MCP
  - [ ] timestamp  
  - [ ] usuário  
  - [ ] tool executada  
  - [ ] status  
- [ ] Criar tool `consultar_logs`

---

## **Fase 2 – Integração com Bancos Relacionais**
> Criar camada de acesso genérica e expor as operações via MCP Tools.

- [ ] Criar módulo `connection_manager`
- [ ] Implementar conexões individuais:
  - [ ] PostgreSQL  
  - [ ] MySQL  
  - [ ] SQL Server  
  - [ ] Oracle  
- [ ] Criar tools MCP:
  - [ ] `listar_tabelas`
  - [ ] `executar_query` (final)
  - [ ] `get_metadata`
- [ ] Definir padrão de resposta JSON  
- [ ] Configurar pools e credenciais seguras

---

## **Fase 3 – Agente de Arquitetura de Dados**
- [ ] Tool: gerar SQL DDL a partir de prompts  
- [ ] Tool: validar modelagem e normalização  
- [ ] Tool: gerar diagramas ER (JSON/imagem)  
- [ ] Tool: documentar tabelas e colunas  

---

## **Fase 4 – Agente de Análise Ad Hoc e Métricas**
- [ ] Tool: conversão NL → SQL  
- [ ] Tool: criação de métricas e KPIs  
- [ ] Tool: identificação de tendências  
- [ ] Tool: geração de insights textuais  

---

## **Fase 5 – Agente de Ensino e Explicação**
- [ ] Tool: explicar queries SQL  
- [ ] Tool: gerar documentação técnica  
- [ ] Tool: recomendar boas práticas de SQL/modelagem  

---

## **Fase 7 – Interface de Utilização (UI)**
- [ ] Criar UI web simples  
  - [ ] Entrada de prompts  
  - [ ] Exibição de resultados  
  - [ ] Histórico de consultas  
- [ ] Conectar UI ao MCP via SSE/WebSocket  
- [ ] Implementar autenticação visual (login/token)

---

## **Fase 8 – Integração e Deploy**
- [ ] Criar Dockerfile para o MCP  
- [ ] Configurar docker-compose com múltiplos bancos  
- [ ] Usar `.env` para variáveis sensíveis

---

## 🎯 **Objetivo Final**
Um servidor MCP robusto para bancos relacionais, com:
- Acesso centralizado a múltiplos bancos  
- Ferramentas inteligentes de análise e governança  
- Auditoria, segurança e documentação automática  
- UI funcional  
- Deploy via Docker  
