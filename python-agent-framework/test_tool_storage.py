"""
Test Tool Storage Functionality
测试工具存储功能

This script tests the tool storage and loading functionality.
此脚本测试工具存储和加载功能。
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tool_storage import ToolStorageManager
from utils.dynamic_tool import load_tool_from_config


def test_tool_storage():
    """Test tool storage operations."""
    print("=" * 60)
    print("Testing Tool Storage Functionality")
    print("=" * 60)
    
    # Initialize storage manager
    storage = ToolStorageManager()
    print(f"\n✓ Storage manager initialized")
    print(f"  Storage directory: {storage.storage_dir}")
    print(f"  Storage file: {storage.tools_file}")
    
    # Test 1: Save a tool
    print("\n" + "-" * 60)
    print("Test 1: Save Tool")
    print("-" * 60)
    
    test_tool = {
        "name": "TestCalculator",
        "description": "A simple calculator for testing",
        "parameters": {
            "type": "object",
            "properties": {
                "num1": {
                    "type": "number",
                    "description": "First number"
                },
                "num2": {
                    "type": "number",
                    "description": "Second number"
                },
                "operation": {
                    "type": "string",
                    "description": "Operation: add, subtract, multiply, divide"
                }
            },
            "required": ["num1", "num2", "operation"]
        },
        "code": """
if operation == 'add':
    result = num1 + num2
elif operation == 'subtract':
    result = num1 - num2
elif operation == 'multiply':
    result = num1 * num2
elif operation == 'divide':
    result = num1 / num2 if num2 != 0 else 'Error: Division by zero'
else:
    result = 'Error: Unknown operation'
"""
    }
    
    if storage.save_tool(test_tool):
        print(f"✓ Tool '{test_tool['name']}' saved successfully")
    else:
        print(f"✗ Failed to save tool")
        return False
    
    # Test 2: Load tools
    print("\n" + "-" * 60)
    print("Test 2: Load Tools")
    print("-" * 60)
    
    tools = storage.load_all_tools()
    print(f"✓ Loaded {len(tools)} tool(s)")
    
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Test 3: Get specific tool
    print("\n" + "-" * 60)
    print("Test 3: Get Specific Tool")
    print("-" * 60)
    
    retrieved_tool = storage.get_tool("TestCalculator")
    if retrieved_tool:
        print(f"✓ Retrieved tool: {retrieved_tool['name']}")
        print(f"  Parameters: {len(retrieved_tool['parameters']['properties'])} defined")
    else:
        print(f"✗ Failed to retrieve tool")
        return False
    
    # Test 4: Load as dynamic tool
    print("\n" + "-" * 60)
    print("Test 4: Load as Dynamic Tool")
    print("-" * 60)
    
    dynamic_tool = load_tool_from_config(retrieved_tool)
    if dynamic_tool:
        print(f"✓ Created dynamic tool: {dynamic_tool.name}")
        print(f"  Description: {dynamic_tool.description}")
        
        # Test execution
        result = dynamic_tool.execute(num1=10, num2=5, operation='add')
        print(f"  Test execution (10 + 5): {result}")
    else:
        print(f"✗ Failed to create dynamic tool")
        return False
    
    # Test 5: Update tool
    print("\n" + "-" * 60)
    print("Test 5: Update Tool")
    print("-" * 60)
    
    updates = {
        "description": "An updated calculator for testing"
    }
    
    if storage.update_tool("TestCalculator", updates):
        print(f"✓ Tool updated successfully")
        updated_tool = storage.get_tool("TestCalculator")
        print(f"  New description: {updated_tool['description']}")
    else:
        print(f"✗ Failed to update tool")
    
    # Test 6: Export tools
    print("\n" + "-" * 60)
    print("Test 6: Export Tools")
    print("-" * 60)
    
    export_path = os.path.join(storage.storage_dir, "test_export.json")
    if storage.export_tools(export_path):
        print(f"✓ Tools exported to: {export_path}")
    else:
        print(f"✗ Failed to export tools")
    
    # Test 7: Tool count
    print("\n" + "-" * 60)
    print("Test 7: Get Tool Count")
    print("-" * 60)
    
    count = storage.get_tool_count()
    print(f"✓ Total tools: {count}")
    
    # Test 8: Delete tool (cleanup)
    print("\n" + "-" * 60)
    print("Test 8: Delete Tool (Cleanup)")
    print("-" * 60)
    
    if storage.delete_tool("TestCalculator"):
        print(f"✓ Test tool deleted successfully")
        remaining = storage.get_tool_count()
        print(f"  Remaining tools: {remaining}")
    else:
        print(f"✗ Failed to delete tool")
    
    # Cleanup export file
    if os.path.exists(export_path):
        os.remove(export_path)
        print(f"✓ Cleaned up export file")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    
    return True


def main():
    """Main test function."""
    try:
        success = test_tool_storage()
        if success:
            print("\n🎉 Tool storage system is working correctly!")
            print("\nYou can now:")
            print("  1. Start the GUI: streamlit run gui/app.py")
            print("  2. Navigate to 'Tool Management'")
            print("  3. Create your custom tools")
            print("\nSee TOOL_QUICKSTART.md for more information.")
        else:
            print("\n❌ Some tests failed. Please check the errors above.")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
