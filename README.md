# AI Task Management Chat Bot

A sophisticated task management chat interface built with Panel, integrating OpenAI's GPT-4 and SurrealDB for persistence. This implementation showcases a modern approach to AI-assisted task management with real-time chat capabilities.

## Features

- 🤖 Interactive chat interface using Panel
- 🔄 OpenAI GPT-4 integration with function calling
- 💾 SurrealDB persistence with WebSocket RPC
- 🎨 Material design theme
- 📝 Task management capabilities
- ⚡ Real-time message processing
- 🛠️ Built-in development tools

## Quick Start

1. **Set up environment**
```bash
# Clone repository
git clone https://github.com/Meh-S-Eze/openai-swarm-chat-agent
cd openai-swarm-chat-agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

2. **Start SurrealDB**
```bash
surreal start --log debug --user root --pass root file://database/data/surreal.db
```

3. **Start the backend**
```bash
python -m backend.support_bot.customer_service
```

4. **Start the frontend**
```bash
python -m frontend.run
```

Visit `http://localhost:5006` to access the chat interface.

## Architecture

- **Frontend**: Panel-based chat interface with material design
- **Backend**: Python async implementation with OpenAI integration
- **Database**: SurrealDB for persistent storage
- **State Management**: In-memory and database-backed context tracking

## Development

- Run tests: `python -m pytest`
- Format code: `black .`
- Check style: `flake8`

## Project Structure
```
.
├── backend/           # Backend services and AI integration
├── database/          # Database models and utilities
├── frontend/         # Panel-based UI components
├── .resources/       # Project documentation and schemas
└── tests/           # Test suites
```

## Credits

This project builds on several amazing technologies:

- [Panel](https://panel.holoviz.org/) - For the reactive interface
- [OpenAI](https://openai.com/) - For GPT-4 intelligence
- [SurrealDB](https://surrealdb.com/) - For data persistence
- [Python](https://www.python.org/) - Core implementation

### Development Credits

- **Original Concept & Composition**: @Meh-S-Eze (The Composer)
- **AI Assistance**: Significant contributions from Claude (Anthropic) in:
  - Architecture design
  - Integration patterns
  - Error handling
  - Documentation
  - Code quality improvements
  - Testing strategies

## License

MIT License - See LICENSE file for details

## Acknowledgments

Special thanks to:
- The Panel team for their excellent documentation
- OpenAI for their powerful API
- SurrealDB team for their innovative database
- Software Composer team for inspiration and guidance
- All contributors and maintainers of the dependencies
- Claude (Anthropic) for development assistance
- The open source community for their invaluable tools and libraries

## References

- [Senior Software Composer](https://www.youtube.com/@SeniorSWC) - Riley Brown's YouTube channel
- [Senior SWC](https://x.com/senior_swc) - Software Composer Team on X
