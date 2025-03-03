from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_anthropic import ChatAnthropic
import structlog

logger = structlog.get_logger(__name__)

class BaseAgent(ABC):
    """Base class for all story creation agents."""
    
    def __init__(
        self,
        model_name: str = "claude-3-opus-20240229",
        system_prompt: Optional[str] = None
    ):
        self.llm = ChatAnthropic(model=model_name)
        self.output_parser = JsonOutputParser()
        self.logger = structlog.get_logger(f"{__name__}.{self.__class__.__name__}")
        
        if system_prompt:
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}")
            ])
    
    @abstractmethod
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return updated state."""
        pass