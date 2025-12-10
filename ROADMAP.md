# 🧭 Roadmap Técnico – MCP para Bancos de Dados Relacionais (alinhado ao README)

---

## **Fase 1 – Núcleo do MCP**  
> Criar o servidor MCP básico e suas primeiras ferramentas.

- [x] Instalar dependências (`fastmcp`, drivers de bancos etc.)
- [x] Criar servidor base `FastMCP("MCP para Bancos de Dados Relacionais")`
- [x] Definir ferramentas iniciais via `@mcp.tool`
- [x] Rodar MCP com `mcp.run(transport="sse")`

---

## **Fase 1.1 – Logs, Auditoria e Governança**
> Observabilidade e rastreabilidade, conforme descrito no README.

- [x] Criar módulo de logs
- [x] Criar tabela de auditoria (`logs_mcp`)
- [x] Registrar logs em cada tool MCP
  - [x] timestamp  
  - [x] token credential  
  - [x] tool executada  
  - [x] status  

---

## **Fase 2 – Integração com Bancos Relacionais**
> Centralizar o acesso aos bancos — objetivo principal descrito no README.

- [x] Criar módulo `BaseDBConnection`
- [-] Implementar conexões individuais:
  - [x] PostgreSQL  
  - [ ] MySQL  
  - [ ] SQL Server
  - [ ] Oracle  
- [x] Criar tools MCP:
  - [x] `analyze_query`
  - [x] `execute_query`
  - [x] `document_schema`
  - [x] `get_schema`
  - [x] `nl_to_sql`
- [ ] Definir padrão de resposta JSON  
  - [ ] `analyze_query`
  - [ ] `execute_query`
  - [ ] `document_schema`
  - [ ] `get_schema`
  - [ ] `nl_to_sql`
- [ ] Configurar pools e credenciais seguras  

---

## **Fase 3 – Agente de Arquitetura de Dados**
> 1º agente listado no README.

- [ ] Tool: gerar SQL DDL a partir de prompts  
- [ ] Tool: validar modelagem e normalização  
- [ ] Tool: gerar diagramas ER (JSON/imagem)  
- [ ] Tool: documentar tabelas e colunas  

---

## **Fase 4 – Agente de Análise Ad Hoc e Métricas**
> 2º agente listado no README.

- [ ] Tool: conversão NL → SQL  
- [ ] Tool: criação de métricas e KPIs  
- [ ] Tool: identificação de tendências  
- [ ] Tool: geração de insights textuais  
- [ ] Tool: resumo automático dos resultados  

---

## **Fase 5 – Agente de Ensino e Explicação**
> 3º agente listado no README.

- [ ] Tool: explicar queries SQL  
- [ ] Tool: recomendar boas práticas de SQL/modelagem  

---

## **Fase 7 – Interface de Utilização (UI) `OPCIONAL`**
> UI não é obrigatória no README, mas complementa o projeto.

- [ ] Criar UI web simples  
  - [ ] Entrada de prompts  
  - [ ] Exibição de resultados  
  - [ ] Histórico de consultas  
- [ ] Conectar UI ao MCP via SSE/WebSocket  
- [ ] Implementar autenticação visual (login/token)

---

## **Fase 8 – Integração e Deploy**
> Consolida o ambiente para uso real.

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
