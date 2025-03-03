from typing import Dict, List

from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain_core.agents import AgentExecutor, Tool
from langchain_core.tools import tool
from langsmith.run_helpers import traceable
from pydantic import BaseModel

from tools.refinement import (analyze_story_coherence, edit_content,
                              verify_story_elements)


@traceable(name="Editor Agent")
def editor_agent(state: StoryState) -> Dict:
    """Agent responsible for story editing and refinement."""
    tools = [
        Tool(name="edit_content", func=edit_content),
        Tool(name="analyze_story_coherence", func=analyze_story_coherence),
    ]

    agent = StructuredChatAgent.from_llm_and_tools(
        llm=get_llm_from_state(state), tools=tools
    )

    executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )

    result = executor.invoke(
        {
            "input": {
                "title": state["title"],
                "manuscript": state["manuscript"],
                "revision_depth": "detailed",
            }
        }
    )

    return {
        "edits": result.get("edits", {}),
        "coherence": result.get("coherence_analysis", {}),
        "feedback": ["Editing completed", "Story coherence improved"],
        "agent_type": "editor",
        "agent_model": state["model_name"],
    }


@traceable(name="Proofreader Agent")
def proofreader_agent(state: StoryState) -> Dict:
    """Agent responsible for final proofreading and verification."""
    tools = [
        Tool(name="verify_story_elements", func=verify_story_elements),
        Tool(name="edit_content", func=edit_content),
    ]

    agent = StructuredChatAgent.from_llm_and_tools(
        llm=get_llm_from_state(state), tools=tools
    )

    executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )

    result = executor.invoke(
        {
            "input": {
                "title": state["title"],
                "manuscript": state["manuscript"],
                "focus_areas": ["technical", "consistency"],
            }
        }
    )

    return {
        "verification": result.get("verification", {}),
        "feedback": ["Proofreading completed", "Technical issues resolved"],
        "agent_type": "proofreader",
        "agent_model": state["model_name"],
    }
