from setuptools import setup, find_packages

setup(
    name="writer2",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.11",
        "langchain_core>=0.1.0",
        "langchain_anthropic>=0.3.8",
        "langchain_aws>=0.2.14",
        "langchain_mongodb>=0.5.0",
        "langchain_openai>=0.3.7",
        "langchain_ollama>=0.0.1",
        "langgraph>=0.0.20",
        "httpx>=0.26.0",
        "Pyjnius",
        # ...other dependencies...
    ],
    python_requires=">=3.10",
)
