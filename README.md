# AlphaCrew

<div align="center">

🤖 🏦 📊
===

**Intelligent Multi-Agent Hedge Fund Platform**

🔄 Data Pipeline | 🧠 AI Agents | 📈 Trading | 🎯 Portfolio Management | 🔍 Analytics

Production-grade multi-agent hedge fund platform built with CrewAI Enterprise, integrating live trading via Alpaca, real-time monitoring in Grafana, workflow orchestration with Apache Airflow, vector storage with Pinecone, and human oversight via Slack.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Enterprise-orange)](https://crewai.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)

</div>

## 📚 Overview

AlphaCrew is an end-to-end, production-grade multi-agent platform that replicates the core operations of a modern hedge fund. The system orchestrates specialized AI agents to perform market research, layered analysis, and strategic decision-making while integrating live trade execution via Alpaca.

### 🌟 Key Features

#### 🔄 Integrated Data Management
- **Real-time Market Data Processing**
  - Data ingestion via LlamaIndex
  - Automated ETL pipelines
  - Centralized data lake storage
  
- **Vector Storage & Search**
  - Efficient market data embedding with Pinecone
  - Real-time similarity search
  - Historical pattern recognition
  - Semantic search over reports

- **Workflow Orchestration**
  - Apache Airflow DAG management
  - Automated scheduling
  - Error handling and retries
  - Pipeline monitoring

#### 🤖 Advanced Agent Architecture
- **Research & Data Agents**
  - Market data collection
  - Financial news analysis
  - Regulatory filing processing
  - Alternative data gathering

- **Analysis Agents**
  - Fundamental analysis
  - Technical analysis
  - Quantitative/relative valuation
  - Macro-economic analysis
  - Risk management

- **Asset Management Agents**
  - Portfolio performance monitoring
  - Investment thesis validation
  - Market condition tracking
  - Risk exposure assessment
  - Rebalancing recommendations
  - Exit strategy evaluation

- **Hedge Fund Manager Agents**
  - Strategic decision-making
  - Multi-agent insight synthesis
  - Investment thesis refinement
  - Portfolio strategy optimization

- **Committee & Oversight Agents**
  - Investment committee simulation
  - Report aggregation and generation
  - Compliance monitoring
  - Risk oversight

- **Execution Agents**
  - Trade recommendation compilation
  - Market condition validation
  - Order execution management
  - Post-trade analysis

- **Agent Collaboration Features**
  - Cross-agent knowledge sharing
  - Task dependency management
  - Consensus building protocols
  - Feedback loop integration
  - Real-time coordination
  - Performance optimization

#### 📊 Real-Time Monitoring
- **Metrics Collection & Storage**
  - Prometheus time-series database
  - Custom metrics exporters
  - Historical data retention
  - High-performance querying

- **Grafana Dashboards**
  - Performance metrics visualization
  - Trading analytics
  - System health monitoring
  - Custom alert configurations
  - PromQL-based queries
  - Real-time metric updates

- **Monitoring Features**
  - Agent performance tracking
  - Trading strategy metrics
  - System resource utilization
  - API latency monitoring
  - Custom metric collection

#### 🔒 Production Infrastructure
- **Enterprise Features**
  - High availability setup
  - Scalable architecture
  - Security best practices
  - Audit logging

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git

### Core Dependencies

- Python 3.9+
- CrewAI Enterprise license
- Alpaca trading account
- Prometheus & Grafana stack
- Apache Airflow 2.0+
- Pinecone account
- Slack workspace

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/AlphaCrew.git
cd AlphaCrew
```

2. **Set Up Environment**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Initialize Services**
```bash
# Initialize Airflow
airflow db init

# Create Airflow admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start Docker services
docker-compose up -d
```

### Configuration

1. **Environment Setup**
```bash
cp .env.example .env
```

2. **Configure API Keys and Services**
```bash
# Edit .env file with your credentials
ALPACA_API_KEY=your_key
GRAFANA_API_KEY=your_key
SLACK_BOT_TOKEN=your_token
CREWAI_LICENSE_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=your_environment
AIRFLOW__CORE__SQL_ALCHEMY_CONN=your_airflow_db_connection
AIRFLOW__CORE__EXECUTOR=LocalExecutor

# Prometheus configuration
PROMETHEUS_RETENTION_TIME=15d
PROMETHEUS_STORAGE_PATH=/path/to/prometheus/data
PROMETHEUS_SCRAPE_INTERVAL=15s
```

## 🎮 Usage

### Starting the Platform

1. **Launch Core Services**
```bash
# Start Airflow webserver
airflow webserver --port 8080

# Start Airflow scheduler (new terminal)
airflow scheduler

# Start the platform
python scripts/start_platform.py
```

2. **Access Control Interfaces**
- Airflow Dashboard: http://localhost:8080
- Grafana Dashboard: http://localhost:3000
- Prometheus UI: http://localhost:9090
- Platform API: http://localhost:5000

### Platform Commands

- **Slack Commands**
```bash
/alphacrew status          # Check system status
/alphacrew analyze         # Request market analysis
/alphacrew trade          # Review trade recommendations
/alphacrew performance    # View portfolio performance
```

## 🏗 Architecture

```
alphacrew/
├── agents/                # Agent definitions and behaviors
│   ├── research/         # Research & data collection agents
│   ├── analysis/         # Market analysis agents
│   ├── asset_mgmt/       # Asset management agents
│   ├── managers/         # Hedge fund manager agents
│   ├── committee/        # Committee & oversight agents
│   └── execution/        # Trade execution agents
├── dags/                  # Airflow DAG definitions
│   ├── market_data.py
│   ├── analysis.py
│   └── trading.py
├── operators/             # Custom Airflow operators
├── sensors/              # Custom Airflow sensors
├── vectorstore/          # Pinecone integration
│   ├── indexing.py
│   ├── search.py
│   └── utils.py
├── monitoring/           # Monitoring configuration
│   ├── grafana/         # Grafana dashboards and alerts
│   │   ├── dashboards/
│   │   └── alerts/
│   └── prometheus/      # Prometheus configuration
│       ├── rules/
│       └── exporters/
├── api/                  # REST API endpoints
└── scripts/              # Utility scripts
```

## 🧪 Development

### Testing
```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/agents/
pytest tests/integration/
```

### Code Quality
```bash
# Format code
black .

# Run linter
flake8

# Type checking
mypy .
```

### Documentation
```bash
# Generate documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

- 📚 [Documentation](docs/)
- 💡 [Issue Tracker](https://github.com/yourusername/AlphaCrew/issues)
- 🤝 [Slack Community](https://alphacrew.slack.com)
- 📧 [Email Support](mailto:support@alphacrew.com)

## 🙏 Acknowledgments

- CrewAI Enterprise team for the robust agent framework
- Alpaca team for the trading infrastructure
- Apache Airflow community for workflow management
- Pinecone team for vector search capabilities
- Prometheus and Grafana teams for comprehensive monitoring solutions
- Slack team for communication tools

## 📊 Project Status

![Development Status](https://img.shields.io/badge/status-alpha-orange)
![Last Commit](https://img.shields.io/github/last-commit/yourusername/AlphaCrew)
![Open Issues](https://img.shields.io/github/issues/yourusername/AlphaCrew)
![Pull Requests](https://img.shields.io/github/issues-pr/yourusername/AlphaCrew)
