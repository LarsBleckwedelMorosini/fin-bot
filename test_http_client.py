import httpx
import json

async def test_http_connection():
    """Test HTTP connection to the MCP server"""
    base_url = "http://localhost:3333"
    
    print("🔌 Testando conexão HTTP...")
    
    try:
        # Test 1: Initialize session
        print("1️⃣ Inicializando sessão...")
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "clientName": "test_client"
            }
        }
        
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            # Initialize
            init_response = await client.post(f"{base_url}/messages", json=init_payload, headers=headers)
            print(f"✅ Initialize response: {init_response.status_code}")
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                print(f"📋 Session info: {init_data}")
                
                # Test 2: Call tool
                print("2️⃣ Chamando ferramenta help_template...")
                tool_payload = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "callTool",
                    "params": {
                        "name": "help_template",
                        "arguments": {
                            "balance_available": 1500.0,
                            "last_month_amount": 3000.0,
                            "income": 2000.0,
                            "frequency": "MONTHLY"
                        }
                    }
                }
                
                tool_response = await client.post(f"{base_url}/messages", json=tool_payload, headers=headers)
                print(f"✅ Tool response: {tool_response.status_code}")
                
                if tool_response.status_code == 200:
                    tool_data = tool_response.json()
                    print(f"📊 Resultado: {json.dumps(tool_data, indent=2)}")
                else:
                    print(f"❌ Erro na chamada da ferramenta: {tool_response.text}")
            else:
                print(f"❌ Erro na inicialização: {init_response.text}")
                
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_http_connection()) 