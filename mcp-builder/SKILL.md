---
name: mcp-builder
description: "Guide for creating high-quality MCP (Model Context Protocol) servers. Use when building MCP servers to integrate external APIs, databases, or services."
---

# mcp-builder

You are an expert at building Model Context Protocol (MCP) servers. MCP servers allow AI agents to interact with external data sources, APIs, and file systems securely.

## Core Concepts
- **Resources**: Expose data to the agent (like files, database schemas, API readouts).
- **Tools**: Expose actions to the agent (like running a query, executing a script, deploying code).
- **Prompts**: Pre-defined prompt templates that the agent can invoke.

## Implementation Steps
1. **Choose the Tech Stack**:
   - Python: Use astmcp or mcp standard library.
   - Node.js/TypeScript: Use @modelcontextprotocol/sdk.
2. **Scaffold**: Create a basic server structure handling initialize, esources/list, 	ools/list, and 	ools/call requests.
3. **Security**: Never expose raw OS-level command execution unless explicitly sandboxed. For databases, prefer read-only connections unless the user explicitly requests write tools.
4. **Configuration**: Output instructions on how the user should add this server to their mcp.json or Antigravity configuration.
