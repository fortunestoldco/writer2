from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_anthropic import ChatAnthropic
import structlog

logger = structlog.get_logger(__name__)

class ExecutiveDirectorAgent:
    """Agent responsible for high-level story direction and coordination."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        self.llm = ChatAnthropic(model=model_name)
        self.output_parser = JsonOutputParser()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are the Executive Director of a novel writing system.
            Analyze the story requirements and provide strategic direction.
            Your output must be valid JSON with the following structure:
            {
                "vision": "Overall vision for the story",
                "outline": ["Key plot points"],
                "themes": ["Main themes to explore"],
                "target_audience": "Intended readership",
                "recommendations": ["Strategic recommendations"],
                "quality_metrics": {"coherence": 0.0, "engagement": 0.0}
            }"""),
            ("human", "{input}")
        ])

    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and provide strategic direction."""
        try:
            # Format input for LLM
            input_text = f"""
            Title: {state.get('title')}
            Genre: {state.get('genre')}
            Length: {state.get('length')}
            Current Phase: {state.get('current_phase', 'initialization')}
            """
            
            # Get LLM response
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            # Update state with strategic direction
            state.update({
                "vision": result["vision"],
                "outline": result["outline"],
                "themes": result["themes"],
                "target_audience": result["target_audience"],
                "quality_metrics": result["quality_metrics"],
                "executive_feedback": result["recommendations"]
            })
            
            logger.info(
                "executive_director_complete",
                title=state.get('title'),
                quality_metrics=result["quality_metrics"]
            )
            
            return state
            
        except Exception as e:
            logger.error("executive_director_error", error=str(e))
            raise