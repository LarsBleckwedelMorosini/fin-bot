#!/usr/bin/env python3
"""
Script para criar dados de cliente personalizados para o Fin-Bot.
Execute este script para gerar um arquivo client_data.json com seus dados.
"""

import json
from datetime import datetime, timedelta
import random

def create_sample_client_data():
    """Cria dados de exemplo para um cliente."""
    
    # Data atual para referência
    today = datetime.now()
    
    # Gera transações dos últimos 7 dias
    transactions = []
    categories = ["Alimentação", "Transporte", "Lazer", "Saúde", "Educação", "Moradia"]
    
    for i in range(10):
        # Data aleatória nos últimos 7 dias
        days_ago = random.randint(0, 7)
        transaction_date = today - timedelta(days=days_ago)
        
        # Valor aleatório entre 20 e 300
        amount = round(random.uniform(20, 300), 2)
        category = random.choice(categories)
        
        transaction = {
            "id": f"tx_{i+1:03d}",
            "amount": amount,
            "category": category,
            "transacted_at": transaction_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "description": f"Transação {i+1} - {category}"
        }
        transactions.append(transaction)
    
    client_data = {
        "cliente": {
            "nome": "Maria Santos",
            "idade": 28,
            "profissao": "Designer Gráfico",
            "estado_civil": "Solteira",
            "filhos": 0
        },
        "situacao_financeira": {
            "saldo_atual": 3200.00,
            "renda_mensal": 3800.00,
            "frequencia_pagamento": "MONTHLY",
            "gastos_mes_passado": 3200.00,
            "gastos_medios_mensais": {
                "alimentacao": 600.00,
                "transporte": 300.00,
                "moradia": 1000.00,
                "saude": 200.00,
                "educacao": 150.00,
                "lazer": 350.00,
                "outros": 400.00
            }
        },
        "emprestimos": [
            {
                "tipo": "Financiamento de Notebook",
                "valor_restante": 8000.00,
                "parcelas_restantes": 18,
                "valor_parcela": 450.00,
                "juros_mensal": 0.012,
                "proximo_vencimento": (today + timedelta(days=12)).strftime("%Y-%m-%d")
            }
        ],
        "transacoes_recentes": transactions,
        "metas_financeiras": {
            "emergencia": 8000.00,
            "viagem": 3000.00,
            "entrada_imovel": 40000.00,
            "aposentadoria": 300000.00
        },
        "habitos": {
            "gasta_mais_que_ganha": False,
            "tem_reserva_emergencia": True,
            "investe_regularmente": False,
            "controla_gastos": True,
            "tem_plano_aposentadoria": False
        }
    }
    
    return client_data

def create_custom_client_data():
    """Interface para criar dados personalizados do cliente."""
    print("🎯 Criador de Dados do Cliente - Fin-Bot")
    print("=" * 50)
    
    # Dados básicos do cliente
    print("\n📋 DADOS PESSOAIS:")
    nome = input("Nome do cliente: ").strip() or "Cliente Teste"
    idade = input("Idade: ").strip() or "30"
    profissao = input("Profissão: ").strip() or "Profissional"
    estado_civil = input("Estado civil: ").strip() or "Solteiro"
    filhos = input("Número de filhos: ").strip() or "0"
    
    print("\n💰 SITUAÇÃO FINANCEIRA:")
    saldo = input("Saldo atual (R$): ").strip() or "2500"
    renda = input("Renda mensal (R$): ").strip() or "4000"
    gastos = input("Gastos do mês passado (R$): ").strip() or "3500"
    
    # Cria dados básicos
    client_data = {
        "cliente": {
            "nome": nome,
            "idade": int(idade),
            "profissao": profissao,
            "estado_civil": estado_civil,
            "filhos": int(filhos)
        },
        "situacao_financeira": {
            "saldo_atual": float(saldo),
            "renda_mensal": float(renda),
            "frequencia_pagamento": "MONTHLY",
            "gastos_mes_passado": float(gastos),
            "gastos_medios_mensais": {
                "alimentacao": 600.00,
                "transporte": 300.00,
                "moradia": 1000.00,
                "saude": 200.00,
                "educacao": 150.00,
                "lazer": 350.00,
                "outros": 400.00
            }
        },
        "emprestimos": [],
        "transacoes_recentes": [],
        "metas_financeiras": {
            "emergencia": 10000.00,
            "viagem": 5000.00,
            "entrada_imovel": 50000.00,
            "aposentadoria": 500000.00
        },
        "habitos": {
            "gasta_mais_que_ganha": False,
            "tem_reserva_emergencia": True,
            "investe_regularmente": False,
            "controla_gastos": True,
            "tem_plano_aposentadoria": False
        }
    }
    
    # Pergunta sobre empréstimos
    tem_emprestimos = input("\n💳 Tem empréstimos? (s/n): ").strip().lower() == 's'
    if tem_emprestimos:
        print("📝 Adicione os empréstimos (deixe vazio para parar):")
        i = 1
        while True:
            tipo = input(f"Tipo do empréstimo {i}: ").strip()
            if not tipo:
                break
                
            valor_restante = float(input(f"Valor restante (R$): ").strip() or "10000")
            parcelas = int(input(f"Parcelas restantes: ").strip() or "12")
            valor_parcela = float(input(f"Valor da parcela (R$): ").strip() or "1000")
            juros = float(input(f"Juros mensal (%): ").strip() or "1.5") / 100
            vencimento = input(f"Próximo vencimento (YYYY-MM-DD): ").strip() or "2025-01-15"
            
            emprestimo = {
                "tipo": tipo,
                "valor_restante": valor_restante,
                "parcelas_restantes": parcelas,
                "valor_parcela": valor_parcela,
                "juros_mensal": juros,
                "proximo_vencimento": vencimento
            }
            client_data["emprestimos"].append(emprestimo)
            i += 1
    
    return client_data

def main():
    """Função principal do script."""
    print("🎯 Criador de Dados do Cliente - Fin-Bot")
    print("=" * 50)
    print("1. Usar dados de exemplo")
    print("2. Criar dados personalizados")
    print("3. Sair")
    
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    if choice == "1":
        client_data = create_sample_client_data()
        print("\n✅ Dados de exemplo criados!")
    elif choice == "2":
        client_data = create_custom_client_data()
        print("\n✅ Dados personalizados criados!")
    else:
        print("👋 Até logo!")
        return
    
    # Salva os dados
    filename = "client_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(client_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Dados salvos em '{filename}'")
    print(f"👤 Cliente: {client_data['cliente']['nome']}")
    print(f"💰 Saldo: R$ {client_data['situacao_financeira']['saldo_atual']:.2f}")
    print(f"💵 Renda: R$ {client_data['situacao_financeira']['renda_mensal']:.2f}")
    
    if client_data['emprestimos']:
        print(f"💳 Empréstimos: {len(client_data['emprestimos'])}")
    
    print(f"\n🚀 Agora você pode executar: python chatbot/main.py")

if __name__ == "__main__":
    main() 