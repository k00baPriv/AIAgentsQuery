# AIAgentsQuery

A sophisticated multi-agent system that provides comprehensive answers about Salesforce Data Cloud by orchestrating multiple specialized AI agents and integrating with a Model Context Protocol (MCP) server for rule-based knowledge retrieval.

## Overview

AIAgentsQuery is an intelligent query system that combines web search, knowledge base search, AI knowledge, and security analysis to provide comprehensive answers about Salesforce Data Cloud. The system uses a multi-agent architecture where specialized agents work together to gather, synthesize, and analyze information from multiple sources.

## Architecture

The system consists of several key components:

### 1. Multi-Agent Orchestration System
- **Orchestrator Agent**: Coordinates all other agents and synthesizes information
- **Web Search Agent**: Searches the web for current Salesforce Data Cloud information
- **File Search Agent**: Searches through vectorized knowledge base
- **LLM Agent**: Provides built-in AI knowledge about Data Cloud
- **Security Agent**: Analyzes security implications and compliance requirements

### 2. MCP Server Integration
- **MCP Server**: Provides access to rule-based knowledge from `data_cloud_rules/` folder
- **Rule Categories**: Security, Data Modeling, Ingestion, Connected Apps, Segmentation

### 3. Knowledge Base
- Vectorized documentation and resources
- Rule-based knowledge files organized by category

## System Interactions

### Main Application Flow

```mermaid
sequenceDiagram
    participant User
    participant Main as Main Application
    participant Orchestrator as Orchestrator Agent
    participant WebAgent as Web Search Agent
    participant FileAgent as File Search Agent
    participant LLMAgent as LLM Agent
    participant MCPServer as MCP Server
    participant SecurityAgent as Security Agent

    User->>Main: Ask question about Data Cloud
    Main->>Orchestrator: Forward user question
    
    par Orchestrator coordinates parallel searches
        Orchestrator->>WebAgent: Search web for current info
        WebAgent-->>Orchestrator: Web search results
        
        Orchestrator->>FileAgent: Search knowledge base
        FileAgent-->>Orchestrator: File search results
        
        Orchestrator->>LLMAgent: Get AI knowledge
        LLMAgent-->>Orchestrator: AI knowledge results
    end
    
    Orchestrator->>Orchestrator: Synthesize all information
    Orchestrator-->>Main: Comprehensive response
    Main->>User: Display initial response
    
    Main->>MCPServer: Initialize MCP server
    MCPServer-->>Main: Server ready
    
    Main->>SecurityAgent: Analyze content for security
    SecurityAgent->>MCPServer: Get relevant security rules
    MCPServer-->>SecurityAgent: Security rules
    SecurityAgent->>SecurityAgent: Analyze security implications
    SecurityAgent-->>Main: Security analysis results
    Main->>User: Display security analysis
```

### Agent Interaction Details

```mermaid
sequenceDiagram
    participant Orchestrator as Orchestrator Agent
    participant WebAgent as Web Search Agent
    participant FileAgent as File Search Agent
    participant LLMAgent as LLM Agent
    participant VectorStore as Vector Store
    participant Web as Web Search

    Note over Orchestrator: Orchestrator receives user question
    
    par Parallel Information Gathering
        Orchestrator->>WebAgent: search_the_web()
        WebAgent->>Web: Search for Data Cloud info
        Web-->>WebAgent: Search results
        WebAgent-->>Orchestrator: [WEB SEARCH] Results
        
        Orchestrator->>FileAgent: search_the_files()
        FileAgent->>VectorStore: Vector search
        VectorStore-->>FileAgent: Relevant documents
        FileAgent-->>Orchestrator: [KNOWLEDGE BASE] Results
        
        Orchestrator->>LLMAgent: search_LLM()
        LLMAgent-->>Orchestrator: [AI KNOWLEDGE] Results
    end
    
    Note over Orchestrator: Information synthesis and attribution
    Orchestrator->>Orchestrator: Combine and format response
```

### MCP Server and Security Analysis

```mermaid
sequenceDiagram
    participant Main as Main Application
    participant MCPServer as MCP Server
    participant SecurityAgent as Security Agent
    participant RulesFolder as data_cloud_rules/
    participant User as User

    Main->>MCPServer: Initialize MCP server
    MCPServer-->>Main: Server ready with tools
    
    Main->>SecurityAgent: Analyze orchestrator content
    SecurityAgent->>MCPServer: get_rules() - list categories
    MCPServer->>RulesFolder: Scan for rule files
    RulesFolder-->>MCPServer: Available categories
    MCPServer-->>SecurityAgent: Available rule categories
    
    SecurityAgent->>MCPServer: get_rules("security")
    MCPServer->>RulesFolder: Read security_rules.txt
    RulesFolder-->>MCPServer: Security rules content
    MCPServer-->>SecurityAgent: Security rules
    
    SecurityAgent->>SecurityAgent: Analyze security implications
    SecurityAgent->>SecurityAgent: Generate recommendations
    SecurityAgent-->>Main: Security analysis with rules
    Main->>User: Display security analysis
```

### MCP Server Tool Interaction

```mermaid
sequenceDiagram
    participant Agent as Any Agent
    participant MCPServer as MCP Server
    participant FileSystem as File System
    participant RulesFolder as data_cloud_rules/

    Agent->>MCPServer: get_rules() - no parameters
    MCPServer->>FileSystem: glob("data_cloud_rules/*.txt")
    FileSystem-->>MCPServer: List of rule files
    MCPServer->>MCPServer: Extract category names
    MCPServer-->>Agent: Available categories list
    
    Agent->>MCPServer: get_rules("security")
    MCPServer->>FileSystem: Check security_rules.txt
    FileSystem-->>MCPServer: File exists
    MCPServer->>RulesFolder: Read security_rules.txt
    RulesFolder-->>MCPServer: File content
    MCPServer-->>Agent: Security rules content
    
    Agent->>MCPServer: get_rules("nonexistent")
    MCPServer->>FileSystem: Check for file
    FileSystem-->>MCPServer: File not found
    MCPServer->>MCPServer: Generate error message
    MCPServer-->>Agent: Error with suggestions
```

## Components

### 1. Orchestrator Agent
The master coordinator that:
- Manages all other agents
- Synthesizes information from multiple sources
- Provides source attribution ([WEB SEARCH], [KNOWLEDGE BASE], [AI KNOWLEDGE])
- Ensures comprehensive and accurate responses

### 2. Web Search Agent
Specialized agent for web research that:
- Searches for current Salesforce Data Cloud information
- Focuses on official documentation and reputable sources
- Prioritizes recent information (within 2 years)
- Provides source attribution

### 3. File Search Agent
Knowledge base specialist that:
- Searches through vectorized documentation
- Finds technical details and best practices
- Cites specific files and sections
- Synthesizes information from multiple documents

### 4. LLM Agent
AI knowledge provider that:
- Provides comprehensive Data Cloud information
- Explains technical concepts clearly
- Offers practical examples and use cases
- Shares best practices and recommendations

### 5. Security Agent
Security and compliance expert that:
- Analyzes content for security implications
- Identifies relevant security topics
- Provides compliance recommendations
- Integrates with MCP server for rule-based guidance

### 6. MCP Server
Model Context Protocol server that:
- Provides access to rule-based knowledge
- Manages rule categories (security, data modeling, etc.)
- Offers tool-based interface for rule retrieval
- Handles file system operations for rule access

## Rule Categories

The system includes predefined rule categories in the `data_cloud_rules/` folder:

- **Security Rules**: Data protection, access controls, compliance
- **Data Modeling Rules**: Schema design, data relationships
- **Ingestion Rules**: Data loading, transformation, validation
- **Connected App Rules**: Integration patterns, authentication
- **Segmentation Rules**: Data partitioning, performance optimization

## Setup and Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   VECTOR_STORE_ID=your_vector_store_id
   ```

3. **Run the Application**:
   ```bash
   python agent_chain.py
   ```

## Testing the MCP Server

You can test your MCP server independently using the MCP CLI development tools:

```bash
mcp dev mcp_server.py
```

This command will start the MCP server in development mode, allowing you to:
- Test the `get_rules` tool directly
- Verify rule file access and parsing
- Debug any issues with the MCP server implementation
- See detailed logs of tool invocations

### Installing uv (if needed)

The `mcp` command-line tool may require `uv` for optimal performance. To install `uv`:

**On macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip:**
```bash
pip install uv
```

After installation, you may need to restart your terminal or add `uv` to your PATH. The `uv` tool provides faster Python package management and is recommended for MCP development workflows.

## Usage

1. Start the application
2. Enter your question about Salesforce Data Cloud
3. The system will:
   - Search multiple sources in parallel
   - Synthesize comprehensive information
   - Provide source attribution
   - Analyze security implications
   - Display both general and security-focused responses

## Key Features

- **Multi-Source Information Gathering**: Combines web search, knowledge base, and AI knowledge
- **Source Attribution**: Clearly marks information sources
- **Security Analysis**: Automatic security implications analysis
- **Rule-Based Knowledge**: Integration with MCP server for structured rules
- **Parallel Processing**: Efficient concurrent information gathering
- **Comprehensive Coverage**: Addresses technical, security, and compliance aspects

## Technical Stack

- **Python**: Core application language
- **OpenAI Agents**: Multi-agent orchestration framework
- **MCP (Model Context Protocol)**: Tool integration and rule management
- **Vector Store**: Knowledge base search capabilities
- **Web Search**: Real-time information retrieval
- **Environment Management**: dotenv for configuration

## Architecture Benefits

- **Modularity**: Each agent has a specific, well-defined role
- **Scalability**: Easy to add new agents or modify existing ones
- **Reliability**: Multiple information sources ensure comprehensive coverage
- **Security**: Dedicated security analysis with rule-based guidance
- **Maintainability**: Clear separation of concerns and well-structured code
