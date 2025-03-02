from typing import Dict, List, Callable, Optional, Any, Annotated, TypedDict, cast, Union
import json
from enum import Enum

from langgraph.graph import StateGraph, START, END
from langchain.schema.runnable import RunnableConfig

from state import NovelSystemState
from agents import AgentFactory

# Define input, output, and overall state schemas
class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    REPLICATE = "replicate"
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"

class NovelInput(TypedDict):
    title: str
    manuscript: str
    model_provider: ModelProvider
    model_name: str  # e.g. "gpt-4", "claude-3", "mistralai/Mistral-7B-Instruct-v0.2"

class NovelOutput(TypedDict):
    title: str
    manuscript: str
    feedback: List[str]
    model_provider: ModelProvider  # Keep track of which model was used
    model_name: str

class NovelState(NovelInput, NovelOutput):
    pass

def create_initialization_graph(config: RunnableConfig) -> StateGraph:
    """Creates the initialization phase workflow graph."""
    workflow = StateGraph(
        NovelState,
        input=NovelInput,
        output=NovelOutput
    )
    
    workflow.add_node("executive_director", 
        lambda x: {
            "title": x["title"], 
            "manuscript": x["manuscript"],
            "model_provider": x["model_provider"],
            "model_name": x["model_name"],
            "feedback": []
        })
    workflow.add_node("human_feedback_manager", 
        lambda x: {"feedback": ["Initial review completed"]})
    workflow.add_node("quality_assessment_director", 
        lambda x: {"feedback": ["Quality assessed"]})
    workflow.add_node("project_timeline_manager", 
        lambda x: {"feedback": ["Timeline updated"]})
    workflow.add_node("market_alignment_director", 
        lambda x: {"feedback": ["Market aligned"]})
    
    workflow.add_edge(START, "executive_director")
    workflow.add_edge("executive_director", "human_feedback_manager")
    workflow.add_edge("human_feedback_manager", "quality_assessment_director")
    workflow.add_edge("quality_assessment_director", "project_timeline_manager")
    workflow.add_edge("project_timeline_manager", "market_alignment_director")
    workflow.add_edge("market_alignment_director", END)
    
    return workflow.compile()

def create_development_graph(config: RunnableConfig) -> StateGraph:
    """Creates the development phase workflow graph."""
    workflow = StateGraph(
        NovelState,
        input=NovelInput,
        output=NovelOutput
    )
    
    workflow.add_node("plot_developer", 
        lambda x: {"title": x["title"], "manuscript": x["manuscript"], "feedback": []})
    workflow.add_node("character_developer", 
        lambda x: {"feedback": ["Character development completed"]})
    
    workflow.add_edge(START, "plot_developer")
    workflow.add_edge("plot_developer", "character_developer")
    workflow.add_edge("character_developer", END)
    
    return workflow.compile()

def create_creation_graph(config: RunnableConfig) -> StateGraph:
    """Creates the creation phase workflow graph."""
    workflow = StateGraph(
        state_schema=NovelInput,
        input_schema=NovelInput,
        output_schema=NovelOutput
    )
    
    workflow.add_node("content_creator", 
        lambda x: {"title": x["title"], "manuscript": x["manuscript"], "feedback": []})
    workflow.add_node("draft_reviewer", 
        lambda x: {"feedback": ["Draft review completed"]})
    
    workflow.set_entry_point("content_creator")
    workflow.add_edge("content_creator", "draft_reviewer")
    workflow.add_edge("draft_reviewer", END)
    
    return workflow

def create_refinement_graph(config: RunnableConfig) -> StateGraph:
    """Creates the refinement phase workflow graph."""
    workflow = StateGraph(
        state_schema=NovelInput,
        input_schema=NovelInput,
        output_schema=NovelOutput
    )
    
    workflow.add_node("editor", 
        lambda x: {"title": x["title"], "manuscript": x["manuscript"], "feedback": []})
    workflow.add_node("proofreader", 
        lambda x: {"feedback": ["Proofreading completed"]})
    
    workflow.set_entry_point("editor")
    workflow.add_edge("editor", "proofreader")
    workflow.add_edge("proofreader", END)
    
    return workflow

def create_finalization_graph(config: RunnableConfig) -> StateGraph:
    """Creates the finalization phase workflow graph."""
    workflow = StateGraph(
        state_schema=NovelInput,
        input_schema=NovelInput,
        output_schema=NovelOutput
    )
    
    workflow.add_node("finalizer", 
        lambda x: {"title": x["title"], "manuscript": x["manuscript"], "feedback": []})
    workflow.add_node("quality_checker", 
        lambda x: {"feedback": ["Final quality check completed"]})
    
    workflow.set_entry_point("finalizer")
    workflow.add_edge("finalizer", "quality_checker")
    workflow.add_edge("quality_checker", END)
    
    return workflow

def get_phase_workflow(phase: str, project_id: str, agent_factory: AgentFactory) -> StateGraph:
    """Get the workflow graph for a specific phase."""
    workflow_map = {
        "initialization": create_initialization_graph,
        "development": create_development_graph,
        "creation": create_creation_graph,
        "refinement": create_refinement_graph,
        "finalization": create_finalization_graph,
    }
    
    if phase not in workflow_map:
        raise ValueError(f"Unknown phase: {phase}")
    
    config = RunnableConfig(
        callbacks=None,
        tags=[f"project_{project_id}"],
        metadata={"project_id": project_id}
    )
    
    return workflow_map[phase](config)
