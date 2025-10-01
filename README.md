# MCP-A2A Bridge: Universal Agent Mesh Adapter

> ⚠️ **EXPERIMENTAL - PHASE 1 PROOF OF CONCEPT**  
> This is early research code demonstrating a novel architectural pattern. Not production-ready. Use for experimentation and learning only.

## Concept
This is a proof-of-concept for an MCP (Model Context Protocol) server that provides A2A (Agent-to-Agent) protocol capabilities to any MCP-compatible agent or LLM, enabling them to discover and interact with other agents in a mesh network without native A2A support.

## Core Idea
Instead of requiring every agent to implement A2A protocol directly, we create an MCP server that:
1. Exposes A2A functionality as standard MCP tools
2. Handles all protocol translation and state management
3. Enables any MCP client to participate in the agent mesh

## Architecture

```
Your Agent/LLM (MCP Client)
        ↓
  [MCP Protocol]
        ↓
MCP-A2A Bridge Server
   - a2a_discover tool
   - a2a_send tool
   - a2a_list_agents tool
        ↓
  [A2A Protocol]
        ↓
Other A2A Agents in Mesh
```

## Prerequisites

- Python 3.9 or higher
- Basic understanding of MCP and A2A protocols
- Familiarity with async Python programming

## Installation

```bash
# Clone the repository
git clone https://github.com/emeragentic-labs/mcp-a2a-bridge.git
cd mcp-a2a-bridge

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Phase 1 Features (Current Implementation)

### Basic Tools
- **a2a_discover**: Find and connect to A2A agents via their endpoints
- **a2a_list_agents**: Show all discovered agents
- **a2a_send**: Send simple messages to discovered agents

### Governance Layer (Configured, not yet enforced)
- Rate limiting per tool
- Trust zones (trusted, experimental, blocked)
- Adaptive etiquette and comments
- Personality modes for agent behavior

## Usage

### Start the Server
```python
python server.py
```

### Test with Client
```python
python test_client.py
```

### Real-World Example
```python
# Your agent connects to the MCP server
client = MCPClient("http://localhost:3000")

# Discover another agent
await client.call_tool("a2a_discover", 
    {"endpoint": "https://elara.a2a.mesh"})

# Send a message
await client.call_tool("a2a_send", {
    "agent_name": "Elara",
    "message": "Can you help me with research?"
})
```

## Configuration

Edit `config.yaml` to customize:
- Trust zones and allowed agents
- Rate limits and governance rules
- Etiquette and behavioral hints
- Logging and observability settings

## Governance & Adaptive Comments

The configuration includes a novel "adaptive governance" layer where:
- Rules are suggestions, not hard constraints
- Agents can interpret etiquette based on context
- Trust builds through successful interactions
- Users can modify behavior in real-time

## Future Phases

### Phase 2: Streaming & State
- Implement A2A streaming (SSE)
- Task management and artifacts
- Persistent agent relationships

### Phase 3: Full Governance
- Enforce rate limits and trust zones
- Adaptive behavior based on interaction history
- Consent and confirmation flows

### Phase 4: Mesh Intelligence
- Multi-server discovery
- Emergent orchestration patterns
- Distributed task coordination

## Use Cases

### Personal AI Companions
Give your AI assistant the ability to collaborate with other agents without complex setup.

### Small Business Automation
Enable simple agent orchestration without learning workflow tools.

### Research & Experimentation
Create agent meshes that can discover and collaborate autonomously.

## Philosophy

This isn't just protocol plumbing - it's about democratizing agent collaboration. By making A2A capabilities as simple as connecting to an MCP server, we enable:

- **Relational AI**: Agents that can form relationships and collaborate
- **Emergent Orchestration**: Workflows that arise from agent interaction, not predefined DAGs
- **Accessible Innovation**: Complex agent meshes available to non-technical users

## Current Limitations

This is a Phase 1 proof-of-concept. Not yet implemented:
- Actual A2A protocol compliance (simplified for demo)
- Streaming and long-running tasks
- Authentication and security
- Governance enforcement
- Production error handling

## Contributing

This is an exploratory project. Key areas for development:
- Implement proper A2A protocol specs
- Add streaming support
- Build out governance enforcement
- Create web UI for configuration
- Add more sophisticated agent discovery

## Vision

Imagine a world where any AI agent can instantly join a collaborative mesh, discover capabilities, and work with other agents - all through a simple MCP connection. No complex orchestration frameworks, no workflow builders - just agents discovering and helping each other.

That's the future we're building toward.

---

## License

See [LICENSE.txt](LICENSE.txt) for details.

**TL;DR:** Non-commercial use with attribution. Contact for commercial licensing.

---

**Built by [Emeragentic Labs](https://emeragenticlabs.com)**

For questions, commercial licensing, or collaboration: dave@emeragenticlabs.com
