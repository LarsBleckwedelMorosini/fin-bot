import os
import json
import asyncio
import warnings
from typing import Any, Dict, List
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.beta.threads import Message
from mcp.client.sse import sse_client
from mcp import ClientSession

# Suprime warnings de deprecação do OpenAI
warnings.filterwarnings("ignore", message=".*The Assistants API is deprecated.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSIS_ID = os.getenv("OPENAI_ASSIS_ID")

class MCPSSEClient:
    def __init__(self, openai_model: str = "gpt-4o-mini", client_data_file: str = "client_data.json"):
        self.openai = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model = openai_model
        self.exit_stack = AsyncExitStack()
        self.client_data_file = client_data_file
        self.client_data = None

    async def connect(self, url: str = "http://0.0.0.0:3333/sse"):
        """Abre e mantém a conexão SSE + MCP session ativa."""
        # print("🔌 Conectando ao servidor SSE...")
        try:
            # entra no exit_stack, salvando os contextos abertos
            read_stream, write_stream = await self.exit_stack.enter_async_context(sse_client(url))
            self.session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
            await self.session.initialize()
            # print("✅ Conexão SSE e sessão MCP inicializadas!")
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            await self.close()
            raise
    
    async def load_client_data(self):
        """Carrega os dados do cliente do arquivo JSON."""
        try:
            with open(self.client_data_file, 'r', encoding='utf-8') as f:
                self.client_data = json.load(f)
            # print(f"✅ Dados do cliente carregados: {self.client_data['cliente']['nome']}")
            initial_data_message = f"""
            DADOS DO CLIENTE (disponíveis para toda a conversa):
            {json.dumps(self.client_data, indent=2, ensure_ascii=False)}

            IMPORTANTE: Esta não é a primeira mensagem do cliente, mas sim os dados do cliente que estão disponíveis para toda a conversa. Se precisar de cálculos específicos, use as ferramentas disponíveis com os dados corretos do cliente. Se precisar de mais informações, pergunte ao cliente.
            """
            await self.send(initial_data_message)
            return True
        except FileNotFoundError:
            # print(f"⚠️ Arquivo {self.client_data_file} não encontrado. Continuando sem dados do cliente.")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            return False

    async def start_thread(self):
        """Cria nova thread e guarda thread_id + assistant_id."""
        thread = await self.openai.beta.threads.create()
        self.thread_id = thread.id
        self.assistant_id = OPENAI_ASSIS_ID

    async def analyze_client_situation(self) -> str:
        """Analisa a situação financeira do cliente usando as ferramentas disponíveis."""
        if not self.client_data:
            return "Nenhum dado do cliente disponível para análise."
        
        analysis_results = []
        
        # 1. Análise básica de gastos vs renda
        situacao = self.client_data['situacao_financeira']
        help_result = await self.session.call_tool("help_template", {
            "balance_available": situacao['saldo_atual'],
            "last_month_amount": situacao['gastos_mes_passado'],
            "income": situacao['renda_mensal'],
            "frequency": situacao['frequencia_pagamento']
        })
        
        if hasattr(help_result, 'content') and help_result.content:
            over_expenses = getattr(help_result.content[0], 'text', str(help_result.content[0]))
        else:
            over_expenses = str(help_result)
        
        analysis_results.append(f"📊 Análise de Gastos: {over_expenses}")
        
        # 2. Análise de gastos surpresa
        if 'transacoes_recentes' in self.client_data:
            surprise_result = await self.session.call_tool("surpresa_gastos", {
                "transactions": self.client_data['transacoes_recentes'],
                "window_days": 7,
                "threshold_pct": 0.30
            })
            
            if hasattr(surprise_result, 'content') and surprise_result.content:
                alerts = getattr(surprise_result.content[0], 'text', str(surprise_result.content[0]))
            else:
                alerts = str(surprise_result)
            
            analysis_results.append(f"🚨 Alertas de Gastos: {alerts}")
        
        # 3. Análise de empréstimos
        if 'emprestimos' in self.client_data:
            loan_analyses = []
            for emprestimo in self.client_data['emprestimos']:
                loan_result = await self.session.call_tool("lembrete_emprestimo", {
                    "next_payment_date": emprestimo['proximo_vencimento'],
                    "minimum_installment_amount": emprestimo['valor_parcela'],
                    "installments_outstanding": emprestimo['parcelas_restantes'],
                    "interest_rate": emprestimo['juros_mensal'],
                    "extra_amount": 100.0  # Valor sugerido
                })
                
                # Tenta extrair o JSON corretamente
                if hasattr(loan_result, 'content') and loan_result.content:
                    text = getattr(loan_result.content[0], 'text', str(loan_result.content[0]))
                else:
                    text = str(loan_result)
                try:
                    data = json.loads(text)
                    msg = (
                        f"Dias até o vencimento: {data.get('days_to_due')}\n"
                        f"Valor da parcela: R$ {data.get('base_amount'):.2f}\n"
                        f"Valor extra sugerido: R$ {data.get('extra_amount'):.2f}\n"
                        f"Economia estimada de juros: R$ {data.get('estimated_interest_saved'):.2f}\n"
                        f"Mensagem: {data.get('message')}"
                    )
                except Exception:
                    msg = text
                loan_analyses.append(f"💳 {emprestimo['tipo']}: {msg}")
            
            analysis_results.extend(loan_analyses)
        
        return "\n".join(analysis_results)

    async def list_tools(self) -> List[Dict[str, Any]]:
        tools = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in tools.tools
        ]

    async def send(self, prompt: str) -> Message:
        """Envia `prompt` pelo sistema de threads + MCP tools e retorna a Message final."""
        if not self.thread_id or not self.assistant_id:
            raise RuntimeError("Thread não iniciada! Chame start_thread() primeiro.")

        # 1) envia a mensagem do usuário para a thread
        await self.openai.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=prompt
        )

        # 2) dispara um run, permitindo escolhas de tools
        tools = await self.list_tools()
        run = await self.openai.beta.threads.runs.create(
            thread_id   = self.thread_id,
            assistant_id= self.assistant_id,
            tools       = tools,  # type: ignore
            tool_choice = "auto",
        )

        # 3) aguarda até o run completar ou exigir ação
        while run.status not in ("completed", "requires_action"):
            await asyncio.sleep(0.5)
            run = await self.openai.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run.id
            )

        if run.status == "requires_action" and run.required_action:
            calls = run.required_action.submit_tool_outputs.tool_calls
            outputs = []
            for call in calls:
                fn_name = call.function.name
                args    = json.loads(call.function.arguments)
                tool_res = await self.session.call_tool(fn_name, args)
                content = ""

                if hasattr(tool_res, "content") and tool_res.content:
                    content = getattr(tool_res.content[0], "text", str(tool_res.content[0]))
                else:
                    content = str(tool_res)

                outputs.append({
                    "tool_call_id": call.id,
                    "output": content
                })

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                run = await self.openai.beta.threads.runs.submit_tool_outputs(
                    thread_id   = self.thread_id,
                    run_id      = run.id,
                    tool_outputs= outputs
                )

            while run.status != "completed":
                await asyncio.sleep(0.5)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    run = await self.openai.beta.threads.runs.retrieve(
                        thread_id=self.thread_id, run_id=run.id
                    )

        # 6) recupera as mensagens da thread (as mais recentes por ordem decrescente)
        msgs = await self.openai.beta.threads.messages.list(thread_id=self.thread_id)
        # normalmente, a última é a que o assistente acabou de gerar
        return msgs.data[0]

    async def close(self):
        """Fecha streams e sessão MCP."""
        await self.exit_stack.aclose()

    def extract_text(self, message: Message) -> str:
        """Extrai o texto de uma mensagem do OpenAI de forma segura."""
        if message.content and len(message.content) > 0:
            content_block = message.content[0]
            if hasattr(content_block, 'text') and hasattr(content_block.text, 'value'): # type: ignore
                return content_block.text.value  # type: ignore
        return "Sem resposta de texto disponível"


async def main():
    client = MCPSSEClient()
    try:
        await client.connect("http://localhost:3333/sse")
        await client.start_thread()
        
        # Carrega dados do cliente
        await client.load_client_data()
        
        # Se tem dados do cliente, faz análise inicial
        if client.client_data:
            
            try:
                analysis = await client.analyze_client_situation()
                # Envia análise para o assistente como contexto inicial
                initial_context = f"""
                Olá! Sou o assistente financeiro. Acabei de analisar a situação do cliente {client.client_data['cliente']['nome']} e aqui está o resumo da análise inicial:
                
                {analysis}
                
                Agora você pode me fazer perguntas sobre a situação financeira do cliente. Tenho acesso completo aos dados e posso usar as ferramentas financeiras para cálculos específicos.
                """
                
                response = await client.send(initial_context)
                print(f"\n🤖 Assistente: {client.extract_text(response)}")
                
            except Exception as e:
                print(f"⚠️ Erro na análise inicial: {e}")
        
        # Flag para controlar o loop
        running = True
        
        while running:
            try:
                # Pega input do usuário com timeout para permitir interrupção
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: input("\n💬 Você: ").strip()
                )
                
                # Verifica se quer sair
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    print("👋 Até logo!")
                    running = False
                    continue
                
                # Se input vazio, continua
                if not user_input:
                    continue
                
                # Envia mensagem e recebe resposta
                response = await client.send(user_input)
                print(f"\n🤖 Assistente: {client.extract_text(response)}")
                
            except KeyboardInterrupt:
                print("\n👋 Interrompido pelo usuário. Até logo!")
                running = False
            except EOFError:
                print("\n👋 Entrada finalizada. Até logo!")
                running = False
            except Exception as e:
                print(f"❌ Erro ao processar mensagem: {e}")
                # Continua o loop mesmo com erro

    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())