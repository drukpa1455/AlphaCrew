# AlphaCrew

Production-grade multi-agent hedge fund platform built with CrewAI Enterprise, integrating live trading via Interactive Brokers, real-time reporting in Airtable, and human oversight via Slack.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

## Overview

AlphaCrew is an end-to-end, production-grade multi-agent platform that replicates the core operations of a modern hedge fund. The system orchestrates specialized AI agents to perform market research, layered analysis, and strategic decision-making while integrating live trade execution via Interactive Brokers.

### Key Features

- **Integrated Data Management**
  - Real-time market data ingestion using LlamaIndex
  - Automated ETL pipelines with Apache Airflow
  - Centralized data lake storage

- **Advanced Agent Architecture**
  - Specialized research and analysis agents
  - Hedge fund manager decision-making agents
  - Risk management and compliance monitoring
  - Trade execution with human oversight

- **Real-Time Reporting & Oversight**
  - Dynamic Airtable dashboards
  - Slack integration for human supervision
  - Comprehensive investment memorandums
  - Interactive trade authorization

- **Production-Grade Infrastructure**
  - Built on CrewAI Enterprise
  - Model fine-tuning with Fireworks
  - Secure API integrations
  - Scalable deployment options

## System Requirements

- Python 3.9+
- CrewAI Enterprise license
- Interactive Brokers account
- Airtable workspace
- Slack workspace

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AlphaCrew.git
cd AlphaCrew

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Set up environment variables:
```bash
cp .env.example .env
```

2. Configure the following in your `.env` file:
```
INTERACTIVE_BROKERS_API_KEY=your_key
AIRTABLE_API_KEY=your_key
SLACK_BOT_TOKEN=your_token
CREWAI_LICENSE_KEY=your_key
```

## Usage

1. **Start the Data Pipeline**
```bash
python scripts/start_pipeline.py
```

2. **Launch Agent System**
```bash
python scripts/run_agents.py
```

3. **Monitor via Slack**
- Use `/alphacrew status` to check system status
- Review and authorize trades via Slack commands
- Request additional analysis with `/alphacrew analyze`

## Architecture

```
├── Data Ingestion
│   ├── LlamaIndex Processors
│   └── Airflow DAGs
├── Agent System
│   ├── Research Agents
│   ├── Analysis Agents
│   ├── Manager Agents
│   └── Execution Agent
└── Integration Layer
    ├── Interactive Brokers
    ├── Airtable
    └── Slack
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
# Format code
black .

# Run linter
flake8
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Open an issue
- Contact the development team via Slack
- Check our [documentation](docs/)

## Acknowledgments

- CrewAI Enterprise team
- Interactive Brokers API documentation
- Airtable and Slack developer communities
