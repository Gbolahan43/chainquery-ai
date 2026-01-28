# ChainQuery AI 🧠⛓️

> **"Don't memorize schemas. Just ask."**  
> Natural Language Interface for Solana Blockchain Data

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev)

ChainQuery AI is an intelligent SQL query generator that transforms natural language questions into optimized **DuneSQL (Trino)** queries for the **Solana blockchain**. No more memorizing complex table schemas—just ask your question in plain English.

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

### 3. Database Setup

```bash
# Start PostgreSQL (using Docker)
docker-compose up -d

# Run migrations
alembic upgrade head
```

### 4. Start Backend Server

```bash
uvicorn app.main:app --reload
# API will run on http://127.0.0.1:8000
# Docs available at http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend will run on http://localhost:5173
```

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
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

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
