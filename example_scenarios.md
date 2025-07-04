# Cenários de Exemplo para o Fin-Bot

Este arquivo contém diferentes cenários financeiros que você pode usar para testar o sistema Fin-Bot.

## Cenário 1: Cliente com Dificuldades Financeiras

**Situação**: Cliente que gasta mais do que ganha e tem dívidas altas.

```json
{
  "cliente": {
    "nome": "Carlos Oliveira",
    "idade": 35,
    "profissao": "Vendedor",
    "estado_civil": "Casado",
    "filhos": 2
  },
  "situacao_financeira": {
    "saldo_atual": 500.00,
    "renda_mensal": 3000.00,
    "frequencia_pagamento": "MONTHLY",
    "gastos_mes_passado": 3500.00
  },
  "emprestimos": [
    {
      "tipo": "Cartão de Crédito",
      "valor_restante": 8000.00,
      "parcelas_restantes": 24,
      "valor_parcela": 400.00,
      "juros_mensal": 0.025,
      "proximo_vencimento": "2025-01-05"
    },
    {
      "tipo": "Financiamento de Carro",
      "valor_restante": 25000.00,
      "parcelas_restantes": 36,
      "valor_parcela": 1200.00,
      "juros_mensal": 0.018,
      "proximo_vencimento": "2025-01-10"
    }
  ],
  "transacoes_recentes": [
    {
      "id": "tx_001",
      "amount": 250.00,
      "category": "Lazer",
      "transacted_at": "2025-01-02T20:00:00Z",
      "description": "Bar com amigos"
    },
    {
      "id": "tx_002",
      "amount": 180.00,
      "category": "Alimentação",
      "transacted_at": "2025-01-02T12:30:00Z",
      "description": "Restaurante"
    }
  ],
  "metas_financeiras": {
    "emergencia": 5000.00,
    "viagem": 2000.00,
    "entrada_imovel": 30000.00,
    "aposentadoria": 200000.00
  }
}
```

## Cenário 2: Cliente Organizado

**Situação**: Cliente que controla bem suas finanças e tem reservas.

```json
{
  "cliente": {
    "nome": "Ana Costa",
    "idade": 29,
    "profissao": "Engenheira",
    "estado_civil": "Solteira",
    "filhos": 0
  },
  "situacao_financeira": {
    "saldo_atual": 15000.00,
    "renda_mensal": 8000.00,
    "frequencia_pagamento": "MONTHLY",
    "gastos_mes_passado": 4500.00
  },
  "emprestimos": [
    {
      "tipo": "Financiamento de Apartamento",
      "valor_restante": 200000.00,
      "parcelas_restantes": 240,
      "valor_parcela": 2500.00,
      "juros_mensal": 0.008,
      "proximo_vencimento": "2025-01-15"
    }
  ],
  "transacoes_recentes": [
    {
      "id": "tx_001",
      "amount": 120.00,
      "category": "Alimentação",
      "transacted_at": "2025-01-02T12:00:00Z",
      "description": "Supermercado"
    },
    {
      "id": "tx_002",
      "amount": 80.00,
      "category": "Educação",
      "transacted_at": "2025-01-01T10:00:00Z",
      "description": "Curso online"
    }
  ],
  "metas_financeiras": {
    "emergencia": 20000.00,
    "viagem": 10000.00,
    "entrada_imovel": 100000.00,
    "aposentadoria": 1000000.00
  }
}
```

## Cenário 3: Cliente com Gastos Surpresa

**Situação**: Cliente que normalmente controla gastos, mas teve gastos inesperados.

```json
{
  "cliente": {
    "nome": "Pedro Santos",
    "idade": 31,
    "profissao": "Professor",
    "estado_civil": "Casado",
    "filhos": 1
  },
  "situacao_financeira": {
    "saldo_atual": 3000.00,
    "renda_mensal": 5000.00,
    "frequencia_pagamento": "MONTHLY",
    "gastos_mes_passado": 4800.00
  },
  "emprestimos": [
    {
      "tipo": "Cartão de Crédito",
      "valor_restante": 2000.00,
      "parcelas_restantes": 6,
      "valor_parcela": 350.00,
      "juros_mensal": 0.020,
      "proximo_vencimento": "2025-01-08"
    }
  ],
  "transacoes_recentes": [
    {
      "id": "tx_001",
      "amount": 800.00,
      "category": "Saúde",
      "transacted_at": "2025-01-02T14:00:00Z",
      "description": "Consulta médica especializada"
    },
    {
      "id": "tx_002",
      "amount": 450.00,
      "category": "Transporte",
      "transacted_at": "2025-01-01T09:00:00Z",
      "description": "Manutenção do carro"
    },
    {
      "id": "tx_003",
      "amount": 120.00,
      "category": "Alimentação",
      "transacted_at": "2024-12-31T18:00:00Z",
      "description": "Supermercado"
    },
    {
      "id": "tx_004",
      "amount": 90.00,
      "category": "Alimentação",
      "transacted_at": "2024-12-30T12:00:00Z",
      "description": "Almoço"
    },
    {
      "id": "tx_005",
      "amount": 85.00,
      "category": "Alimentação",
      "transacted_at": "2024-12-29T19:00:00Z",
      "description": "Jantar"
    }
  ],
  "metas_financeiras": {
    "emergencia": 8000.00,
    "viagem": 4000.00,
    "entrada_imovel": 60000.00,
    "aposentadoria": 400000.00
  }
}
```

## Como Usar os Cenários

1. **Escolha um cenário** que você quer testar
2. **Copie o JSON** do cenário escolhido
3. **Substitua o conteúdo** do arquivo `client_data.json`
4. **Execute o chat**: `python chatbot/main.py`

## Perguntas Sugeridas para Testar

### Para o Cenário 1 (Dificuldades):
- "Como posso sair do vermelho?"
- "Devo priorizar qual dívida primeiro?"
- "Como posso reduzir meus gastos?"

### Para o Cenário 2 (Organizado):
- "Como posso otimizar meus investimentos?"
- "Devo antecipar o financiamento do apartamento?"
- "Qual a melhor estratégia para minha aposentadoria?"

### Para o Cenário 3 (Gastos Surpresa):
- "Como lidar com gastos inesperados?"
- "Devo usar minha reserva de emergência?"
- "Como evitar surpresas financeiras no futuro?"

## Análise Esperada

### Cenário 1:
- ✅ `help_template` deve retornar `over_expenses: true`
- ✅ `surpresa_gastos` pode detectar gastos altos em lazer
- ✅ `lembrete_emprestimo` deve sugerir pagamentos extras

### Cenário 2:
- ✅ `help_template` deve retornar `over_expenses: false`
- ✅ `surpresa_gastos` deve retornar poucos alertas
- ✅ `lembrete_emprestimo` pode sugerir antecipação do financiamento

### Cenário 3:
- ✅ `help_template` pode retornar `over_expenses: true` ou `false`
- ✅ `surpresa_gastos` deve detectar gastos altos em saúde e transporte
- ✅ `lembrete_emprestimo` deve sugerir pagamento extra no cartão

## Personalização

Você pode modificar qualquer cenário para testar situações específicas:

- **Altere valores** de saldo, renda, gastos
- **Adicione/remova empréstimos**
- **Modifique transações** para testar diferentes padrões
- **Ajuste metas** financeiras
- **Mude hábitos** para ver como o assistente responde

Isso permite testar como o sistema se comporta com diferentes perfis financeiros e situações específicas. 