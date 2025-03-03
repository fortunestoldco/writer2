from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_anthropic import ChatAnthropic
import structlog

logger = structlog.get_logger(__name__)

class HumanFeedbackManager:
    """Agent responsible for managing and incorporating human feedback."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        self.llm = ChatAnthropic(model=model_name)
        self.output_parser = JsonOutputParser()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are the Human Feedback Manager.
            Review the current story state and executive direction.
            Provide specific questions and areas where human input would be valuable.
            Format your response as JSON with:
            {
                "feedback_requests": ["Specific questions for human review"],
                "critical_areas": ["Areas needing human attention"],
                "suggested_revisions": ["Proposed changes"],
                "confidence": 0.0
            }"""),
            ("human", "{input}")
        ])

    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process state and generate feedback requests."""
        try:
            input_text = f"""
            Vision: {state.get('vision')}
            Outline: {state.get('outline')}
            Themes: {state.get('themes')}
            Quality Metrics: {state.get('quality_metrics')}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                "feedback_requests": result["feedback_requests"],
                "critical_areas": result["critical_areas"],
                "suggested_revisions": result["suggested_revisions"],
                "human_feedback_confidence": result["confidence"]
            })
            
            logger.info(
                "human_feedback_complete",
                title=state.get('title'),
                confidence=result["confidence"]
            )
            
            return state
            
        except Exception as e:
            logger.error("human_feedback_error", error=str(e))
            raise