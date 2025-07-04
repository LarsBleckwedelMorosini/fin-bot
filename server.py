from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any


mcp = FastMCP("HelpTemplateServer", host="0.0.0.0", port=3333)

@mcp.tool(name="help_template", title="Gera template de ajuda financeira")
async def help_template_tool(balance_available: float, last_month_amount: float, income: float, frequency: str) -> dict:
    """
    Gera um template de ajuda financeira com base no saldo disponível, o valor gasto no mês passado, o rendimento com base na frequência de pagamento.

    Args:
        balance_available: float - Saldo disponível
        last_month_amount: float - Valor gasto no mês passado
        income: float - Rendimento com base na frequência de pagamento
        frequency: str - Frequência de pagamento
    
    frequency:
        DAILY: 30 (30 dias)
        WEEKLY: 4 (4 semanas)
        FORTNIGHTLY: 2 (2 semanas)
        MONTHLY: 1 (1 mês)
        BIMONTHLY: 0.5 (2 meses)
        QUARTERLY: 1/3 (3 meses)
        BIANNUALLY: 1/6 (6 meses)
        ANNUALLY: 1/12 (12 meses)

    Returns:
        dict - Dicionário com a chave "over_expenses" contendo um booleano indicando se o saldo disponível é suficiente para cobrir os gastos do mês. Se over_expenses for False, o saldo disponível é suficiente para cobrir os gastos do mês.
    """
    factor = {
        "DAILY": 30,
        "WEEKLY": 4,
        "FORTNIGHTLY": 2,
        "MONTHLY": 1,
        "BIMONTHLY": 0.5,
        "QUARTERLY": 1/3,
        "BIANNUALLY": 1/6,
        "ANNUALLY": 1/12,
    }
    multi = factor.get(frequency, 1)
    month_income = income * multi
    if balance_available is not None and month_income:
        return {"over_expenses": (balance_available - last_month_amount + month_income) < 0}
    return {"over_expenses": False}

@mcp.tool(name="surpresa_gastos", title="Sinaliza Gastos “Surpresa”")
async def surpresa_gastos_tool(transactions: List[Dict[str, Any]], reference_date: str | None = None, window_days: int = 7, threshold_pct: float = 0.30) -> Dict[str, Any]:
    """
    Retorna alertas de categorias em que o gasto recente ficou > threshold_pct acima da média diária dos últimos window_days.

    Args:
        transactions: List[Dict[str, Any]] - Lista de transações
        reference_date: str | None - Data de referência para o cálculo
        window_days: int - Número de dias para o cálculo da média diária
        threshold_pct: float - Percentual de tolerância para o cálculo da média diária
    
    transactions: [
      {
        "id": "...",
        "amount": 123.45,
        "category": "Alimentação",
        "transacted_at": "2025-07-02T14:22:00Z"
      }, ...
    ]

    Returns:
        Dict[str, Any] - Dicionário com a chave "alerts" contendo uma lista de alertas.
    """
    # 1) define datas
    today = datetime.now(timezone.utc).date()
    if reference_date:
        today = datetime.fromisoformat(reference_date).date()
    
    # 2) encontra a data mais recente nas transações
    datas_transacoes = [datetime.fromisoformat(tx["transacted_at"]).date() for tx in transactions]
    if not datas_transacoes:
        return {"alerts": []}
    
    data_mais_recente = max(datas_transacoes)
    
    # 3) calcula janela de análise (window_days antes da data mais recente)
    inicio = data_mais_recente - timedelta(days=window_days - 1)
    
    # 4) agrupa valores por categoria e dia
    gastos_por_cat: Dict[str, Dict[datetime, float]] = {}
    for tx in transactions:
        dt = datetime.fromisoformat(tx["transacted_at"]).date()
        if inicio <= dt <= data_mais_recente:
            gastos_por_cat.setdefault(tx["category"], {}).setdefault(dt, 0.0) # type: ignore
            gastos_por_cat[tx["category"]][dt] += tx["amount"] # type: ignore

    # 5) calcula média diária de cada categoria (excluindo o dia mais recente)
    media_diaria: Dict[str, float] = {}
    for cat, dias in gastos_por_cat.items():
        # Remove o dia mais recente do cálculo da média
        dias_sem_recente = {d: v for d, v in dias.items() if d < data_mais_recente}
        if dias_sem_recente:
            media_diaria[cat] = sum(dias_sem_recente.values()) / len(dias_sem_recente)
        else:
            # Se não há dados históricos, usa um valor baixo como referência
            media_diaria[cat] = 50.0  # R$ 50 como referência mínima

    # 6) total gasto no dia mais recente por categoria
    gasto_recente: Dict[str, float] = {}
    for tx in transactions:
        dt = datetime.fromisoformat(tx["transacted_at"]).date()
        if dt == data_mais_recente:
            gasto_recente.setdefault(tx["category"], 0.0)
            gasto_recente[tx["category"]] += tx["amount"]

    # 7) detecta surpresas
    alertas = []
    for cat, val in gasto_recente.items():
        media = media_diaria.get(cat, 0)
        if media and val > media * (1 + threshold_pct):
            alertas.append({
                "category": cat,
                "spent_recently": round(val, 2),
                "daily_avg": round(media, 2),
                "pct_over": round((val / media - 1) * 100, 1),
                "date": data_mais_recente.strftime("%Y-%m-%d"),
            })

    return {"alerts": alertas}

@mcp.tool(name="lembrete_emprestimo", title="Lembrete & Turbo na Parcela do Empréstimo")
async def lembrete_emprestimo_tool(next_payment_date: str, minimum_installment_amount: float, installments_outstanding: int, interest_rate: float, extra_amount: float) -> dict:
    """
    Gera um lembrete de vencimento de parcela de empréstimo e sugere um pagamento extra para reduzir juros.

    Args:
        next_payment_date: str - Data ISO da próxima parcela (ex: "2025-07-10").
        minimum_installment_amount: float - valor mínimo da parcela.
        installments_outstanding: int - quantas parcelas faltam.
        interest_rate: float - juros mensal 
        extra_amount: float - valor extra sugerido (entre 10 e 500). Se não for informado, utilize um valor que seja o suficiente para reduzir juros em R$ 5.00 ou mais, mas não mais que R$ 200.00 que o cliente possa pagar.

    Returns:
        dict com:
            - days_to_due: número de dias até o vencimento.
            - base_amount: valor mínimo da parcela.
            - extra_amount: valor extra sugerido.
            - estimated_interest_saved: valor estimado de economia de juros.
            - message: texto informal para usar de referência.
    """
    # 1) Parse da data
    due = datetime.fromisoformat(next_payment_date).date()

    # 2) Normaliza hoje em UTC e dias até o vencimento
    today = datetime.now(timezone.utc).date()
    days_to_due = max((due - today).days, 0)

    # 4) Limita extra_amount entre R$10 e R$500
    extra = min(max(extra_amount, 10.0), 500.0)

    # 5) Estima economia de juros
    #    extra reduz o principal em cada parcela restante
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
        for _ in range(n_periods):
            interest = balance * rate
            amort = payment - interest
            balance -= amort
            total_interest += interest
        return total_interest

    # dentro da sua tool:
    # 1) calcula o valor presente (saldo devedor) daqui a 0 usando fórmula PRICE:
    #    PV = payment * (1 - (1+rate)**(-n)) / rate
    pv = minimum_installment_amount * (1 - (1 + interest_rate) ** (-installments_outstanding)) / interest_rate
    orig_juros = simulate_schedule(pv, interest_rate, installments_outstanding, minimum_installment_amount)
    balance_after_extra = pv
    interest1 = balance_after_extra * interest_rate
    amort1 = minimum_installment_amount + extra - interest1
    balance_after_extra -= amort1
    new_juros = interest1

    for _ in range(installments_outstanding - 1):
        i = balance_after_extra * interest_rate
        balance_after_extra -= (minimum_installment_amount - i)
        new_juros += i

    # 4) economia real
    estimated_interest_saved = round(orig_juros - new_juros, 2)

    # 6) Formata data num texto amigável
    due_str = due.strftime("%d/%m/%Y")

    # 7) Monta a mensagem
    message = (
        f"Oi! Sua próxima parcela de R$ {minimum_installment_amount:.2f} "
        f"vence em {due_str} (daqui a {days_to_due} dia(s)).\n"
        f"Que tal antecipar mais R$ {extra:.2f}? Assim, você pode economizar "
        f"aproximadamente R$ {estimated_interest_saved:.2f} em juros até o fim!"
    )

    return {
        "days_to_due": days_to_due,
        "base_amount": minimum_installment_amount,
        "extra_amount": extra,
        "estimated_interest_saved": estimated_interest_saved,
        "message": message
    }

if __name__ == "__main__":
    mcp.run(transport="sse")