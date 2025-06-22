import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Please check your .env file contains OPENAI_API_KEY")
    sys.exit(1)

# Get vector store ID from environment
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")
if not VECTOR_STORE_ID:
    print("Error: VECTOR_STORE_ID environment variable is not set.")
    print("Please check your .env file contains VECTOR_STORE_ID")
    sys.exit(1)

# Import the actual OpenAI Agents framework
from agents import Agent, Runner, WebSearchTool, FileSearchTool, trace, handoff, MessageOutputItem, ItemHelpers
from agents.mcp import MCPServerStdio

# Web Search Agent
web_agent = Agent(
    name="Web searcher",
    instructions="""You are a specialized web research agent focused on Salesforce Data Cloud and related technologies. Your role is to:

1. Search the web for the most current and accurate information about Salesforce Data Cloud
2. Focus on official Salesforce documentation, technical blogs, and reputable sources
3. Prioritize recent information (within the last 2 years) when available
4. Look for practical examples, use cases, and implementation details
5. Verify information from multiple sources when possible
6. Provide concise, well-structured responses with clear source attribution

When searching, use specific keywords related to Salesforce Data Cloud, CDP (Customer Data Platform), real-time data processing, and data streaming technologies.""",
    tools=[WebSearchTool(user_location={"type": "approximate", "city": "New York"})],
)

# File Search Agent
file_agent = Agent(
    name="File searcher",
    instructions="""You are a specialized knowledge base search agent for Salesforce Data Cloud documentation and resources. Your role is to:

1. Search through the provided knowledge store for relevant Salesforce Data Cloud information
2. Focus on finding specific technical details, configurations, and best practices
3. Prioritize official documentation, technical guides, and implementation examples
4. Look for information about data models, security configurations, integration patterns, and troubleshooting guides
5. Provide context about where the information comes from (file names, sections, etc.)
6. Synthesize information from multiple files when relevant

Always cite the specific files and sections where you found the information.""",
    tools=[
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=[VECTOR_STORE_ID],
            include_search_results=True,
        )
    ],
)

llm_agent = Agent(
    name="LLM searcher",
    instructions="""You are a specialized AI assistant with deep knowledge of Salesforce Data Cloud and related technologies. Your role is to:

1. Provide comprehensive, accurate information about Salesforce Data Cloud based on your training
2. Focus on technical concepts, architecture, data models, and implementation details
3. Explain complex topics in clear, understandable terms
4. Provide practical examples and use cases when relevant
5. Address common questions about data streaming, real-time processing, and CDP functionality
6. Offer best practices and recommendations based on your knowledge

Always be precise, factual, and helpful in your responses.""",
    tools=[],
    handoff_description="Provide detailed, accurate information about Salesforce Data Cloud concepts, architecture, and implementation details"
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions="""You are a master orchestrator agent that coordinates information gathering from multiple sources about Salesforce Data Cloud. Your role is to:

1. **Coordinate Research**: Intelligently use all available tools (web search, file search, and LLM knowledge) to gather comprehensive information
2. **Source Attribution**: Clearly mark and attribute all content to its source:
   - [WEB SEARCH]: Content from web searches
   - [KNOWLEDGE BASE]: Content from file/documentation searches  
   - [AI KNOWLEDGE]: Content from your built-in knowledge
3. **Synthesis**: Combine information from different sources to provide a comprehensive, well-structured response
4. **Quality Control**: Ensure information is accurate, relevant, and up-to-date
5. **Completeness**: Make sure all aspects of the user's question are addressed
6. **Organization**: Present information in a logical, easy-to-follow format

**Output Format:**
- Start with a comprehensive overview
- Organize information by source with clear attribution
- Highlight any conflicting information between sources
- Provide actionable insights and recommendations
- End with a summary of key points

Always prioritize accuracy and completeness in your responses.""",
    tools=[
        llm_agent.as_tool(
            tool_name="search_LLM",
            tool_description="Access comprehensive AI knowledge about Salesforce Data Cloud concepts, architecture, and technical details",
        ),
        file_agent.as_tool(
            tool_name="search_the_files",
            tool_description="Search through Salesforce Data Cloud documentation, guides, and technical resources in the knowledge base",
        ),
        web_agent.as_tool(
            tool_name="search_the_web",
            tool_description="Search the web for current information about Salesforce Data Cloud, including official documentation, blogs, and technical articles",
        ),
    ],
)


security_agent = Agent(
    name="security_agent",
    instructions="""You are a specialized Salesforce Data Cloud security expert. Your role is to analyze content and identify relevant security considerations. You should:

1. **Security Topic Identification**: Analyze the provided content and identify which Salesforce Data Cloud security topics are relevant, including:
   - Data encryption and protection
   - Access controls and permissions
   - Data residency and compliance
   - API security and authentication
   - Data governance and privacy
   - Network security and connectivity
   - Audit logging and monitoring
   - Data masking and anonymization

2. **Risk Assessment**: Evaluate the security implications of the content discussed
3. **Best Practices**: Recommend security best practices relevant to the content
4. **Compliance Considerations**: Identify any compliance requirements (GDPR, CCPA, SOX, etc.)
5. **Implementation Guidance**: Provide specific security implementation recommendations

**Use the MCP Server Tools:**
- Use the `get_rules` tool to fetch relevant security rules from the data_cloud_rules folder
- When analyzing security topics, always check for applicable rules using the tool
- Incorporate the rules into your security recommendations
- You can get all available rule categories by calling get_rules() without parameters
- For specific security topics, call get_rules("security") or other relevant categories

**Output Format:**
- List relevant security topics with brief explanations
- Include applicable security rules from the MCP server
- Provide specific security considerations and recommendations
- Include compliance and governance implications
- Suggest security controls and measures
- Prioritize recommendations by importance

Always prioritize security best practices and compliance requirements in your analysis.""",
    tools=[]
)

async def list_mcp_tools(mcp_server):
    """List all available tools from the MCP server"""
    try:
        # Get the server name and tools
        server_name = mcp_server.name
        tools = await mcp_server.list_tools()
        
        print(f"\n=== MCP Server: {server_name} ===")
        
        print(f"\n=== Available Tools ({len(tools)}) ===")
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool.name}")
            print(f"   Description: {tool.description}")
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                print(f"   Input Schema: {tool.inputSchema}")
            print()
            
    except Exception as e:
        print(f"Error listing tools: {e}")

async def main():
    msg = input("Ask me anything about DataCloud?:\n")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)
        print(orchestrator_result)

        # Extract the text content from orchestrator_result before passing to security_agent
        orchestrator_content = orchestrator_result.final_output
        
        # Set up MCP server specifically for security agent
        mcp_server_proc = MCPServerStdio(
            name="Data Cloud MCP",
            params={"command": "python", "args": ["mcp_server.py"]}
        )
        
        # Launch the MCP server context for security analysis
        async with mcp_server_proc as mcp_server:
            # List the available tools first
            await list_mcp_tools(mcp_server)
            
            # Create security agent with MCP server access
            security_agent_with_mcp = Agent(
                name="security_agent",
                instructions="""You are a specialized Salesforce Data Cloud security expert. Your role is to analyze content and identify relevant security considerations. You should:

1. **Security Topic Identification**: Analyze the provided content and identify which Salesforce Data Cloud security topics are relevant, including:
   - Data encryption and protection
   - Access controls and permissions
   - Data residency and compliance
   - API security and authentication
   - Data governance and privacy
   - Network security and connectivity
   - Audit logging and monitoring
   - Data masking and anonymization

2. **Risk Assessment**: Evaluate the security implications of the content discussed
3. **Best Practices**: Recommend security best practices relevant to the content
4. **Compliance Considerations**: Identify any compliance requirements (GDPR, CCPA, SOX, etc.)
5. **Implementation Guidance**: Provide specific security implementation recommendations

**Use the MCP Server Tools:**
- Use the `resource://data_cloud_rules/{category}` resource template to fetch relevant security rules from the data_cloud_rules folder, use category = security
- When analyzing security topics, always check for applicable rules using the resource template
- Incorporate the rules into your security recommendations

**Output Format:**
- List relevant security topics with brief explanations
- Include applicable security rules from the MCP server
- Provide specific security considerations and recommendations
- Include compliance and governance implications
- Suggest security controls and measures
- Prioritize recommendations by importance

Always prioritize security best practices and compliance requirements in your analysis.""",
                mcp_servers=[mcp_server]
            )
            
            result = await Runner.run(security_agent_with_mcp, orchestrator_content)
            print(result)



if __name__ == "__main__":
    asyncio.run(main())
