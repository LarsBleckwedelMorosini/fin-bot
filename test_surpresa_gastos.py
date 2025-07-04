#!/usr/bin/env python3
"""
Script para testar a ferramenta surpresa_gastos com dados de exemplo.
"""

import asyncio
import json
from datetime import datetime, timedelta
from mcp.client.sse import sse_client
from mcp import ClientSession

async def test_surpresa_gastos():
    """Testa a ferramenta surpresa_gastos com diferentes cenários."""
    
    # Conecta ao servidor
    url = "http://localhost:3333/sse"
    
    print("🔌 Conectando ao servidor SSE...")
    
    try:
        async with sse_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ Conexão estabelecida!")
                
                # Teste 1: Transação com valor muito alto (R$ 100.000)
                print("\n🧪 TESTE 1: Transação de R$ 100.000 em Lazer")
                transactions_1 = [
                    {
                        "id": "tx_001",
                        "amount": 100000.00,
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
                ]
                
                result_1 = await session.call_tool("surpresa_gastos", {
                    "transactions": transactions_1,
                    "window_days": 7,
                    "threshold_pct": 0.30
                })
                
                print(f"📊 Resultado Teste 1: {result_1}")
                
                # Teste 2: Múltiplas transações com valores normais
                print("\n🧪 TESTE 2: Múltiplas transações normais")
                transactions_2 = [
                    {
                        "id": "tx_001",
                        "amount": 50.00,
                        "category": "Alimentação",
                        "transacted_at": "2025-01-01T12:00:00Z",
                        "description": "Almoço"
                    },
                    {
                        "id": "tx_002",
                        "amount": 45.00,
                        "category": "Alimentação",
                        "transacted_at": "2025-01-02T12:00:00Z",
                        "description": "Almoço"
                    },
                    {
                        "id": "tx_003",
                        "amount": 200.00,
                        "category": "Alimentação",
                        "transacted_at": "2025-01-03T12:00:00Z",
                        "description": "Restaurante caro"
                    }
                ]
                
                result_2 = await session.call_tool("surpresa_gastos", {
                    "transactions": transactions_2,
                    "window_days": 7,
                    "threshold_pct": 0.30
                })
                
                print(f"📊 Resultado Teste 2: {result_2}")
                
                # Teste 3: Transações em diferentes datas
                print("\n🧪 TESTE 3: Transações em diferentes datas")
                transactions_3 = [
                    {
                        "id": "tx_001",
                        "amount": 100.00,
                        "category": "Transporte",
                        "transacted_at": "2024-12-30T08:00:00Z",
                        "description": "Combustível"
                    },
                    {
                        "id": "tx_002",
                        "amount": 120.00,
                        "category": "Transporte",
                        "transacted_at": "2024-12-31T08:00:00Z",
                        "description": "Combustível"
                    },
                    {
                        "id": "tx_003",
                        "amount": 500.00,
                        "category": "Transporte",
                        "transacted_at": "2025-01-01T08:00:00Z",
                        "description": "Manutenção do carro"
                    }
                ]
                
                result_3 = await session.call_tool("surpresa_gastos", {
                    "transactions": transactions_3,
                    "window_days": 7,
                    "threshold_pct": 0.30
                })
                
                print(f"📊 Resultado Teste 3: {result_3}")
                
                # Teste 4: Sem transações
                print("\n🧪 TESTE 4: Sem transações")
                result_4 = await session.call_tool("surpresa_gastos", {
                    "transactions": [],
                    "window_days": 7,
                    "threshold_pct": 0.30
                })
                
                print(f"📊 Resultado Teste 4: {result_4}")
                
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    asyncio.run(test_surpresa_gastos()) 