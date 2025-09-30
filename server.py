#!/usr/bin/env python3
"""
Minimal MCP Server with A2A Bridge Capability
Phase 1: Basic proxy pattern with simple request/response

DISCLAIMER: This is a simplified demonstration of A2A protocol concepts.
This implementation uses basic HTTP/JSON-RPC style communication as a proxy
for true A2A protocol compliance. In production, this would need:
- Full A2A protocol specification compliance
- Proper authentication and security
- Streaming support (SSE)
- Rate limiting and governance enforcement
- Error handling and retry logic

Use this as a learning tool and architectural pattern demonstration.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
import aiohttp
from datetime import datetime

# MCP Protocol handlers (simplified)
@dataclass
class MCPTool:
    name: str
    description: str
    parameters: Dict[str, Any]
    
@dataclass
class A2AMessage:
    role: str  # "user" or "agent"
    parts: List[Dict[str, Any]]
    
@dataclass
class AgentCard:
    name: str
    endpoint: str
    capabilities: List[str]
    auth_type: str = "api_key"
    discovered_at: Optional[str] = None

class A2ABridge:
    """Handles A2A protocol operations"""
    
    def __init__(self):
        self.discovered_agents: Dict[str, AgentCard] = {}
        self.session = None
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self):
        """Set up HTTP session for A2A calls"""
        self.session = aiohttp.ClientSession()
        
    async def discover_agent(self, endpoint: str) -> Optional[AgentCard]:
        """Fetch agent card from endpoint"""
        try:
            # Standard A2A discovery endpoint
            card_url = f"{endpoint}/.well-known/agent-card.json"
            
            async with self.session.get(card_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    agent = AgentCard(
                        name=data.get("name", "Unknown"),
                        endpoint=endpoint,
                        capabilities=data.get("capabilities", []),
                        auth_type=data.get("auth", {}).get("type", "none"),
                        discovered_at=datetime.now().isoformat()
                    )
                    self.discovered_agents[agent.name] = agent
                    return agent
        except Exception as e:
            self.logger.error(f"Failed to discover agent at {endpoint}: {e}")
        return None
        
    async def send_message(self, agent_name: str, message: A2AMessage) -> Dict[str, Any]:
        """Send a message to a discovered A2A agent"""
        if agent_name not in self.discovered_agents:
            return {"error": f"Agent {agent_name} not discovered"}
            
        agent = self.discovered_agents[agent_name]
        
        # Simple A2A message send (JSON-RPC style)
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/send",
            "params": {
                "message": asdict(message)
            }
        }
        
        try:
            async with self.session.post(
                f"{agent.endpoint}/api/a2a",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get("result", {})
                else:
                    return {"error": f"A2A call failed: {resp.status}"}
        except Exception as e:
            return {"error": str(e)}
            
    async def cleanup(self):
        """Close connections"""
        if self.session:
            await self.session.close()

class MCPServer:
    """MCP Server that exposes A2A as tools"""
    
    def __init__(self):
        self.a2a_bridge = A2ABridge()
        self.tools = self._register_tools()
        self.logger = logging.getLogger(__name__)
        
    def _register_tools(self) -> Dict[str, MCPTool]:
        """Define MCP tools that wrap A2A functionality"""
        return {
            "a2a_discover": MCPTool(
                name="a2a_discover",
                description="Discover an A2A agent at a given endpoint",
                parameters={
                    "type": "object",
                    "properties": {
                        "endpoint": {
                            "type": "string",
                            "description": "The base URL of the A2A agent"
                        }
                    },
                    "required": ["endpoint"]
                }
            ),
            "a2a_list_agents": MCPTool(
                name="a2a_list_agents",
                description="List all discovered A2A agents",
                parameters={
                    "type": "object",
                    "properties": {}
                }
            ),
            "a2a_send": MCPTool(
                name="a2a_send",
                description="Send a message to a discovered A2A agent",
                parameters={
                    "type": "object",
                    "properties": {
                        "agent_name": {
                            "type": "string",
                            "description": "Name of the discovered agent"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message to send"
                        }
                    },
                    "required": ["agent_name", "message"]
                }
            )
        }
        
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Process MCP tool calls and route to A2A operations"""
        
        if tool_name == "a2a_discover":
            agent = await self.a2a_bridge.discover_agent(arguments["endpoint"])
            if agent:
                return {
                    "success": True,
                    "agent": asdict(agent),
                    "message": f"Discovered agent: {agent.name}"
                }
            return {"success": False, "message": "Failed to discover agent"}
            
        elif tool_name == "a2a_list_agents":
            agents = [asdict(a) for a in self.a2a_bridge.discovered_agents.values()]
            return {
                "success": True,
                "agents": agents,
                "count": len(agents)
            }
            
        elif tool_name == "a2a_send":
            # Convert simple string message to A2A message format
            message = A2AMessage(
                role="user",
                parts=[{"kind": "text", "text": arguments["message"]}]
            )
            
            result = await self.a2a_bridge.send_message(
                arguments["agent_name"],
                message
            )
            
            return {
                "success": "error" not in result,
                "response": result
            }
            
        else:
            return {"error": f"Unknown tool: {tool_name}"}
            
    async def start(self, host: str = "localhost", port: int = 3000):
        """Start the MCP server"""
        await self.a2a_bridge.initialize()
        
        # This is where you'd implement the actual MCP protocol
        # For now, we'll create a simple HTTP endpoint for testing
        from aiohttp import web
        
        async def handle_mcp_request(request):
            """Simple HTTP handler for MCP-style requests"""
            data = await request.json()
            
            if data.get("method") == "tools/list":
                return web.json_response({
                    "tools": [asdict(t) for t in self.tools.values()]
                })
                
            elif data.get("method") == "tools/call":
                tool_name = data.get("params", {}).get("name")
                arguments = data.get("params", {}).get("arguments", {})
                result = await self.handle_tool_call(tool_name, arguments)
                return web.json_response(result)
                
            return web.json_response({"error": "Unknown method"})
            
        app = web.Application()
        app.router.add_post('/mcp', handle_mcp_request)
        
        self.logger.info(f"MCP-A2A Bridge starting on {host}:{port}")
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        # Keep running
        await asyncio.Event().wait()
        
    async def cleanup(self):
        await self.a2a_bridge.cleanup()

async def main():
    logging.basicConfig(level=logging.INFO)
    server = MCPServer()
    
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
