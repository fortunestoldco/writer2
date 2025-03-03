from setuptools import find_packages, setup

setup(
    name="writer2",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Web framework
        "fastapi>=0.115.11",
        "uvicorn>=0.24.0",
        # LangChain ecosystem
        "langchain>=0.1.0",
        "langchain_core>=0.1.0",
        "langchain_anthropic>=0.3.8",
        "langchain_aws>=0.2.14",
        "langchain_mongodb>=0.5.0",
        "langchain_openai>=0.3.7",
        "langchain_ollama>=0.0.1",
        "langgraph>=0.0.20",
        "langsmith>=0.0.30",
        # Database
        "motor>=3.3.0",
        "pymongo>=4.6.0",
        "beanie>=1.25.0",  # Added for ODM support
        # Utilities
        "httpx>=0.26.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "structlog>=24.1.0",
        "tenacity>=8.2.0",  # Added for retries
        "asyncio>=3.4.3",  # Added for async support
        # Testing
        "pytest>=8.0.0",
        "pytest-asyncio>=0.23.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.12.0",  # Added for mocking
    ],
    extras_require={
        "dev": [
            "black>=24.1.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",
            "ruff>=0.2.0",
            "pre-commit>=3.5.0",
            "sphinx>=7.2.0",  # Added for documentation
            "sphinx-rtd-theme>=2.0.0",
        ],
        "monitoring": [
            "prometheus-client>=0.19.0",
            "opentelemetry-api>=1.22.0",
            "opentelemetry-sdk>=1.22.0",
        ],
    },
    python_requires=">=3.10",
    description="An advanced novel writing system using LangChain and LangGraph",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/writer2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
