from enum import Enum
from typing import (Annotated, Any, Callable, Dict, List, Optional, TypedDict,
                    Union, cast)

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langsmith import RunTree
from langsmith.run_helpers import traceable

from agents import AgentFactory
from state import NovelSystemState
import structlog

logger = structlog.get_logger(__name__)


# Define input, output, and overall state schemas
class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    REPLICATE = "replicate"
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"


class StoryInput(TypedDict):
    title: str
    manuscript: str
    model_provider: ModelProvider
    model_name: str  # e.g. "gpt-4", "claude-3", "mistralai/Mistral-7B-Instruct-v0.2"


class StoryOutput(TypedDict):
    title: str
    manuscript: str
    feedback: List[str]
    model_provider: ModelProvider  # Keep track of which model was used
    model_name: str


class StoryState(StoryInput, StoryOutput):
    pass


# Add tracing decorator to agent functions
@traceable(name="Executive Director Agent")
def executive_director_agent(state: StoryState) -> Dict:
    return {
        "title": state["title"],
        "manuscript": state["manuscript"],
        "model_provider": state["model_provider"],
        "model_name": state["model_name"],
        "feedback": [],
        "agent_type": "executive_director",
        "agent_model": state["model_name"],
    }


@traceable(name="Human Feedback Manager Agent")
def human_feedback_manager_agent(state: StoryState) -> Dict:
    return {
        "feedback": ["Initial review completed"],
        "agent_type": "human_feedback_manager",
        "agent_model": state["model_name"],
    }


from typing import Any, Dict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph

from agents import (content_creator_agent, creative_director_agent,
                    draft_reviewer_agent, editor_agent,
                    executive_director_agent, finalizer_agent,
                    human_feedback_manager_agent, market_alignment_agent,
                    proofreader_agent, quality_assessment_director_agent,
                    quality_checker_agent)
from state import StoryState


def create_initialization_graph() -> StateGraph:
    """Creates a minimal initialization graph for testing."""
    graph = StateGraph()
    
    # Add a simple pass-through node
    async def process(state: Dict[str, Any]) -> Dict[str, Any]:
        state["initialization_complete"] = True
        return state
    
    graph.add_node("init", process)
    graph.set_entry_point("init")
    graph.add_edge("init", END)
    
    return graph


def create_development_graph(config: RunnableConfig) -> StateGraph:
    """Creates the development phase workflow graph."""
    workflow = StateGraph(StoryState)

    # Add creative director node
    workflow.add_node(
        "creative_director",
        creative_director_agent,
        metadata={
            "description": "Creative vision and direction",
            "agent_type": "director",
            "team": "creative",
        },
    )

    workflow.add_edge("START", "creative_director")
    workflow.add_edge("creative_director", "END")

    return workflow.compile()


def create_creation_graph(config: RunnableConfig) -> StateGraph:
    """Creates the content creation phase workflow graph."""
    workflow = StateGraph(StoryState)

    # Add content creator node
    workflow.add_node(
        "content_creator",
        content_creator_agent,
        metadata={
            "description": "Creates story content",
            "agent_type": "creator",
            "team": "writing",
        },
    )

    # Add draft reviewer node
    workflow.add_node(
        "draft_reviewer",
        draft_reviewer_agent,
        metadata={
            "description": "Reviews draft content",
            "agent_type": "reviewer",
            "team": "quality",
        },
    )

    workflow.add_edge("START", "content_creator")
    workflow.add_edge("content_creator", "draft_reviewer")
    workflow.add_edge("draft_reviewer", "END")

    return workflow.compile()


def create_refinement_graph(config: RunnableConfig) -> StateGraph:
    """Creates the refinement phase workflow graph."""
    workflow = StateGraph(StoryState)

    # Add editor node
    workflow.add_node(
        "editor",
        editor_agent,
        metadata={
            "description": "Edits and refines content",
            "agent_type": "editor",
            "team": "editing",
        },
    )

    # Add proofreader node
    workflow.add_node(
        "proofreader",
        proofreader_agent,
        metadata={
            "description": "Performs final proofreading",
            "agent_type": "proofreader",
            "team": "editing",
        },
    )

    workflow.add_edge("START", "editor")
    workflow.add_edge("editor", "proofreader")
    workflow.add_edge("proofreader", "END")

    return workflow.compile()


def create_finalization_graph(config: RunnableConfig) -> StateGraph:
    """Creates the finalization phase workflow graph."""
    workflow = StateGraph(StoryState)

    # Add finalizer node
    workflow.add_node(
        "finalizer",
        finalizer_agent,
        metadata={
            "description": "Prepares for publication",
            "agent_type": "finalizer",
            "team": "market",
        },
    )

    # Add quality checker node
    workflow.add_node(
        "quality_checker",
        quality_checker_agent,
        metadata={
            "description": "Final quality assurance",
            "agent_type": "checker",
            "team": "quality",
        },
    )

    # Add market alignment node
    workflow.add_node(
        "market_alignment",
        market_alignment_agent,
        metadata={
            "description": "Market positioning and alignment",
            "agent_type": "analyst",
            "team": "market",
        },
    )

    workflow.add_edge("START", "finalizer")
    workflow.add_edge("finalizer", "quality_checker")
    workflow.add_edge("quality_checker", "market_alignment")
    workflow.add_edge("market_alignment", "END")

    return workflow.compile()


def get_phase_workflow(
    phase: str, project_id: str, agent_factory: AgentFactory
) -> StateGraph:
    """Get the workflow graph for a specific phase."""
    config = RunnableConfig(
        metadata={"project_id": project_id, "agent_factory": agent_factory}
    )

    workflow_map = {
        "initialization": create_initialization_graph,
        "development": create_development_graph,
        "creation": create_creation_graph,
        "refinement": create_refinement_graph,
        "finalization": create_finalization_graph,
    }

    if phase not in workflow_map:
        raise ValueError(f"Unknown phase: {phase}")

    return workflow_map[phase](config)


# Add this after your existing graph functions


def create_novel_writing_workflow(config: RunnableConfig) -> StateGraph:
    """Creates a complete novel writing workflow combining all phases."""
    workflow = StateGraph(StoryState)

    # Add each phase as a node with detailed metadata for LangSmith visualization
    phases = {
        "initialization": {
            "description": "Initial project setup and planning",
            "team": "management",
        },
        "development": {
            "description": "Story and character development",
            "team": "creative",
        },
        "creation": {"description": "Content creation and drafting", "team": "writing"},
        "refinement": {"description": "Editing and refinement", "team": "editing"},
        "finalization": {
            "description": "Final review and polishing",
            "team": "quality",
        },
    }

    # Add each phase with its metadata
    for phase_name, phase_info in phases.items():
        workflow.add_node(
            f"{phase_name}_phase",
            get_phase_workflow(
                phase_name,
                config.metadata.get("project_id", "default"),
                config.metadata.get("agent_factory"),
            ),
            metadata={
                "description": phase_info["description"],
                "team": phase_info["team"],
                "phase": phase_name,
                "project_id": config.metadata.get("project_id", "default"),
            },
        )

    # Connect phases sequentially
    workflow.add_edge(START, "initialization_phase")
    workflow.add_edge("initialization_phase", "development_phase")
    workflow.add_edge("development_phase", "creation_phase")
    workflow.add_edge("creation_phase", "refinement_phase")
    workflow.add_edge("refinement_phase", "finalization_phase")
    workflow.add_edge("finalization_phase", END)

    return workflow.compile()


def create_storybook_workflow(config: RunnableConfig) -> StateGraph:
    """Creates a complete storybook workflow combining all phases."""
    workflow = StateGraph(StoryState)

    # Define phases with their teams and descriptions
    phases = {
        "initialization": {
            "description": "Project setup and planning",
            "team": "management",
            "agents": ["executive_director", "human_feedback_manager"],
        },
        "development": {
            "description": "Story and character development",
            "team": "creative",
            "agents": ["plot_developer", "character_developer"],
        },
        "creation": {
            "description": "Content creation and drafting",
            "team": "writing",
            "agents": ["content_creator", "draft_reviewer"],
        },
        "refinement": {
            "description": "Editing and refinement",
            "team": "editing",
            "agents": ["editor", "proofreader"],
        },
        "finalization": {
            "description": "Final review and publication prep",
            "team": "quality",
            "agents": ["finalizer", "quality_checker"],
        },
    }

    # Add each phase with its metadata and agents
    for phase_name, phase_info in phases.items():
        workflow.add_node(
            f"{phase_name}_phase",
            get_phase_workflow(
                phase_name,
                config.metadata.get("project_id", "default"),
                config.metadata.get("agent_factory"),
            ),
            metadata={
                "description": phase_info["description"],
                "team": phase_info["team"],
                "phase": phase_name,
                "agents": phase_info["agents"],
                "project_id": config.metadata.get("project_id", "default"),
            },
        )

    # Create sequential flow through phases
    workflow.add_edge(START, "initialization_phase")
    workflow.add_edge("initialization_phase", "development_phase")
    workflow.add_edge("development_phase", "creation_phase")
    workflow.add_edge("creation_phase", "refinement_phase")
    workflow.add_edge("refinement_phase", "finalization_phase")
    workflow.add_edge("finalization_phase", END)

    return workflow.compile()


async def create_story(input_data: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """Main story creation workflow."""
    try:
        # Initialize workflow
        init_graph = create_initialization_graph(config)
        state = await init_graph.ainvoke(input_data)
        
        if not state.get("initialization_complete"):
            logger.error("initialization_failed", state=state)
            return {"status": "failed", "error": "Initialization failed"}
        
        # Continue with other phases...
        return {
            "status": "success",
            "title": state["title"],
            "feedback": state["feedback"],
            "quality_metrics": state["quality_metrics"]
        }
        
    except Exception as e:
        logger.error("story_creation_failed", error=str(e))
        return {"status": "error", "error": str(e)}
