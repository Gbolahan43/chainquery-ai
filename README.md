# ChainQuery AI 🧠⛓️

> **"Don't memorize schemas. Just ask."**  
> Natural Language Interface for Solana Blockchain Data

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev)
[![CI/CD](https://github.com/Gbolahan43/chainquery-ai/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Gbolahan43/chainquery-ai/actions/workflows/ci-cd.yml)
[![Deploy](https://github.com/Gbolahan43/chainquery-ai/actions/workflows/deploy.yml/badge.svg)](https://github.com/Gbolahan43/chainquery-ai/actions/workflows/deploy.yml)

ChainQuery AI is an intelligent SQL query generator that transforms natural language questions into optimized **DuneSQL (Trino)** queries for the **Solana blockchain**.

## 🎯 The Problem

Analyzing blockchain data on Solana is complex. Developers and analysts often face:
- **Steep Learning Curve**: Mastering DuneSQL (Trino) syntax takes time.
- **Complex Schemas**: Solana data tables are deeply nested and hard to navigate.
- **Time Consumption**: Writing and debugging queries manually is slow and error-prone.

## 💡 The Solution

ChainQuery AI acts as a smart bridge:
1. **Just Ask**: User types "Show me the top 10 NFT sales on Magic Eden yesterday".
2. **AI Processing**: The system understands the intent, maps it to the correct tables, and generates precise SQL.
3. **Instant Results**: Get a ready-to-run query for Dune Analytics in seconds.

## � AI Agent Architecture

ChainQuery AI functions as an autonomous **AI Agent** powered by **LangGraph**.

- **Workflow**: The system uses a stateful graph to orchestrate the "thinking" process: `Input` → `Prompt` → `LLM` → `SQL`.
- **Context**: it intelligently injects database schema and DuneSQL syntax rules into the context.
- **Details**: See [docs/AGENTS.md](docs/AGENTS.md) for a deep dive into the internal agent architecture.

---

## ✨ Features

### 🤖 AI-Powered Query Generation
- Transform natural language to SQL using advanced LLM models (GPT-4, Claude, Groq)
- Schema-aware generation with Solana table knowledge
- Optimized for DuneSQL/Trino syntax

### 🔐 Hybrid Authentication
- **Guest Access**: Try without signup using session IDs
- **User Accounts**: JWT authentication with bcrypt password hashing
- Seamless upgrade from guest to authenticated user

### 📊 Query Management
- Real-time SQL generation with streaming support
- Query history tracking (session-based for guests, account-based for users)
- Syntax highlighting with Monaco Editor

### 🎨 Modern UI
- Built with React + Vite + TypeScript
- Responsive design with Tailwind CSS
- Component library powered by shadcn/ui
- Dark mode support

---

## 🌐 Live Demo

**Try it now:** [https://chainquery-app.onrender.com](https://chainquery-app.onrender.com)

Experience ChainQuery AI in action! Generate Solana blockchain queries using natural language—no signup required (guest access available).

---

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/          # API routes and dependencies
│   │   ├── auth.py   # JWT authentication endpoints
│   │   ├── routes.py # Query generation routes
│   │   └── deps.py   # Hybrid auth dependencies
│   ├── agent/        # LangGraph agent system
│   │   ├── prompts.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   ├── core/         # Config, database, security
│   ├── models/       # SQLModel database models
│   └── schemas/      # Pydantic request/response schemas
├── alembic/          # Database migrations
└── requirements.txt
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/   # Reusable UI components
│   │   ├── auth/     # Auth-related components
│   │   └── layout/   # Layout components
│   ├── pages/        # Page components
│   │   ├── Landing.tsx
│   │   ├── Login.tsx
│   │   ├── Signup.tsx
│   │   └── Generator.tsx
│   ├── context/      # React contexts (AuthContext)
│   ├── lib/          # Utilities and API clients
│   └── hooks/        # Custom React hooks
└── package.json
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL** (via Docker or local)
- **OpenAI/Groq API Key**

### 1. Clone Repository
```bash
git clone https://github.com/Gbolahan43/chainquery-ai.git
cd chainquery-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY or GROQ_API_KEY
# - POSTGRES_* settings
```

## 🛠️ Technology Stack

### 🎨 Frontend
- **React 18**: Core framework for building the user interface.
- **Vite**: Next-generation frontend tooling for ultra-fast builds.
- **TypeScript**: Ensures type safety and developer productivity.
- **Tailwind CSS**: Utility-first CSS framework for rapid styling.
- **shadcn/ui**: High-quality, accessible component library.

### ⚙️ Backend
- **FastAPI**: Modern, high-performance web framework for Python APIs.
- **SQLModel**: ORM library combining SQL connectivity with Pydantic validation.
- **LangGraph**: Framework for building stateful, multi-actor AI agent applications.
- **Alembic**: Lightweight database migration tool.

### 🗄️ Database
- **PostgreSQL**: Robust, open-source object-relational database system.
- **DuneSQL (Trino)**: SQL dialect used for querying blockchain data.

### 🏗️ Infrastructure & DevOps
- **Docker**: Containerization for consistent environments across dev and prod.
- **GitHub Actions**: Automated CI/CD pipelines for testing and deployment.
- **Render**: Cloud platform for hosting the backend and frontend services.

### 🧬 AI & Agents
- **GPT-4 / Claude / Groq**: Advanced Large Language Models (LLMs) used for reasoning.
- **LangChain**: Framework for developing applications powered by language models.

---

## 🔑 Environment Variables

### Backend (.env)
```env
# App Config
PROJECT_NAME="ChainQuery AI"
ENVIRONMENT="dev"

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chainquery

# AI Provider (choose one)
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
GROQ_API_KEY=gsk_YOUR_KEY_HERE
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Create new account
- `POST /api/v1/auth/login` - Login with email/password

### Query Generation
- `POST /api/v1/generate` - Generate SQL from natural language (hybrid: works for guests & users)
- `GET /api/v1/history?session_id={id}` - Get query history

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest -v --cov=app --cov-report=term-missing
```

### Frontend Tests
```bash
cd frontend
npm run type-check  # TypeScript checking
npm run lint        # ESLint
npm run test        # Run tests
```

---

## 🔄 CI/CD Pipeline

ChainQuery AI uses **GitHub Actions** for automated testing and deployment.

### Workflows
- **CI/CD Pipeline**: Runs tests, linting, and Docker build on every push
- **Deployment**: Auto-deploys to Render after CI passes on `main` branch

### Status
[![CI/CD](https://github.com/Gbolahan43/chainquery-ai/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Gbolahan43/chainquery-ai/actions/workflows/ci-cd.yml)

**Documentation**: See [docs/CICD.md](docs/CICD.md) for detailed CI/CD setup and troubleshooting.

---

## 🛣️ Roadmap

- [x] **Core Features**
  - [x] Natural language to SQL conversion
  - [x] Hybrid authentication (guest + user accounts)
  - [x] Query history tracking
  - [x] Modern UI with shadcn/ui

- [ ] **Coming Soon**
  - [ ] SQL query debugging and validation
  - [ ] Multi-chain support (Ethereum, Polygon)
  - [ ] Query templates and favorites
  - [ ] Collaborative query sharing
  - [ ] Advanced analytics dashboard

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain/LangGraph** - Agent orchestration framework
- **shadcn/ui** - Beautiful React components
- **Dune Analytics** - Blockchain data platform inspiration
- **FastAPI** - Modern Python web framework

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Gbolahan43/chainquery-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Gbolahan43/chainquery-ai/discussions)

---

## 👨‍💻 Author

**Abdulbasit Gbolahan**

[![Twitter](https://img.shields.io/badge/Twitter-@0xexcellus-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://x.com/0xexcellus)
[![GitHub](https://img.shields.io/badge/GitHub-Gbolahan43-181717?style=flat&logo=github&logoColor=white)](https://github.com/Gbolahan43)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/abdulbasit-olanrewaju-gbolahan)

---

**Built with ❤️ for the Solana developer community**
