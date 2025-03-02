from typing import Dict, List, Optional, Any, Callable, Union
import json
import logging

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_aws import BedrockChat  # Changed from ChatBedrock to BedrockChat
from langchain_mongodb import MongoDBChatMessageHistory
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.chains import LLMChain
from langchain.schema import BaseMessage
from langchain_ollama import ChatOllama

from langgraph.graph import Graph, StateGraph, END
from langgraph.checkpoint.mongodb import MongoDBCheckpointHandler
from langgraph.prebuilt import ToolExecutor

from config import MODEL_CONFIGS, PROMPT_TEMPLATES, MONGODB_CONFIG
from state import NovelSystemState
from mongodb import MongoDBManager
from utils import create_prompt_with_context, current_timestamp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory for creating agents in the novel writing system."""
    
    def __init__(self, mongo_manager: Optional[MongoDBManager] = None):
        """Initialize the agent factory.
        
        Args:
            mongo_manager: The MongoDB manager for persistence.
        """
        self.mongo_manager = mongo_manager or MongoDBManager()
    
    def _get_llm(self, agent_name: str) -> Any:
        """Get an LLM for an agent based on its configuration.
        
        Args:
            agent_name: Name of the agent.
            
        Returns:
            An LLM instance.
        """
        try:
            config = MODEL_CONFIGS.get(agent_name, {})
            model_name = config.get("model", "")
            
            if model_name.startswith("anthropic/"):
                return ChatAnthropic(
                    model_name=model_name.replace("anthropic/", ""),
                    temperature=config.get("temperature", 0.3),
                    max_tokens=config.get("max_tokens", 2000)
                )
            elif model_name.startswith("meta-llama/") or model_name.startswith("llama-3/"):
                clean_model_name = model_name.replace("meta-llama/", "").replace("llama-3/", "")
                return BedrockChat(
                    model_id=clean_model_name,
                    model_kwargs={
                        "temperature": config.get("temperature", 0.3),
                        "max_tokens": config.get("max_tokens", 2000)
                    }
                )
            elif model_name.startswith("huggingface/"):
                if "endpoint" in model_name.lower():
                    return HuggingFaceEndpoint(
                        endpoint_url=config.get("endpoint_url"),
                        task=config.get("task", "text-generation"),
                        model_kwargs={
                            "temperature": config.get("temperature", 0.3),
                            "max_tokens": config.get("max_tokens", 2000)
                        }
                    )
                else:
                    return ChatHuggingFace(
                        model_id=model_name.replace("huggingface/", ""),
                        task=config.get("task", "text-generation"),
                        temperature=config.get("temperature", 0.3),
                        max_tokens=config.get("max_tokens", 2000)
                    )
            elif model_name.startswith("replicate/"):
                model_version = config.get("model_version", "")
                return Replicate(
                    model=f"{model_name.replace('replicate/', '')}:{model_version}",
                    model_kwargs={
                        "temperature": config.get("temperature", 0.3),
                        "max_length": config.get("max_tokens", 2000)
                    }
                )
            elif model_name.startswith("ollama/"):
                return ChatOllama(
                    model=model_name.replace("ollama/", ""),
                    temperature=config.get("temperature", 0.3),
                    repeat_penalty=config.get("repeat_penalty", 1.1),
                    base_url=OLLAMA_CONFIG["host"],
                    timeout=OLLAMA_CONFIG["timeout"]
                )
            else:
                # Default to OpenAI
                return ChatOpenAI(
                    model_name=model_name,
                    temperature=config.get("temperature", 0.3),
                    max_tokens=config.get("max_tokens", 2000)
                )
        except Exception as e:
            logger.error(f"Error getting LLM for agent {agent_name}: {e}")
            raise
    
    def _get_message_history(self, agent_name: str, project_id: str) -> MongoDBChatMessageHistory:
        """Get message history for an agent from MongoDB.
        
        Args:
            agent_name: Name of the agent.
            project_id: ID of the project.
            
        Returns:
            A MongoDBChatMessageHistory instance.
        """
        try:
            return MongoDBChatMessageHistory(
                connection_string=MONGODB_CONFIG["connection_string"],
                database_name=MONGODB_CONFIG["database_name"],
                collection_name=f"message_history_{agent_name}",
                session_id=project_id
            )
        except Exception as e:
            logger.error(f"Error getting message history for agent {agent_name}: {e}")
            raise
    
    def _get_memory(self, agent_name: str, project_id: str) -> ConversationBufferMemory:
        """Get memory for an agent.
        
        Args:
            agent_name: Name of the agent.
            project_id: ID of the project.
            
        Returns:
            A ConversationBufferMemory instance.
        """
        try:
            message_history = self._get_message_history(agent_name, project_id)
            return ConversationBufferMemory(
                memory_key="chat_history",
                chat_memory=message_history,
                return_messages=True
            )
        except Exception as e:
            logger.error(f"Error getting memory for agent {agent_name}: {e}")
            raise
    
    def _get_prompt_template(self, agent_name: str) -> PromptTemplate:
        """Get a prompt template for an agent.
        
        Args:
            agent_name: Name of the agent.
            
        Returns:
            A PromptTemplate instance.
        """
        try:
            template = PROMPT_TEMPLATES.get(agent_name, "You are an AI assistant.")
            
            # Create a ChatPromptTemplate
            system_message_prompt = SystemMessagePromptTemplate.from_template(template)
            human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
            chat_prompt = ChatPromptTemplate.from_messages([
                system_message_prompt,
                human_message_prompt
            ])
            
            return chat_prompt
        except Exception as e:
            logger.error(f"Error getting prompt template for agent {agent_name}: {e}")
            raise
    
    def create_agent(self, agent_name: str, project_id: str) -> Callable[[NovelSystemState], Dict]:
        """Create an agent function for use in the graph.
        
        Args:
            agent_name: Name of the agent.
            project_id: ID of the project.
            
        Returns:
            A callable agent function that takes NovelSystemState and returns Dict.
        """
        try:
            llm = self._get_llm(agent_name)
            memory = self._get_memory(agent_name, project_id)
            prompt = self._get_prompt_template(agent_name)
            
            chain = LLMChain(
                llm=llm,
                prompt=prompt,
                memory=memory,
                verbose=True
            )
            
            def agent_function(state: NovelSystemState) -> Dict:
                """The agent function to be used in the graph.
                
                Args:
                    state: The current state.
                    
                Returns:
                    The updated state.
                """
                try:
                    # Prepare the context
                    context = {
                        "project_state": json.dumps(state["project"], indent=2),
                        "current_phase": state["project"].current_phase,
                        "task": state["current_input"].get("task", ""),
                        "input": state["current_input"].get("content", "")
                    }
                    
                    # Run the chain
                    response = chain.run(input=json.dumps(context))
                    
                    # Update the state
                    state["current_output"] = {
                        "agent": agent_name,
                        "content": response,
                        "timestamp": current_timestamp()
                    }
                    
                    # Add to message history
                    state["messages"].append({
                        "role": agent_name,
                        "content": response,
                        "timestamp": current_timestamp()
                    })
                    
                    return state
                except Exception as e:
                    logger.error(f"Error in agent function for agent {agent_name}: {e}")
                    raise
            
            return agent_function
        except Exception as e:
            logger.error(f"Error creating agent {agent_name}: {e}")
            raise
