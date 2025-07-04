# Fin-Bot: Assistente Financeiro com MCP

Um chatbot financeiro inteligente que usa Model Context Protocol (MCP) para fornecer conselhos financeiros personalizados.

## Funcionalidades

- **Análise Financeira Automática**: Carrega dados do cliente e faz análise inicial
- **Acesso Completo aos Dados**: O assistente tem acesso aos dados completos do cliente em cada mensagem
- **Ferramentas Financeiras**:
  - `help_template`: Analisa se o saldo é suficiente para cobrir gastos
  - `surpresa_gastos`: Detecta gastos acima da média
  - `lembrete_emprestimo`: Sugere pagamentos extras para economizar juros
- **Chat Interativo**: Conversa natural com o assistente financeiro
- **Histórico de Conversas**: Mantém contexto usando OpenAI Threads API
- **Cálculos Precisos**: O assistente pode fazer cálculos específicos usando os dados reais do cliente

## Configuração

1. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

2. **Configure as variáveis de ambiente**:
   - Copie o arquivo `env.example` para `.env`:
     ```bash
     cp env.example .env
     ```
   - Edite o arquivo `.env` e adicione suas chaves reais:
     ```
     OPENAI_API_KEY=sua_chave_api_aqui
     OPENAI_ASSIS_ID=seu_assistant_id_aqui
     ```
   
   ⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` com suas chaves reais!

3. **Configure o Assistente OpenAI**:
- Crie um assistente no OpenAI com as instruções financeiras
- Use o ID do assistente na variável `OPENAI_ASSIS_ID`

## Como Usar

### 1. Configure os Dados do Cliente

Você tem três opções:

**Opção A: Usar dados de exemplo**
```bash
python create_client_data.py
# Escolha opção 1 para dados de exemplo
```

**Opção B: Criar dados personalizados**
```bash
python create_client_data.py
# Escolha opção 2 e siga as instruções
```

**Opção C: Usar cenários pré-definidos**
- Veja o arquivo `example_scenarios.md` para diferentes cenários
- Copie um cenário e cole no arquivo `client_data.json`

### 2. Inicie o Servidor MCP
```bash
python server.py
```

### 3. Execute o Chat
```bash
python chatbot/main.py
```

O sistema irá:
1. Carregar os dados do cliente de `client_data.json`
2. Fazer uma análise inicial da situação financeira usando as ferramentas
3. Apresentar recomendações baseadas na análise
4. Iniciar o chat interativo com contexto completo

## Estrutura dos Dados do Cliente

O arquivo `client_data.json` deve conter:

```json
{
  "cliente": {
    "nome": "Nome do Cliente",
    "idade": 30,
    "profissao": "Profissão",
    "estado_civil": "Estado Civil",
    "filhos": 0
  },
  "situacao_financeira": {
    "saldo_atual": 2500.00,
    "renda_mensal": 4500.00,
    "frequencia_pagamento": "MONTHLY",
    "gastos_mes_passado": 3800.00,
    "gastos_medios_mensais": {
      "alimentacao": 800.00,
      "transporte": 400.00,
      "moradia": 1200.00,
      "saude": 300.00,
      "educacao": 200.00,
      "lazer": 400.00,
      "outros": 500.00
    }
  },
  "emprestimos": [
    {
      "tipo": "Tipo do Empréstimo",
      "valor_restante": 15000.00,
      "parcelas_restantes": 24,
      "valor_parcela": 850.00,
      "juros_mensal": 0.015,
      "proximo_vencimento": "2025-01-15"
    }
  ],
  "transacoes_recentes": [
    {
      "id": "tx_001",
      "amount": 120.50,
      "category": "Alimentação",
      "transacted_at": "2025-01-02T12:30:00Z",
      "description": "Descrição da transação"
    }
  ],
  "metas_financeiras": {
    "emergencia": 10000.00,
    "viagem": 5000.00,
    "entrada_imovel": 50000.00,
    "aposentadoria": 500000.00
  },
  "habitos": {
    "gasta_mais_que_ganha": false,
    "tem_reserva_emergencia": true,
    "investe_regularmente": false,
    "controla_gastos": true,
    "tem_plano_aposentadoria": false
  }
}
```

## Ferramentas Disponíveis

### help_template
Analisa se o saldo disponível é suficiente para cobrir os gastos do mês.

**Parâmetros**:
- `balance_available`: Saldo disponível
- `last_month_amount`: Valor gasto no mês passado
- `income`: Rendimento mensal
- `frequency`: Frequência de pagamento (DAILY, WEEKLY, MONTHLY, etc.)

### surpresa_gastos
Detecta categorias onde o gasto de ontem ficou acima da média dos últimos dias.

**Parâmetros**:
- `transactions`: Lista de transações
- `reference_date`: Data de referência (opcional)
- `window_days`: Janela de dias para cálculo da média
- `threshold_pct`: Percentual de tolerância

### lembrete_emprestimo
Gera lembretes de vencimento e sugere pagamentos extras para economizar juros.

**Parâmetros**:
- `next_payment_date`: Data do próximo vencimento
- `minimum_installment_amount`: Valor mínimo da parcela
- `installments_outstanding`: Parcelas restantes
- `interest_rate`: Taxa de juros mensal
- `extra_amount`: Valor extra sugerido

## Comandos do Chat

- `sair`, `exit`, `quit`: Encerra o chat
- `Ctrl+C`: Interrompe a execução

## Exemplo de Uso

```
👋 Olá João Silva! Analisando sua situação financeira...
============================================================
📋 ANÁLISE INICIAL DA SUA SITUAÇÃO FINANCEIRA:
--------------------------------------------------
📊 Análise de Gastos: {"over_expenses": false}
🚨 Alertas de Gastos: {"alerts": []}
💳 Financiamento de Carro: {"days_to_due": 13, "base_amount": 850.0, "extra_amount": 100.0, "estimated_interest_saved": 45.23, "message": "Oi! Sua próxima parcela de R$ 850.00 vence em 15/01/2025 (daqui a 13 dia(s)). Que tal antecipar mais R$ 100.00? Assim, você pode economizar aproximadamente R$ 45.23 em juros até o fim!"}
💳 Cartão de Crédito: {"days_to_due": 3, "base_amount": 350.0, "extra_amount": 100.0, "estimated_interest_saved": 12.50, "message": "Oi! Sua próxima parcela de R$ 350.00 vence em 05/01/2025 (daqui a 3 dia(s)). Que tal antecipar mais R$ 100.00? Assim, você pode economizar aproximadamente R$ 12.50 em juros até o fim!"}
--------------------------------------------------

🤖 Assistente: Olá João! Analisei sua situação financeira e tenho algumas observações importantes...

🤖 Chat iniciado! Digite 'sair' para encerrar.
==================================================

💬 Você: Como posso melhorar minha situação financeira?
```

## Arquitetura

- **Server**: FastMCP com ferramentas financeiras
- **Client**: Cliente SSE que se conecta ao servidor MCP
- **OpenAI Integration**: Usa OpenAI Assistants API com Threads
- **Data**: Arquivo JSON com dados do cliente para análise personalizada
- **Context Management**: Dados completos do cliente são incluídos em cada mensagem para acesso contínuo

## Como o Assistente Acessa os Dados

O assistente tem acesso completo aos dados do cliente através de:

1. **Contexto Inicial**: Análise automática da situação financeira
2. **Dados em Cada Mensagem**: Os dados completos do cliente são incluídos em cada mensagem enviada ao assistente
3. **Ferramentas MCP**: O assistente pode usar as ferramentas financeiras com os dados corretos do cliente

Isso garante que o assistente sempre tenha acesso às informações mais atualizadas para fazer cálculos precisos e dar conselhos personalizados.

## Desenvolvimento

Para testar apenas a conexão SSE:
```bash
python test_sse_client.py
```

Para testar a conexão HTTP:
```bash
python test_http_client.py
```

Para testar a ferramenta surpresa_gastos:
```bash
python test_surpresa_gastos.py
```

## Arquivos do Projeto

- `server.py` - Servidor MCP com ferramentas financeiras
- `chatbot/main.py` - Cliente chat interativo
- `client_data.json` - Dados do cliente (gerado automaticamente)
- `create_client_data.py` - Script para criar dados do cliente
- `example_scenarios.md` - Cenários de teste pré-definidos
- `test_sse_client.py` - Teste de conexão SSE
- `test_http_client.py` - Teste de conexão HTTP
- `test_surpresa_gastos.py` - Teste da ferramenta surpresa_gastos
- `requirements.txt` - Dependências do projeto 