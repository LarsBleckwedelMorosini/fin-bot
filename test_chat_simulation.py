#!/usr/bin/env python3
"""
Teste que simula exatamente o que aconteceu no chat para identificar o erro.
"""

import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession

async def test_chat_simulation():
    """Simula exatamente o que aconteceu no chat."""
    
    url = "http://localhost:3333/sse"
    
    print("🔌 Conectando ao servidor SSE...")
    
    try:
        async with sse_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ Conexão estabelecida!")
                
                # Simula a chamada que o chat fez para R$ 100
                print("\n🧪 TESTE 1: Antecipação de R$ 100 (como no chat original)")
                result_100 = await session.call_tool("lembrete_emprestimo", {
                    "next_payment_date": "2025-07-20",
                    "minimum_installment_amount": 1200.0,
                    "installments_outstanding": 36,
                    "interest_rate": 0.018,
                    "extra_amount": 100.0
                })
                
                print(f"📊 Resultado para R$ 100: {result_100}")
                
                # Simula a chamada que o chat fez para R$ 300
                print("\n🧪 TESTE 2: Antecipação de R$ 300 (como no chat)")
                result_300 = await session.call_tool("lembrete_emprestimo", {
                    "next_payment_date": "2025-07-20",
                    "minimum_installment_amount": 1200.0,
                    "installments_outstanding": 36,
                    "interest_rate": 0.018,
                    "extra_amount": 300.0
                })
                
                print(f"📊 Resultado para R$ 300: {result_300}")
                
                # Verifica se os resultados são proporcionais
                if hasattr(result_100, 'content') and result_100.content:
                    economia_100 = getattr(result_100.content[0], 'text', str(result_100.content[0]))
                else:
                    economia_100 = str(result_100)
                
                if hasattr(result_300, 'content') and result_300.content:
                    economia_300 = getattr(result_300.content[0], 'text', str(result_300.content[0]))
                else:
                    economia_300 = str(result_300)
                
                print(f"\n📋 RESULTADOS BRUTOS:")
                print(f"R$ 100: {economia_100}")
                print(f"R$ 300: {economia_300}")
                
                # Tenta extrair os valores numéricos
                try:
                    import json
                    import re
                    
                    # Extrai valores usando regex
                    def extract_savings(text):
                        # Procura especificamente por "estimated_interest_saved": valor
                        match = re.search(r'"estimated_interest_saved":\s*(\d+\.?\d*)', text)
                        if match:
                            return float(match.group(1))
                        return None
                    
                    savings_100 = extract_savings(economia_100)
                    savings_300 = extract_savings(economia_300)
                    
                    print(f"\n💰 VALORES EXTRAÍDOS:")
                    print(f"Economia R$ 100: {savings_100}")
                    print(f"Economia R$ 300: {savings_300}")
                    
                    if savings_100 and savings_300:
                        ratio = savings_300 / savings_100
                        expected_ratio = 3.0
                        print(f"\n📊 ANÁLISE:")
                        print(f"Razão real: {ratio:.2f}")
                        print(f"Razão esperada: {expected_ratio:.2f}")
                        print(f"Diferença: {abs(ratio - expected_ratio):.2f}")
                        
                        if abs(ratio - expected_ratio) < 0.1:
                            print("✅ Resultados são proporcionais!")
                        else:
                            print("❌ Resultados NÃO são proporcionais!")
                            
                except Exception as e:
                    print(f"❌ Erro ao analisar resultados: {e}")
                
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat_simulation()) 