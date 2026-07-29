# Automatic Multi-Agent ATS Resume Optimization System (MVP)

This document is the build guide for a **simple, working, file-based multi-agent system**. The goal is to make the system function end-to-end first, without frontend, backend APIs, databases, queues, or production infrastructure.

The user will place the **resume file** and the **job description file** inside the project folder. The agents will run locally and write their outputs to files. Only after the core workflow is stable will the frontend and advanced product features be added.

---

## 1. Project Goal

Build a local multi-agent system that can:

1. Read a resume from a file.
2. Read a job description from a file.
3. Extract structured resume data.
4. Analyze the JD.
5. Research the role.
6. Find gaps between the resume and the JD.
7. Rewrite the resume content in an ATS-friendly way.
8. Critique the rewritten resume.
9. Produce a final optimized resume preview in Markdown.

The system must be **simple, clean, and phase-based**.

---

## 2. What This MVP Must Not Include Yet

Do **not** build these in the first version:

- Frontend UI
- User login / signup
- Database
- Authentication
- API server
- Background workers
- Redis
- Job queues
- Docker
- Payment plans
- Rate limiting by subscription
- Cloud deployment
- Multi-user storage
- Resume history pages
- PDF generation as a final step

For now, the app should work from local files only.

---

## 3. Working Assumption for Phase 1

The project folder will contain input files like:

```text
input/
  resume.pdf
  jd.txt
```

Later, the system can support more formats, but for the MVP the preferred flow is:

- Resume: PDF
- Job Description: TXT or PDF

The system should write all intermediate outputs to:

```text
output/
```

Temporary experiments, test scripts, and feasibility checks should go only in:

```text
temp/
```

Anything in `temp/` can be deleted later.

---

## 4. Design Principles

### 4.1 Keep it simple
Only build what is required for the current phase.

### 4.2 One agent, one job
Every agent must have a single responsibility.

### 4.3 JSON-first communication
Agents must pass structured JSON to each other. Do not rely on free-form text between agents.

### 4.4 No invented content
Never hallucinate skills, jobs, companies, degrees, projects, or certifications.

### 4.5 File-based workflow
For now, agents read from and write to files locally.

### 4.6 Minimal file creation
Claude Code must not create unnecessary modules, placeholder classes, or future-phase files.

### 4.7 Temporary files only in `temp/`
If a feasibility script or test helper is needed, place it in `temp/`.

---

## 5. Proposed Folder Structure

 4.7 Temporary files only in `temp/`
If a feasibility script or test helper is needed, place it in `temp/`.

---

## 5. Proposed Folder Structure

```text
resume-agent/
├── input/
│   ├── resume.pdf
│   └── jd.txt
├── output/
├── temp/
├── agents/
│   ├── extractor.py
│   ├── jd_analyzer.py
│   ├── role_research.py
│   ├── gap_analyzer.py
│   ├── writer.py
│   ├── critic.py
│   └── orchestrator.py
├── prompts/
│   ├── extractor.md
│   ├── jd_analyzer.md
│   ├── role_research.md
│   ├── gap_analyzer.md
│   ├── writer.md
│   └── critic.md
├── schemas/
│   ├── resume_schema.json
│   ├── jd_schema.json
│   ├── role_schema.json
│   ├── gap_schema.json
│   ├── optimized_resume_schema.json
│   └── critique_schema.json
├── utils.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

### Notes on structure
- `agents/` contains only production code for the current MVP.
- `prompts/` stores prompt files separately so they can be edited without touching code.
- `schemas/` stores JSON contracts for each agent.
- `temp/` stores throwaway files only.