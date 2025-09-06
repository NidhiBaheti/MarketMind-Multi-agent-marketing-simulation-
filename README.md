# MarketMind - Multi-Agent Marketing Simulation

A sophisticated multi-agent system that simulates marketing dynamics and consumer behavior through intelligent agent interactions. This project combines artificial intelligence, behavioral modeling, and marketing strategy simulation to create realistic market scenarios.

## 📋 Features

- **Multi-Agent Architecture**: Simulate complex interactions between brand agents and consumer agents
- **Marketing Campaign Management**: Create, manage, and analyze marketing campaigns through an intuitive UI
- **Behavioral Modeling**: Advanced consumer behavior simulation based on psychological and economic principles
- **Real-time Analytics**: Monitor agent interactions and campaign performance in real-time
- **Modular Design**: Extensible architecture supporting custom agent behaviors and market scenarios
- **Data-driven Insights**: Comprehensive data collection and analysis for marketing strategy optimization

## 🏗️ Project Structure

```
MarketMind-Multi-agent-marketing-simulation-/
├── agents/              # Agent implementations and behaviors
├── campaign-ui/         # React-based campaign management interface
├── data/               # Data models, storage, and analytics
├── interface/          # API interfaces and communication protocols
├── llm/               # Language model integrations and AI components
├── simulation/        # Core simulation engine and market dynamics
├── .gitignore         # Git ignore configuration
├── README.md          # Project documentation (this file)
├── package.json       # Node.js dependencies
├── requirements.txt   # Python dependencies
├── test_run_brandagent.py     # Brand agent testing script
└── test_run_consumeragent.py  # Consumer agent testing script
```

### Directory Overview

- **`agents/`**: Contains the core agent implementations including brand agents, consumer agents, and their behavioral models
- **`campaign-ui/`**: Web-based user interface built with React for creating and managing marketing campaigns
- **`data/`**: Data management components, database models, and analytics tools
- **`interface/`**: API definitions and communication interfaces between different system components
- **`llm/`**: Integration with large language models for natural language processing and agent intelligence
- **`simulation/`**: Market simulation engine, environment setup, and scenario management

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Python Dependencies

1. Create a virtual environment:
```bash
python -m venv marketmind-env
source marketmind-env/bin/activate  # On Windows: marketmind-env\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Node.js Dependencies

1. Navigate to the campaign-ui directory:
```bash
cd campaign-ui
```

2. Install Node.js dependencies:
```bash
npm install
# or
yarn install
```

## 💻 Usage

### Running the Simulation

1. Start the core simulation engine:
```bash
python simulation/main.py
```

2. Test individual agents:
```bash
# Test brand agent
python test_run_brandagent.py

# Test consumer agent
python test_run_consumeragent.py
```

### Campaign Management UI

1. Navigate to the campaign-ui directory:
```bash
cd campaign-ui
```

2. Start the development server:
```bash
npm start
# or
yarn start
```

3. Open your browser and navigate to `http://localhost:3000`

### API Interface

The system provides RESTful APIs for:
- Agent management and configuration
- Campaign creation and monitoring
- Data analytics and reporting
- Real-time simulation control

Refer to the `interface/` directory for detailed API documentation.

## 🔧 Configuration

Configuration files and environment variables can be found in:
- `simulation/config/` - Simulation parameters
- `campaign-ui/src/config/` - UI configuration
- `.env` files for environment-specific settings

## 🎯 Key Components

### Agent System
- **Brand Agents**: Represent marketing entities with strategic decision-making capabilities
- **Consumer Agents**: Model individual consumer behavior and preferences
- **Market Environment**: Simulates market conditions and external factors

### Simulation Engine
- Multi-threaded simulation processing
- Real-time event handling
- Scalable agent interaction management

### Analytics Dashboard
- Campaign performance metrics
- Agent behavior analysis
- Market trend visualization

## 🛠️ Development

### Languages and Technologies
- **Python**: Core simulation engine, agent logic, and backend services
- **JavaScript/React**: Frontend campaign management interface
- **APIs**: RESTful services for system integration
- **Data Storage**: JSON, CSV, and database integration support

### Modular Architecture
The project is designed with modularity in mind:
- Each directory represents a distinct functional area
- Clear separation between simulation logic and user interface
- Extensible agent framework for custom implementations
- Plugin architecture for additional features

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow coding standards** for both Python and JavaScript
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/NidhiBaheti/MarketMind-Multi-agent-marketing-simulation-.git
cd MarketMind-Multi-agent-marketing-simulation-
```

2. Follow installation instructions above
3. Create a new branch for your feature
4. Make changes and test thoroughly
5. Submit a pull request

### Code Style
- Python: Follow PEP 8 guidelines
- JavaScript: Use ESLint configuration provided
- Use meaningful variable names and comments
- Maintain consistent indentation

## 📊 Testing

Run the test suite:

```bash
# Python tests
python -m pytest

# JavaScript tests
cd campaign-ui
npm test
```

## 📝 Documentation

- API documentation: `interface/docs/`
- Agent behavior guides: `agents/docs/`
- Simulation configuration: `simulation/docs/`

## 🎯 Roadmap

- [ ] Advanced machine learning integration
- [ ] Enhanced visualization capabilities
- [ ] Mobile-responsive campaign interface
- [ ] Multi-market simulation support
- [ ] Real-time collaboration features

## 📄 License

This project is licensed under [LICENSE_TYPE]. See the LICENSE file for details.

---

**MarketMind** - Revolutionizing marketing strategy through intelligent simulation and multi-agent systems.
