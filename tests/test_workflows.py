import unittest
from unittest.mock import patch, MagicMock
from workflows import (
    create_initialization_graph,
    create_development_graph,
    create_creation_graph,
    create_refinement_graph,
    create_finalization_graph,
    create_storybook_workflow,
    ModelProvider,
    StoryState
)
from langchain.schema.runnable import RunnableConfig
from agents import AgentFactory
from mongodb import MongoDBManager
from test_helpers import create_test_story_input, create_test_config
import pytest
from typing import Dict, Any

@pytest.fixture
def test_input() -> Dict[str, Any]:
    return {
        "title": "Test Story",
        "manuscript": "Test content",
        "model_provider": "anthropic",
        "model_name": "claude-3-opus-20240229"
    }

@pytest.fixture
def agent_factory(mongodb_manager):
    return AgentFactory(mongodb_manager)

@pytest.fixture
def config(agent_factory):
    return {"metadata": {"agent_factory": agent_factory}}

class TestWorkflows(unittest.TestCase):

    def setUp(self):
        """Set up test cases."""
        self.test_input = create_test_story_input()
        self.config = create_test_config()

    def test_create_initialization_graph(self):
        graph = create_initialization_graph(self.project_id, self.agent_factory)
        self.assertIsNotNone(graph)
        self.assertEqual(graph.entry_point, "executive_director")
        self.assertIn("executive_director", graph.nodes)
        self.assertIn("human_feedback_manager", graph.nodes)
        self.assertIn("quality_assessment_director", graph.nodes)
        self.assertIn("project_timeline_manager", graph.nodes)
        self.assertIn("market_alignment_director", graph.nodes)

    def test_create_development_graph(self):
        graph = create_development_graph(self.project_id, self.agent_factory)
        self.assertIsNotNone(graph)
        self.assertEqual(graph.entry_point, "executive_director")
        self.assertIn("executive_director", graph.nodes)
        self.assertIn("creative_director", graph.nodes)
        self.assertIn("structure_architect", graph.nodes)
        self.assertIn("plot_development_specialist", graph.nodes)
        self.assertIn("world_building_expert", graph.nodes)
        self.assertIn("character_psychology_specialist", graph.nodes)
        self.assertIn("character_voice_designer", graph.nodes)
        self.assertIn("character_relationship_mapper", graph.nodes)
        self.assertIn("domain_knowledge_specialist", graph.nodes)
        self.assertIn("cultural_authenticity_expert", graph.nodes)
        self.assertIn("market_alignment_director", graph.nodes)

    def test_create_creation_graph(self):
        graph = create_creation_graph(self.project_id, self.agent_factory)
        self.assertIsNotNone(graph)
        self.assertEqual(graph.entry_point, "executive_director")
        self.assertIn("executive_director", graph.nodes)
        self.assertIn("content_development_director", graph.nodes)
        self.assertIn("creative_director", graph.nodes)
        self.assertIn("chapter_drafters", graph.nodes)
        self.assertIn("scene_construction_specialists", graph.nodes)
        self.assertIn("dialogue_crafters", graph.nodes)
        self.assertIn("continuity_manager", graph.nodes)
        self.assertIn("voice_consistency_monitor", graph.nodes)
        self.assertIn("emotional_arc_designer", graph.nodes)
        self.assertIn("domain_knowledge_specialist", graph.nodes)

    def test_create_refinement_graph(self):
        graph = create_refinement_graph(self.project_id, self.agent_factory)
        self.assertIsNotNone(graph)
        self.assertEqual(graph.entry_point, "executive_director")
        self.assertIn("executive_director", graph.nodes)
        self.assertIn("editorial_director", graph.nodes)
        self.assertIn("creative_director", graph.nodes)
        self.assertIn("market_alignment_director", graph.nodes)
        self.assertIn("structural_editor", graph.nodes)
        self.assertIn("character_arc_evaluator", graph.nodes)
        self.assertIn("thematic_coherence_analyst", graph.nodes)
        self.assertIn("prose_enhancement_specialist", graph.nodes)
        self.assertIn("dialogue_refinement_expert", graph.nodes)
        self.assertIn("rhythm_cadence_optimizer", graph.nodes)
        self.assertIn("grammar_consistency_checker", graph.nodes)
        self.assertIn("fact_verification_specialist", graph.nodes)

    def test_create_finalization_graph(self):
        graph = create_finalization_graph(self.project_id, self.agent_factory)
        self.assertIsNotNone(graph)
        self.assertEqual(graph.entry_point, "executive_director")
        self.assertIn("executive_director", graph.nodes)
        self.assertIn("editorial_director", graph.nodes)
        self.assertIn("market_alignment_director", graph.nodes)
        self.assertIn("positioning_specialist", graph.nodes)
        self.assertIn("title_blurb_optimizer", graph.nodes)
        self.assertIn("differentiation_strategist", graph.nodes)
        self.assertIn("formatting_standards_expert", graph.nodes)

    def test_initialization_graph(self):
        """Test initialization phase workflow."""
        graph = create_initialization_graph(self.config)
        result = graph.invoke(self.test_input)
        
        # Verify state management
        self.assertEqual(result["title"], self.test_input["title"])
        self.assertEqual(result["model_provider"], ModelProvider.ANTHROPIC)
        self.assertIn("feedback", result)
        
        # Verify agent execution order
        self.assertIn("executive_director", result["phase_history"])
        self.assertIn("human_feedback_manager", result["phase_history"])
        self.assertIn("quality_assessment_director", result["phase_history"])

    def test_storybook_workflow(self):
        """Test the complete storybook workflow."""
        workflow = create_storybook_workflow(self.config)
        result = workflow.invoke(self.test_input)
        
        # Verify workflow completion
        self.assertEqual(result["title"], self.test_input["title"])
        self.assertEqual(result["model_provider"], self.test_input["model_provider"])
        self.assertIn("feedback", result)
        
        # Verify phase completion
        self.assertIn("initialization_complete", result)
        self.assertIn("development_complete", result)
        self.assertIn("creation_complete", result)
        self.assertIn("refinement_complete", result)
        self.assertIn("finalization_complete", result)
        
        # Verify quality metrics
        self.assertIn("quality_score", result)
        self.assertGreaterEqual(result["quality_score"], 0.0)
        self.assertLessEqual(result["quality_score"], 1.0)

    def test_storybook_workflow_registration(self):
        """Test that the storybook workflow is properly registered."""
        workflow = create_storybook_workflow(self.config)
        self.assertIsNotNone(workflow)
        self.assertTrue(hasattr(workflow, 'invoke'))
        
        # Test workflow invocation
        result = workflow.invoke(self.test_input)
        self.assertEqual(result["title"], self.test_input["title"])
        self.assertEqual(result["model_provider"], self.test_input["model_provider"])

def test_initialization_graph(test_input, config):
    """Test initialization phase workflow."""
    graph = create_initialization_graph(config)
    result = graph.invoke(test_input)
    
    assert result["title"] == test_input["title"]
    assert "feedback" in result
    assert "executive_director" in result["phase_history"]

def test_storybook_workflow(test_input, config):
    """Test the complete storybook workflow."""
    workflow = create_storybook_workflow(config)
    result = workflow.invoke(test_input)
    
    assert result["title"] == test_input["title"]
    assert result["model_provider"] == test_input["model_provider"]
    assert "feedback" in result
    
    # Verify phase completion
    assert "initialization_complete" in result
    assert "development_complete" in result
    assert "creation_complete" in result
    assert "refinement_complete" in result
    assert "finalization_complete" in result
    
    # Verify quality metrics
    assert "quality_score" in result
    assert 0.0 <= result["quality_score"] <= 1.0

def test_workflow_graph_structure(config):
    """Test the structure of workflow graphs."""
    init_graph = create_initialization_graph(config)
    dev_graph = create_development_graph(config)
    create_graph = create_creation_graph(config)
    refine_graph = create_refinement_graph(config)
    final_graph = create_finalization_graph(config)
    
    # Test initialization graph structure
    assert "executive_director" in init_graph.nodes
    assert "human_feedback_manager" in init_graph.nodes
    assert "quality_assessment_director" in init_graph.nodes
    
    # Test development graph structure
    assert "creative_director" in dev_graph.nodes
    assert "structure_architect" in dev_graph.nodes
    assert "plot_development_specialist" in dev_graph.nodes

if __name__ == '__main__':
    pytest.main(['-v', __file__])
