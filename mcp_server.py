# mcp_server.py
from mcp.server.fastmcp import FastMCP
import os
import glob

# Initialize the MCP server with a descriptive name
mcp = FastMCP("MCP server for Data Cloud knowledge")

def get_available_categories():
    """Get list of available rule categories from the data_cloud_rules folder"""
    rules_dir = "data_cloud_rules"
    if not os.path.exists(rules_dir):
        return []
    
    # Get all .txt files in the rules directory
    rule_files = glob.glob(os.path.join(rules_dir, "*.txt"))
    categories = []
    
    for file_path in rule_files:
        # Extract category name from filename (remove .txt and _rules)
        filename = os.path.basename(file_path)
        category = filename.replace("_rules.txt", "").replace(".txt", "")
        categories.append(category)
    
    return categories

def read_rules_file(category: str) -> str:
    """Read rules from a specific category file"""
    rules_dir = "data_cloud_rules"
    
    # Try different possible filename patterns
    possible_files = [
        f"{category}_rules.txt",
        f"{category}.txt",
        f"{category}_rules"
    ]
    
    for filename in possible_files:
        file_path = os.path.join(rules_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except Exception as e:
                return f"Error reading file {file_path}: {str(e)}"
    
    return f"No rules file found for category: {category}"

# Define a tool (capability) for fetching rules
@mcp.tool()
# def get_rules(category: str = None) -> str:
#     """Fetch rules created by Solution Architects from data_cloud_rules folder"""
#     try:
#         if category is None:
#             # Return all available categories
#             categories = get_available_categories()
#             if not categories:
#                 return "No rule categories found. Please ensure the data_cloud_rules folder exists with .txt files."
            
#             result = "Available rule categories:\n"
#             for cat in categories:
#                 result += f"- {cat}\n"
#             result += "\nUse a specific category name to get detailed rules."
#             return result
        
#         # Read rules for the specified category
#         rules_content = read_rules_file(category.lower())
#         if rules_content.startswith("No rules file found"):
#             # Try to suggest available categories
#             available_categories = get_available_categories()
#             if available_categories:
#                 suggestions = ", ".join(available_categories)
#                 return f"{rules_content}\n\nAvailable categories: {suggestions}"
#             else:
#                 return f"{rules_content}\n\nNo rule categories are currently available."
        
#         return rules_content
        
#     except Exception as e:
#         return f"Unexpected error: {str(e)}"

@mcp.resource("resource://data_cloud_rules/{category}")
def get_rules_resource(category: str) -> str:
    """Provides rules content from data_cloud_rules folder based on category."""
    try:
        # Read rules for the specified category
        rules_content = read_rules_file(category.lower())
        if rules_content.startswith("No rules file found"):
            # Try to suggest available categories
            available_categories = get_available_categories()
            if available_categories:
                suggestions = ", ".join(available_categories)
                return f"{rules_content}\n\nAvailable categories: {suggestions}"
            else:
                return f"{rules_content}\n\nNo rule categories are currently available."
        
        return rules_content
        
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Start the MCP server when this script is executed
if __name__ == "__main__":
    mcp.run()
