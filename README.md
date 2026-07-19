# Auto MEP 🚀

Auto MEP is a production-ready engineering platform designed to automate Mechanical, Electrical, and Plumbing (MEP) engineering workflows, including room data processing, engineering calculations, load analysis, and AI-powered report generation.

The primary objective of the system is to **reduce engineering time**, **eliminate repetitive manual tasks**, and provide a scalable foundation for AI-driven engineering automation.

---

# ⚙️ Setup & Installation

Follow these steps to set up the development environment:

```bash
# 1. Create a dedicated Conda environment
conda create -n mep python=3.11 -y

# 2. Activate the environment
conda activate mep

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the FastAPI development server
uvicorn app.main:app --reload
```

---

# 🛠️ System Features

## 1. User Authentication (JWT)

Secure authentication using JSON Web Tokens.

- **Register (`POST /auth/register`)**
  - Create a new user account.
  - Required fields:
    - Full Name
    - Email
    - Password
    - Engineering Role (Engineer, Manager, Admin)

- **Login (`POST /auth/login`)**
  - Authenticate users.
  - Generate secure JWT access tokens.

- **Current User (`GET /auth/me`)**
  - Retrieve information about the authenticated user.

---

## 2. Project Management

Manage engineering projects efficiently.

- **Create Project (`POST /projects`)**
  - Create a new engineering project.
  - Specify project name and description.

- **Get All Projects (`GET /projects`)**
  - Retrieve all projects owned by the authenticated user.

- **Get Project by ID (`GET /projects/id/{project_id}`)**
  - Retrieve complete project information.
  - Includes uploaded files associated with the project.

- **Get Project by Name (`GET /projects/name/{project_name}`)**
  - Search projects by name.

- **Update Project (`PUT /projects/{project_id}`)**
  - Modify project name or description.

- **Delete Project (`DELETE /projects/{project_id}`)**
  - Delete the project.
  - Remove all associated uploaded files.

---

## 3. File Management & Validation

Upload and manage engineering spreadsheets.

- **Upload File (`POST /projects/{project_id}/files`)**
  - Supported formats:
    - Excel (.xlsx)
    - CSV (.csv)
  - Automatic validation:
    - File type
    - Maximum file size (40 MB)
  - Files are stored inside dedicated project directories.

- **Delete File (`DELETE /projects/{project_id}/files`)**
  - Remove both:
    - Database record
    - Physical file from local storage

---

## 4. Engineering Load Analysis

Automatically analyze uploaded engineering spreadsheets.

- **Analyze File (`GET /analysis/{file_id}`)**

The analysis engine extracts engineering data from uploaded spreadsheets and calculates:

- Total conditioned area
- Average room area
- Total occupancy
- Average occupancy
- Lighting load
- Equipment load
- Lighting power density
- Equipment power density
- Fresh air requirements
- Cooling load estimation
- Cooling capacity (TR)

The calculated statistics become the input for AI-generated engineering reports.

---

## 5. AI Engineering Report Generation

Generate professional engineering reports using Large Language Models.

- **Generate Report (`GET /analysis/generate_report/{file_id}`)**

Supported LLM providers:

- OpenAI
- Google Gemini
- Groq

The AI generates consultant-level reports containing:

- Project Overview
- Occupancy Analysis
- Internal Heat Gain Analysis
- Ventilation Analysis
- Cooling Load Summary
- Engineering Remarks
- Engineering Recommendations

---

# 🎯 Project Vision

## Reduce Engineering Time

The primary goal of Auto MEP is to automate repetitive engineering workflows.

Instead of manually reading spreadsheets, calculating loads, estimating cooling capacity, and preparing engineering reports, engineers simply upload an Excel or CSV file and receive engineering calculations and professional reports within seconds.

This significantly reduces engineering effort while improving consistency and productivity.

---

## AI-Powered Engineering Platform

Auto MEP is designed as a scalable platform that supports future AI-driven engineering applications.

The architecture enables seamless integration of additional engineering modules, advanced analytical models, and intelligent automation capabilities.

Future enhancements may include:

- Advanced HVAC load calculations
- Electrical load analysis
- Plumbing system calculations
- Firefighting system design assistance
- Retrieval-Augmented Generation (RAG) for engineering standards
- AI agents for engineering workflows
- Automated feasibility studies
- Bill of Quantities (BOQ) generation
- Engineering specification analysis
- Intelligent document processing
- Multi-agent engineering assistants
- Integration with multiple LLM providers and engineering APIs

The platform serves as a flexible foundation for building next-generation AI solutions tailored to MEP engineering and consulting workflows.