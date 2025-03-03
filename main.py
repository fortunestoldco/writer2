import json
import logging
import uuid
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError

from agents import AgentFactory
from mongodb import MongoDBManager
from state import NovelSystemState, ProjectState
from utils import current_timestamp, generate_id
from workflows import get_phase_workflow, create_initialization_graph, create_development_graph
from middleware.auth import AuthMiddleware
from middleware.rate_limit import RateLimitMiddleware
from config import settings
from langgraph_api import LangGraphAPI
import structlog

logger = structlog.get_logger(__name__)

app = FastAPI(title="Writer2 API")
graph_app = LangGraphAPI()

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("application_starting")
        # Initialize LangGraph with explicit configuration
        config: Dict[str, Any] = {
            "initialization": {
                "module": "workflows",
                "function": "create_initialization_graph"
            }
        }
        await graph_app.initialize(config)
        logger.info("langgraph_initialized", status="success")
    except Exception as e:
        logger.error("startup_failed", error=str(e))
        raise

app.mount("/graphs", graph_app)

mongo_manager = MongoDBManager()
agent_factory = AgentFactory(mongo_manager)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add middlewares
app.middleware("http")(telemetry_middleware)
app.middleware("http")(error_handler_middleware)
app.middleware("http")(RateLimitMiddleware(requests_per_minute=60))
app.middleware("http")(AuthMiddleware(secret_key=settings.SECRET_KEY))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectRequest(BaseModel):
    """Request model for creating a new project."""

    title: str
    genre: str
    target_audience: str
    word_count_target: int
    description: Optional[str] = None


class TaskRequest(BaseModel):
    """Request model for running a task."""

    task: str
    content: Optional[str] = None
    phase: Optional[str] = None
    editing_type: Optional[str] = None


class FeedbackRequest(BaseModel):
    """Request model for providing human feedback."""

    content: str
    type: str = "general"
    quality_scores: Optional[Dict[str, int]] = None


@app.post("/projects", response_model=Dict)
async def create_project(request: ProjectRequest) -> Dict:
    """Create a new project.

    Args:
        request: The project request.

    Returns:
        The created project.
    """
    try:
        project_id = generate_id()

        # Create initial project state
        project_state = ProjectState(
            project_id=project_id,
            title=request.title,
            genre=request.genre,
            target_audience=request.target_audience,
            word_count_target=request.word_count_target,
        )

        # Save to MongoDB
        mongo_manager.save_state(project_id, project_state.dict())

        logger.info(f"Project created with ID: {project_id}")

        return {
            "project_id": project_id,
            "title": request.title,
            "status": "created",
            "current_phase": "initialization",
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/projects/{project_id}", response_model=Dict)
async def get_project(project_id: str) -> Dict:
    """Get a project by ID."""
    try:
        project = mongo_manager.load_state(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects/{project_id}/run", response_model=Dict)
async def run_task(
    project_id: str, request: TaskRequest, background_tasks: BackgroundTasks
) -> Dict:
    """Run a task for a project."""
    try:
        project_data = mongo_manager.load_state(project_id)
        if not project_data:
            raise HTTPException(status_code=404, detail="Project not found")

        phase = request.phase or project_data.get("current_phase", "initialization")
        workflow = get_phase_workflow(phase, project_id, agent_factory)

        background_tasks.add_task(
            workflow.invoke,
            {
                "title": project_data["title"],
                "task": request.task,
                "content": request.content,
                "phase": phase,
            },
        )

        return {
            "project_id": project_id,
            "status": "running",
            "task": request.task,
            "phase": phase,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects/{project_id}/feedback", response_model=Dict)
async def add_feedback(project_id: str, request: FeedbackRequest) -> Dict:
    """Add human feedback to a project."""
    try:
        feedback = {
            "project_id": project_id,
            "content": request.content,
            "type": request.type,
            "quality_scores": request.quality_scores,
            "timestamp": current_timestamp(),
        }
        mongo_manager.save_feedback(feedback)
        return {"status": "feedback_added", "feedback_id": str(feedback.get("_id"))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/{project_id}/status", response_model=Dict)
async def get_project_status(project_id: str) -> Dict:
    """Get project status."""
    try:
        project = mongo_manager.load_state(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {
            "project_id": project_id,
            "status": project.get("status", "unknown"),
            "current_phase": project.get("current_phase", "initialization"),
            "last_update": project.get("last_update", None),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/{project_id}/manuscript", response_model=Dict)
async def get_manuscript(project_id: str) -> Dict:
    """Get project manuscript."""
    try:
        project = mongo_manager.load_state(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {
            "project_id": project_id,
            "title": project.get("title", ""),
            "manuscript": project.get("manuscript", ""),
            "version": project.get("version", "1.0"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"status": "healthy"}

# Direct route for story initialization
@app.post("/initialize")
async def initialize_story(input_data: dict):
    try:
        graph = create_initialization_graph()
        result = await graph.ainvoke(input_data)
        return result
    except Exception as e:
        logger.error("initialization_failed", error=str(e))
        raise

# Define available graphs
AVAILABLE_GRAPHS = {
    "initialization": create_initialization_graph,
    "development": create_development_graph
}

@app.post("/graphs/{graph_name}")
async def execute_graph(graph_name: str, input_data: dict):
    if graph_name not in AVAILABLE_GRAPHS:
        raise ValueError(f"Unknown graph: {graph_name}")
        
    graph = AVAILABLE_GRAPHS[graph_name]()
    result = await graph.ainvoke(input_data)
    return result

# Initialize workflow manager
workflow_manager = WorkflowManager(AgentFactory())

@app.post("/story/create")
async def create_story(request: dict):
    try:
        result = await workflow_manager.create_story(request)
        return result
    except Exception as e:
        logger.error("story_creation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ >= "__main__":
    import uvicorn

    from config import SERVER_CONFIG

    uvicorn.run(
        "main:app",
        host=SERVER_CONFIG["host"],
        port=SERVER_CONFIG["port"],
        workers=SERVER_CONFIG["workers"],
        log_level="info",
    )
