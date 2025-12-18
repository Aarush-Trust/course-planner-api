# Course Planner API

A backend service for building Waterloo-style course schedules with validation for term consistency and time conflicts between sections. Built with FastAPI as a learning and portfolio project.

## Overview

Course Planner API lets users:

- Browse courses, terms, and sections.
- Create schedules for a specific academic term.
- Validate that all sections in a schedule exist and belong to the same term.
- Detect time conflicts between sections (overlapping days and times).

The API is implemented using FastAPI with type-safe request/response models and auto-generated OpenAPI/Swagger documentation.

## Features

- **Courses**
  - List all courses or filter by course code.
  - Create new courses via `POST /courses`.
  - Retrieve a single course by ID with clear 404 errors when missing.

- **Terms**
  - List predefined academic terms (e.g., Winter 2026).
  - Retrieve a specific term by ID.

- **Sections**
  - List sections with day/time information and associated course + term.
  - Retrieve a section by ID.

- **Schedules**
  - Create schedules for a term from a list of section IDs.
  - Validate:
    - All section IDs exist.
    - All sections belong to the requested term.
    - No time conflicts between selected sections.
  - Check conflicts independently via `POST /schedules/check-conflicts`.

- **Error handling & docs**
  - Consistent error format:
    - `{"detail": {"code": "...", "message": "..."}}`
  - Auto-generated interactive API docs at `/docs` (Swagger UI).

## API Examples

### Health check

GET /health
Response:
{"status": "healthy", "message": "Course API is Running"}

### Courses

GET /courses
GET /courses?code=ECE 150
GET /courses/1
POST /courses

Example `POST /courses` body:
{
"code": "ECE 190",
"name": "Ethics",
"credits": 0.25
}

### Schedules

POST /schedules
Example body:
{
"term_id": 1,
"name": "Plan A",
"section_ids":​
}

If sections overlap:
{
"detail": {
"code": "TIME_CONFLICT",
"message": "Time conflicts detected between sections",
"conflicts": [
{
"section_a_id": 1,
"section_b_id": 2,
"shared_days": ["MON", "WED"]
}
]
}
}

Conflict-only check:
POST /schedules/check-conflicts
Body:
Response: list of conflict objects or `[]` if no conflicts.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Getting Started

git clone <your-repo-url>
cd course-planner-api

python -m venv .venv

Linux/macOS
source .venv/bin/activate

Windows
.venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload

Then open:
- Swagger UI: http://127.0.0.1:8000/docs  
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
