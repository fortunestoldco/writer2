# storybook writer. - AI-Powered Story Creation System

A sophisticated system leveraging AI agents to collaboratively create stories through structured workflows.

## Overview

storybook writer. is a microservices-based application that orchestrates multiple specialized AI agents to create stories. Each agent handles specific aspects of the storytelling process, from world-building to character development and prose refinement.

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

- **Backend**: FastAPI with async support
- **AI**: LangChain with Anthropic's Claude
- **Database**: MongoDB
- **Monitoring**: Prometheus, Grafana
- **Tracing**: Jaeger
- **Logging**: Structlog

## Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/storybook writer..git
cd storybook writer.

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

```properties
# filepath: /c:/Users/DavidJamesLennon/Documents/GitHub/storybook writer./.env
# Core Configuration
APP_ENV=development
DEBUG=true

# LangChain Configuration
LANGCHAIN_API_KEY=your-api-key-here
LANGCHAIN_PROJECT=storybook writer.

# Model Configuration
DEFAULT_MODEL=claude-3-opus-20240229

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=storybook writer.
```

## Usage

### Starting the Application

```powershell
# Start MongoDB and monitoring services
docker-compose up -d

# Start the application
uvicorn main:app --reload --port 8000
```

### Creating a Story

```powershell
# Using PowerShell
$body = @{
    title = "The Last Echo"
    genre = "science fiction"
    length = "novel"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/story/create" `
                 -Method Post `
                 -Body $body `
                 -ContentType "application/json"
```

## Development

### Running Tests

```powershell
# Install test dependencies
pip install -r test-requirements.txt

# Run tests with coverage
python -m pytest tests/ -v --cov=. --cov-report=html

# Open coverage report
start htmlcov/index.html
```

### Code Structure

```
storybook writer./
├── agents/           # AI agent implementations
├── workflows/        # Story creation workflows
├── models/          # Data models
├── routes/          # API endpoints
├── monitoring/      # Metrics and monitoring
├── tests/           # Test suite
└── tools/           # Utility functions
```

## Monitoring

### Metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Dashboard includes:
- Agent performance metrics
- Story creation success rates
- Processing times
- Error rates

### Logging
- Application logs: `logs/storybook writer..log`
- Structured JSON format
- Elasticsearch integration for search

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For support:
1. Check the documentation
2. Open an issue in the GitHub repository
3. Contact the development team

## Roadmap

- [ ] Enhanced character interaction modeling
- [ ] Genre-specific templates
- [ ] Multi-language support
- [ ] AI model fine-tuning
- [ ] Web-based story editor interface

