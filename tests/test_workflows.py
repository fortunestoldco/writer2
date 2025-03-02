import unittest
from unittest.mock import patch, MagicMock
from workflows import (
    create_initialization_graph,
    create_development_graph,
    create_creation_graph,
    create_refinement_graph,
    create_finalization_graph
)
from agents import AgentFactory
from mongodb import MongoDBManager

class TestWorkflows(unittest.TestCase):

    @patch('mongodb.MongoClient')
    def setUp(self, MockMongoClient):
        self.mock_client = MockMongoClient.return_value
        self.mock_db = self.mock_client[MONGODB_CONFIG["database_name"]]
        self.mongo_manager = MongoDBManager()
        self.agent_factory = AgentFactory(self.mongo_manager)
        self.project_id = "test_project"

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

if __name__ == '__main__':
    unittest.main()
