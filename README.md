# 🧩 Team Productivity Reporting Platform (Prototype)

[![Live Demo](https://img.shields.io/badge/Visit%20Live%20Site-Vercel-black?style=for-the-badge&logo=vercel)](https://team-productivity-reporting-platfor.vercel.app)

> 🌐 **Live Website**: [https://team-productivity-reporting-platfor.vercel.app](https://team-productivity-reporting-platfor.vercel.app)

![Dashboard Screenshot](<img width="947" alt="image" src="https://github.com/user-attachments/assets/1dd8b5aa-d9f8-4d59-8641-7e6eb7dd2f04" />

![Screenshot 2025-06-25 175347](https://github.com/user-attachments/assets/383dccad-d8db-4e31-b33b-3dc2faf35274)

)



This is a **prototype** of the Team Productivity Reporting Platform, developed as part of the **Godspeed Remote Internship Program**.

The platform provides a dashboard for visualizing key sprint metrics like **Sprint Velocity** and **Mean Time to Resolve (MTTR)** across different development teams. It also supports **natural language queries** for retrieving data using **LangChain’s Text-to-SQL** capabilities.

---

## 🚀 Features (Prototype)

✅ Implemented:

- Dashboard for metric visualization by team and sprint
- Filter options:
  - Team selection
  - Sprint selection
  - Metric toggle: Velocity / MTTR
- Interactive bar chart using `recharts`
- Responsive UI with **TailwindCSS + Shadcn UI**
- Backend powered by **Django + PostgreSQL**
- CSV-based dummy data import (teams, sprints, issues)
- REST API endpoints:
  - `GET /API/v2/teams`
  - `GET /API/v2/sprints`
  - `GET /API/v2/metrics/{team}/{sprint}`
- 🔍 **Text-to-SQL natural language querying** using **LangChain + Hugging Face LLM**

🚫 Not included in prototype (planned but not yet implemented):

- PDF export of dashboard
- User authentication / access control
- Sprint/issue creation/editing via frontend

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/soham1334/Team-Productivity-Reporting-Platform.git
cd Team-Productivity-Reporting-Platform
```

### 2. Backend Setup (Django)

```bash
cd Backend
python -m venv venv
.env\Scriptsctivate       # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddummydata
python manage.py runserver
```

Backend API: http://127.0.0.1:8000/API/v2/

### 3. Frontend Setup (React)

```bash
cd frontend/teamproductivity
npm install
npm run dev
```

Frontend: http://localhost:5173/

---

## 🧠 LangChain Text-to-SQL (Implemented)

Users can ask questions like:

- What is the average velocity of Team Alpha?
- List sprints with MTTR greater than 5
- Show all metrics for Sprint 3

LangChain uses `SQLDatabaseChain` to convert natural language into SQL and query the PostgreSQL DB.

### How to Use:

- Open chatbot interface
- Type query in plain English
- Backend responds with accurate metrics

---

## 🔁 Improvements and Next Steps

### 🧠 1. Enhanced Text-to-SQL with Better LLMs

- Replace the current model with advanced LLMs like **OpenAI GPT-4**, **Anthropic Claude**, or **Cohere Command R+**.
- These models improve SQL accuracy, especially for multi-table joins and schema understanding.

### 🎯 2. Few-shot Prompting

- Include example question-answer pairs (few-shot learning) in the prompt for more consistent SQL generation.

```
Q: Show all sprints for Team Alpha
A: SELECT * FROM sprint WHERE team_id = (SELECT id FROM team WHERE name='Alpha');
```

### ⚙️ 3. SQL Optimization and Security

- Sanitize generated SQL queries to prevent injection attacks.
- Add support for query timeouts, caching, and error handling for invalid queries.

### 🖨️ 4. Add PDF Export (Planned)

- Use `html2canvas` and `jsPDF` to allow exporting dashboard visuals.
- Fix Tailwind’s `oklch()` color issue to prevent html2canvas crashes.

### 🔐 5. User Authentication

- Implement login system and **role-based access control** (e.g., developer, manager, admin).
- Protect sensitive API endpoints and LLM query routes.

### 🌐 6. Deployment Plan

- **Backend**: Deploy via Render or Railway (PostgreSQL + Django).
- **Frontend**: Deploy via Vercel or Netlify (Vite + React).
- Use `.env` for API keys, DB configs, and model endpoints in production.

---

## 📂 Project Structure

```
Team-Productivity-Reporting-Platform/
├── Backend/
│   ├── goldspeed/
│   └── teamproductivity/
├── frontend/teamproductivity/
```

## 📎 API Endpoints

| Method | URL                             | Description             |
| ------ | ------------------------------- | ----------------------- |
| GET    | /API/v2/teams                   | List all teams          |
| GET    | /API/v2/sprints                 | List all sprints        |
| GET    | /API/v2/metrics/{team}/{sprint} | Metrics for team/sprint |

---
