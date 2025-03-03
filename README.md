# Writer2 - AI-Powered Story Creation System

A sophisticated system leveraging AI agents to collaboratively create stories through structured workflows.

## Overview

Writer2 is a microservices-based application that orchestrates multiple specialized AI agents to create stories. Each agent handles specific aspects of the storytelling process, from world-building to character development and prose refinement.

## Architecture

### Core Components

- **Agents**: Specialized AI workers focusing on specific storytelling aspects
  - ExecutiveDirector: High-level story direction
  - CreativeDirector: Artistic vision and tone
  - WorldBuilder: Setting and environment
  - CharacterDesigner: Character development
  - PlotArchitect: Story structure
  - SceneComposer: Scene creation
  - DialogueWriter: Character conversations
  - PacingEditor: Story rhythm
  - ContinuityChecker: Consistency
  - StyleEditor: Prose quality
  - QualityAssessor: Final review

### Technology Stack

- **Backend**: FastAPI
- **AI**: LangChain with Anthropic's Claude
- **Database**: MongoDB
- **Monitoring**: Prometheus, Grafana
- **Tracing**: Jaeger
- **Logging**: Structlog

## Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/writer2.git
```

### Using Docker (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd novel-writing-system

# Start the containers
docker-compose up -d
```

### Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd novel-writing-system

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (must be running separately)
# Then start the server
python server.py
```

## API Usage

The system provides a RESTful API for interaction:

### Create a New Project
```bash
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Novel",
    "genre": "Science Fiction",
    "target_audience": "Young Adult",
    "word_count_target": 80000,
    "description": "A space adventure story"
  }'
```

### Run a Task
```bash
curl -X POST http://localhost:8000/projects/{project_id}/run \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Develop character profiles",
    "phase": "development"
  }'
```

### Add Human Feedback
```bash
curl -X POST http://localhost:8000/projects/{project_id}/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The protagonist needs a stronger motivation",
    "type": "character",
    "quality_scores": {
      "character_believability": 70,
      "plot_coherence": 85
    }
  }'
```

### Get Project Status
```bash
curl -X GET http://localhost:8000/projects/{project_id}/status
```

### Get Manuscript
```bash
curl -X GET http://localhost:8000/projects/{project_id}/manuscript
```

## Architecture Details

### Components

- **Agents**: Specialized AI components with specific roles
- **Workflows**: Phase-specific graphs defining agent interaction patterns
- **State Management**: Hierarchical state tracking at global, director, and team levels
- **MongoDB Integration**: Persistent storage for all system artifacts
- **Quality Gates**: Criteria that must be met to transition between phases

### Key Features

- **Dynamic Team Activation**: Teams are activated based on manuscript needs
- **Hierarchical Quality Control**: Quality checks at different levels
- **Enhanced Knowledge Persistence**: Specialized knowledge bases
- **Adaptive Resource Allocation**: Computation focused on high-impact areas
- **Human-in-the-Loop Integration**: Strategic placement of human touchpoints

## License

This project is licensed under the MIT License - see the LICENSE file for details.

