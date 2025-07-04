#!/usr/bin/env python3
"""
Script para testar e debugar os cálculos da ferramenta lembrete_emprestimo.
"""

def simulate_schedule(principal: float, rate: float, n_periods: int, payment: float):
    """
    Simula um cronograma PRICE puro:
    - principal: saldo devedor inicial
    - rate: taxa de juros por período (mensal)
    - n_periods: número de parcelas
    - payment: valor fixo de cada parcela
    Retorna soma dos juros pagos ao longo de todas as parcelas.
    """
    total_interest = 0.0
    balance = principal
    print(f"🔍 Simulando cronograma:")
    print(f"   Principal inicial: R$ {principal:.2f}")
    print(f"   Taxa mensal: {rate*100:.1f}%")
    print(f"   Parcelas: {n_periods}")
    print(f"   Valor parcela: R$ {payment:.2f}")
    print()
    
    for period in range(n_periods):
        interest = balance * rate
        amort = payment - interest
        balance -= amort
        total_interest += interest
        print(f"   Período {period+1}: Juros=R$ {interest:.2f}, Amort=R$ {amort:.2f}, Saldo=R$ {balance:.2f}")
    
    print(f"   Total de juros: R$ {total_interest:.2f}")
    return total_interest

def test_loan_calculation():
    """Testa o cálculo de economia de juros com diferentes valores."""
    
    # Parâmetros do empréstimo (baseado nos dados do cliente)
    minimum_installment_amount = 1200.0  # Valor da parcela
    installments_outstanding = 36        # Parcelas restantes
    interest_rate = 0.018               # Juros mensal (1.8%)
    
    # Calcula o valor presente (saldo devedor)
    pv = minimum_installment_amount * (1 - (1 + interest_rate) ** (-installments_outstanding)) / interest_rate
    print(f"💰 Valor presente (saldo devedor): R$ {pv:.2f}")
    print()
    
    # Simula cronograma original
    print("📊 CRONOGRAMA ORIGINAL:")
    orig_juros = simulate_schedule(pv, interest_rate, installments_outstanding, minimum_installment_amount)
    print()
    
    # Testa diferentes valores de antecipação
    test_amounts = [100, 200, 300, 500]
    
    for extra in test_amounts:
        print(f"🧮 TESTANDO ANTECIPAÇÃO DE R$ {extra:.2f}:")
        
        # Simula com antecipação
        balance_after_extra = pv
        interest1 = balance_after_extra * interest_rate
        amort1 = minimum_installment_amount + extra - interest1
        balance_after_extra -= amort1
        new_juros = interest1
        
        print(f"   Primeira parcela: Juros=R$ {interest1:.2f}, Amort=R$ {amort1:.2f}, Saldo=R$ {balance_after_extra:.2f}")
        
        # Simula parcelas restantes
        for period in range(installments_outstanding - 1):
            i = balance_after_extra * interest_rate
            amort = minimum_installment_amount - i
            balance_after_extra -= amort
            new_juros += i
            if period < 2:  # Mostra apenas as primeiras parcelas para não poluir
                print(f"   Parcela {period+2}: Juros=R$ {i:.2f}, Amort=R$ {amort:.2f}, Saldo=R$ {balance_after_extra:.2f}")
        
        if installments_outstanding > 3:
            print(f"   ... ({installments_outstanding-3} parcelas restantes)")
        
        print(f"   Total de juros com antecipação: R$ {new_juros:.2f}")
        
        # Calcula economia
        economia = orig_juros - new_juros
        print(f"   💰 ECONOMIA: R$ {economia:.2f}")
        print(f"   📈 Economia por R$ 100 antecipado: R$ {economia/extra*100:.2f}")
        print()

def test_proportionality():
    """Testa se a economia é proporcional ao valor antecipado."""
    print("🔬 TESTE DE PROPORCIONALIDADE")
    print("=" * 50)
    
    # Parâmetros fixos
    minimum_installment_amount = 1200.0
    installments_outstanding = 36
    interest_rate = 0.018
    
    # Calcula valor presente
    pv = minimum_installment_amount * (1 - (1 + interest_rate) ** (-installments_outstanding)) / interest_rate
    
    # Simula cronograma original
    def quick_simulate(extra_amount):
        balance = pv
        interest1 = balance * interest_rate
        amort1 = minimum_installment_amount + extra_amount - interest1
        balance -= amort1
        total_juros = interest1
        
        for _ in range(installments_outstanding - 1):
            i = balance * interest_rate
            balance -= (minimum_installment_amount - i)
            total_juros += i
        
        return total_juros
    
    orig_juros = quick_simulate(0)
    
    # Testa valores de 100 em 100
    results = []
    for extra in range(100, 501, 100):
        new_juros = quick_simulate(extra)
        economia = orig_juros - new_juros
        economia_por_100 = economia / extra * 100
        results.append((extra, economia, economia_por_100))
        print(f"R$ {extra:3.0f} antecipado → R$ {economia:6.2f} economia → R$ {economia_por_100:6.2f} por R$ 100")
    
    # Verifica se é proporcional
    print("\n📊 ANÁLISE DE PROPORCIONALIDADE:")
    first_rate = results[0][2]
    for extra, economia, rate in results:
        desvio = abs(rate - first_rate) / first_rate * 100
        print(f"R$ {extra:3.0f}: {rate:6.2f} por R$ 100 (desvio: {desvio:5.1f}%)")
    
    if all(abs(r[2] - first_rate) / first_rate < 0.01 for r in results):
        print("✅ Cálculo é proporcional!")
    else:
        print("❌ Cálculo NÃO é proporcional!")

if __name__ == "__main__":
    print("🧮 TESTE DE CÁLCULOS DE EMPRÉSTIMO")
    print("=" * 60)
    
    test_loan_calculation()
    print("\n" + "=" * 60)
    test_proportionality() 