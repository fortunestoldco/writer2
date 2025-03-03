from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from graphviz import Digraph
from typing import Dict
from dependencies import get_agent_factory

router = APIRouter(prefix="/visualize", tags=["visualization"])

@router.get("/workflow/{project_id}")
async def visualize_workflow(
    project_id: str,
    agent_factory = Depends(get_agent_factory)
) -> HTMLResponse:
    """Generate a visual representation of the workflow"""
    try:
        dot = Digraph(comment='Story Workflow')
        dot.attr(rankdir='LR')
        
        # Add phases
        phases = ["initialization", "development", "creation", "refinement", "finalization"]
        for phase in phases:
            dot.node(phase, phase.title())
        
        # Add edges
        for i in range(len(phases)-1):
            dot.edge(phases[i], phases[i+1])
        
        return HTMLResponse(dot.pipe().decode('utf-8'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))