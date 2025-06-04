from setuptools import find_packages, setup

setup(
    name="omeka_s_mcp_sample",
    version="0.1.0",
    description="MCP server for Omeka S API integration",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.6.0",
        "mcp-server>=0.1.0",
        "anthropic>=0.52.1",
        "python-dotenv>=1.1.0",
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.10",
)
