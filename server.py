from typing import Dict, List, Optional, Any
import os
import json
from dotenv import load_dotenv

from langgraph.server import Server
from langgraph.runtime import RuntimeEnvironment
from langgraph.graph import StateGraph

from agents import AgentFactory
from mongodb import MongoDBManager
from state import NovelSystemState
from workflows import get_phase_workflow
from config import SERVER_CONFIG

# Load environment variables
load_dotenv()

# Initialize MongoDB and agent factory
mongo_manager = MongoDBManager()
agent_factory = AgentFactory(mongo_manager)

# Define graph configurations as strings (not dict)
GRAPH_CONFIGS = [
    "workflows:create_initialization_graph",
    "workflows:create_development_graph",
    "workflows:create_creation_graph",
    "workflows:create_refinement_graph",
    "workflows:create_finalization_graph"
]

# Initialize server with string configuration
server = Server(
    graphs_config=",".join(GRAPH_CONFIGS),
    runtime=RuntimeEnvironment(
        python_dependencies=[
            "langchain-anthropic",
            "langchain-openai",
            "langchain-mongodb",
            "langgraph"
        ]
    )
)

# Register graphs as endpoints
@server.register("/initialize/{project_id}")
def get_initialization_graph(project_id: str) -> StateGraph:
    return get_phase_workflow("initialization", project_id, agent_factory)

@server.register("/develop/{project_id}")
def get_development_graph(project_id: str) -> StateGraph:
    """Get the development phase graph for a project.
    
    Args:
        project_id: ID of the project.
        
    Returns:
        The development phase graph.
    """
    return get_phase_workflow("development", project_id, agent_factory)

@server.register("/create/{project_id}")
def get_creation_graph(project_id: str) -> StateGraph:
    """Get the creation phase graph for a project.
    
    Args:
        project_id: ID of the project.
        
    Returns:
        The creation phase graph.
    """
    return get_phase_workflow("creation", project_id, agent_factory)

@server.register("/refine/{project_id}")
def get_refinement_graph(project_id: str) -> StateGraph:
    """Get the refinement phase graph for a project.
    
    Args:
        project_id: ID of the project.
        
    Returns:
        The refinement phase graph.
    """
    return get_phase_workflow("refinement", project_id, agent_factory)

@server.register("/finalize/{project_id}")
def get_finalization_graph(project_id: str) -> StateGraph:
    """Get the finalization phase graph for a project.
    
    Args:
        project_id: ID of the project.
        
    Returns:
        The finalization phase graph.
    """
    return get_phase_workflow("finalization", project_id, agent_factory)

if __name__ == "__main__":
    server.serve(
        host="0.0.0.0",
        port=8000,
        workers=1
    )
