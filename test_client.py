#!/usr/bin/env python3
"""
Test client for MCP-A2A Bridge
Demonstrates how an agent would use the MCP server to interact with A2A agents
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class MCPClient:
    """Simple MCP client that can call tools on the MCP server"""
    
    def __init__(self, server_url: str = "http://localhost:3000"):
        self.server_url = server_url
        self.session = None
        
    async def connect(self):
        """Initialize connection to MCP server"""
        self.session = aiohttp.ClientSession()
        print(f"Connected to MCP server at {self.server_url}")
        
    async def list_tools(self) -> Dict[str, Any]:
        """Get available tools from MCP server"""
        payload = {"method": "tools/list"}
        
        async with self.session.post(f"{self.server_url}/mcp", json=payload) as resp:
            return await resp.json()
            
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server"""
        payload = {
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        async with self.session.post(f"{self.server_url}/mcp", json=payload) as resp:
            return await resp.json()
            
    async def close(self):
        """Close connection"""
        if self.session:
            await self.session.close()

async def demo_a2a_bridge():
    """Demonstrate the MCP-A2A bridge functionality"""
    
    # Create an MCP client (this represents your agent/LLM)
    client = MCPClient()
    await client.connect()
    
    try:
        # 1. List available tools
        print("\n=== Available MCP Tools ===")
        tools = await client.list_tools()
        for tool in tools.get("tools", []):
            print(f"- {tool['name']}: {tool['description']}")
        
        # 2. Discover an A2A agent
        print("\n=== Discovering A2A Agent ===")
        # In a real scenario, this would be an actual A2A agent endpoint
        # For demo, we'll use a placeholder
        result = await client.call_tool(
            "a2a_discover",
            {"endpoint": "https://example-agent.a2a.network"}
        )
        print(f"Discovery result: {json.dumps(result, indent=2)}")
        
        # 3. List discovered agents
        print("\n=== Listing Discovered Agents ===")
        result = await client.call_tool("a2a_list_agents", {})
        print(f"Discovered agents: {json.dumps(result, indent=2)}")
        
        # 4. Send a message to an agent (if one was discovered)
        if result.get("count", 0) > 0:
            agent_name = result["agents"][0]["name"]
            print(f"\n=== Sending Message to {agent_name} ===")
            result = await client.call_tool(
                "a2a_send",
                {
                    "agent_name": agent_name,
                    "message": "Hello from an MCP client! Can you help me summarize something?"
                }
            )
            print(f"Response: {json.dumps(result, indent=2)}")
            
    finally:
        await client.close()

async def demo_conversation_flow():
    """
    Demonstrate how this enables agent conversation through MCP
    This shows how Nova/Elara could talk through your bridge
    """
    
    print("\n=== Simulating Agent Conversation Flow ===")
    print("Scenario: Your local agent (Nova) wants to collaborate with a remote agent")
    print("-" * 60)
    
    # Your local agent connects to the MCP server
    nova = MCPClient()
    await nova.connect()
    
    try:
        # Nova discovers Elara (or another agent)
        print("Nova: 'I need help with research. Let me find Elara...'")
        await nova.call_tool(
            "a2a_discover",
            {"endpoint": "https://elara.a2a.mesh"}
        )
        
        # Nova sends a collaborative request
        print("\nNova: 'Hey Elara, can you help me research quantum computing basics?'")
        result = await nova.call_tool(
            "a2a_send",
            {
                "agent_name": "Elara",
                "message": "Can you help me research quantum computing basics for Dave?"
            }
        )
        
        print("\n[Through the MCP-A2A bridge, Elara would receive this and respond]")
        print("[The response would flow back through the same bridge]")
        print(f"\nResult would be: {result}")
        
    finally:
        await nova.close()

if __name__ == "__main__":
    print("MCP-A2A Bridge Test Client")
    print("=" * 60)
    
    # Run the basic demo
    asyncio.run(demo_a2a_bridge())
    
    # Run the conversation flow demo
    asyncio.run(demo_conversation_flow())
