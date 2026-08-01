# Auto MEP - Mechanical, Electrical & Plumbing Engineering Portal

An AI-powered MEP engineering platform that automates load calculations, generates professional reports, and provides intelligent analysis for HVAC and building services engineering projects.

---

## Project Overview

Auto MEP is a full-stack web application designed to streamline MEP engineering workflows. It enables engineers to upload room data spreadsheets, automatically perform engineering calculations (cooling loads, lighting, equipment, fresh air), and generate comprehensive AI-powered analysis reports.

The platform combines traditional engineering calculations with modern AI/LLM capabilities to produce detailed, professional MEP reports in both web and PDF formats.

---

## Key Features

### Core Functionality
- **Automated Engineering Analysis** — Upload Excel/CSV files with room data and get instant calculations for total cooling loads (TR), lighting density, equipment density, fresh air requirements, and occupancy analysis
- **AI-Powered Report Generation** — Leverages LLM models (OpenAI, Google, Groq) to generate professional MEP engineering summaries from raw calculation data
- **PDF Export** — Download analysis results and AI-generated reports as professionally formatted PDF documents with project-specific naming
- **Report Caching** — Analysis and report results are cached in the database to avoid redundant LLM calls and improve performance

### Project Management
- **Project CRUD** — Create, read, update, and delete engineering projects
- **File Management** — Upload and manage Excel (.xlsx) and CSV files per project
- **User Authentication** — JWT-based authentication with role-based access control (admin, manager, user)

### Monitoring & Operations
- **Application Logs** — Built-in HTML log viewer at `/logs` with filtering by level (DEBUG/INFO/WARNING/ERROR) and text search
- **Activity Logging** — All major operations (auth, projects, files, analysis) are logged for audit and debugging

---

## Architecture

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.14 + FastAPI |
| **Database** | SQLite (via SQLAlchemy ORM) |
| **Authentication** | JWT (PyJWT + bcrypt via passlib) |
| **AI/LLM** | OpenAI API, Google Gemini, Groq |
| **PDF Generation** | PyMuPDF (fitz) |
| **Data Processing** | pandas + numpy |
| **Frontend (Legacy)** | Vanilla HTML/CSS/JS (SPA with hash routing) |
| **Frontend (React)** | React + React Router + Axios |

### Backend Structure

```
Auto_MEP/
├── app/
│   ├── main.py                # FastAPI app, CORS, router registration
│   ├── config/                # Settings, logger, enums
│   ├── core/
│   │   ├── security.py        # Password hashing + JWT tokens
│   │   ├── deps.py            # Auth dependencies (get_current_user, RoleChecker)
│   │   ├── EDA/               # Engineering Data Analysis
│   │   │   ├── analyzer.py    # DataAnalyzer — calculations + caching
│   │   │   ├── summery.py     # ReportGenerator — LLM reports + caching
│   │   │   └── prompt/        # Prompt templates for LLM
│   │   ├── file/              # PDF generation + file utilities
│   │   └── llm/               # LLM abstraction layer
│   │       ├── call_handler.py    # Unified model caller
│   │       ├── families/          # OpenAI, Google, Groq adapters
│   │       └── models_registry.json
│   ├── db/                    # SQLite database setup
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic request/response schemas
│   ├── routes/                # API endpoint modules
│   ├── services/              # Business logic layer
│   └── logs/                  # Runtime log files
├── automep.db                 # SQLite database file
└── requirements.txt
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get current authenticated user |
| POST | `/projects` | Create a new project |
| GET | `/projects` | List all projects for current user |
| GET | `/projects/id/{id}` | Get project by ID with files |
| GET | `/projects/name/{name}` | Get project by name |
| PUT | `/projects/{id}` | Update a project |
| DELETE | `/projects/{id}` | Delete a project |
| POST | `/projects/{id}/files` | Upload a file to a project |
| DELETE | `/projects/{id}/files?file_id=` | Delete a file |
| GET | `/analysis/{file_id}` | Run engineering analysis on a file |
| GET | `/analysis/{file_id}/download` | Download analysis as PDF |
| GET | `/analysis/generate_report/{file_id}` | Generate AI report |
| GET | `/analysis/generate_report/{file_id}/download` | Download report as PDF |
| GET | `/logs` | HTML log viewer |
| GET | `/logs/data` | Logs as JSON (filterable) |

---

## Engineering Calculations

The `DataAnalyzer` processes room-level data and computes:

| Metric | Description |
|--------|-------------|
| Total Area (m²) | Sum of all room areas |
| Average Room Area (m²) | Mean room area |
| Total Occupancy | Sum of all room occupancies |
| Total Lighting (W) | Sum of lighting loads |
| Lighting Density (W/m²) | Lighting load per unit area |
| Total Equipment (W) | Sum of equipment loads |
| Equipment Density (W/m²) | Equipment load per unit area |
| Total Fresh Air (CFM) | Sum of ventilation requirements |
| Fresh Air per Person | Ventilation rate per occupant |
| Estimated Total Load (W) | Lighting + Equipment + (Area × 120 W/m²) |
| Estimated Tons of Refrigeration | Total load ÷ 3517 W/TR |

---

## Getting Started

### Prerequisites
- Python 3.14+
- pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Auto_MEP

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your API keys and settings

# Run the application
python -m uvicorn app.main:app --reload --port 8000
```

### Quick Start (Windows)

```bash
# Run from the MAAP root folder
run_maap.bat
```

This starts:
- Backend API on `http://localhost:8000`
- SPA Frontend on `http://localhost:5500`

### Frontend Access

- **React Frontend**: `http://localhost:3000` (if running CRA dev server)
- **Vanilla SPA**: `http://localhost:5500` (via `web/server.py`)
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Log Viewer**: `http://localhost:8000/logs`

---

## Environment Variables

```env
# Application
APP_NAME=Auto MEP
APP_VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM API Keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
GROQ_API_KEY=gsk_...

# LLM Models
COOLING_REPORT_MODEL=gpt-4o-mini
```

---

## Project Root Structure

```
MAAP/
├── Auto_MEP/           # Backend (FastAPI)
│   ├── app/            # Application code
│   ├── automep.db      # Database
│   └── requirements.txt
├── web/                # Vanilla SPA Frontend
│   ├── index.html
│   ├── server.py       # Python SPA server (port 5500)
│   ├── js/             # JavaScript modules
│   └── css/            # Stylesheets
├── frontend/           # React Frontend (CRA)
│   ├── src/
│   └── package.json
├── run_maap.bat        # One-click startup script
├── install.bat         # Environment setup script
└── Auto MEP.lnk        # Desktop shortcut
```

---

## License

Private — MAAP (Mega AI Agent Project)
