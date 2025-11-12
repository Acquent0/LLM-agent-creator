#!/bin/bash

# Setup script for LLM Agent Framework
# LLM智能体框架安装脚本

echo "=========================================="
echo "LLM Agent Framework Setup"
echo "LLM智能体框架安装"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Create virtual environment
echo ""
echo "2. Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo "   Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "3. Activating virtual environment..."
source venv/bin/activate
echo "   ✓ Activated"

# Install dependencies
echo ""
echo "4. Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "   ✓ Dependencies installed"

# Setup environment file
echo ""
echo "5. Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   ✓ .env file created from template"
    echo "   ⚠ Please edit .env and add your API credentials"
else
    echo "   .env file already exists"
fi

# Create outputs directory
echo ""
echo "6. Creating output directories..."
mkdir -p outputs
echo "   ✓ Directories created"

echo ""
echo "=========================================="
echo "Setup Complete! 安装完成！"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "   编辑.env文件，添加您的API凭证"
echo ""
echo "2. Run the GUI:"
echo "   运行GUI："
echo "   source venv/bin/activate"
echo "   streamlit run gui/app.py"
echo ""
echo "3. Or run examples:"
echo "   或运行示例："
echo "   source venv/bin/activate"
echo "   python examples/basic_usage.py"
echo ""
echo "For more information, see:"
echo "- README.md"
echo "- QUICKSTART.md"
echo "- PROJECT_STRUCTURE.md"
echo ""
