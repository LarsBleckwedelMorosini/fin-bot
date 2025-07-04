import asyncio
import json
from mcp.client.sse import sse_client
from mcp import ClientSession

async def test_sse_connection():
    """Test SSE connection to the MCP server"""
    url = "http://localhost:3333/sse"  # Default SSE endpoint
    
    print("🔌 Conectando ao servidor SSE...")
    
    try:
        async with sse_client(url) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                print("✅ Conexão estabelecida!")
                
                # Initialize the session
                await session.initialize()
                print("✅ Sessão inicializada!")
                
                # List available tools
                tools = await session.list_tools()
                print(f"🔧 Ferramentas disponíveis: {[tool.name for tool in tools.tools]}")
                
                # Test the help_template tool
                print("🧪 Testando help_template...")
                result = await session.call_tool("help_template", {
                    "balance_available": 1500.0,
                    "last_month_amount": 3000.0,
                    "income": 2000.0,
                    "frequency": "MONTHLY"
                })
                
                print("✅ Resultado recebido!")
                print(f"📊 Resultado: {result}")
                
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    asyncio.run(test_sse_connection())