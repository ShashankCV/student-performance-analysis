# Student Records API

A Python backend for managing student records with FastAPI and persistent SQLite storage. The CRUD API is split into route modules, with an optional Ollama endpoint for natural-language questions grounded in student records.

## Requirements

- Python 3.10 or newer
- pip

## Install and run

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs> for interactive Swagger documentation. The database file `students.db` is created in the project directory on first startup. To store it elsewhere, set `STUDENT_DATABASE_PATH` before starting the server.

On macOS or Linux, activate the environment with `source .venv/bin/activate` instead.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List students, with optional filters |
| `GET` | `/students/{student_id}` | Retrieve one student |
| `PATCH` | `/students/{student_id}` | Update provided fields |
| `DELETE` | `/students/{student_id}` | Delete a student |
| `GET` | `/health` | Check API status |
| `POST` | `/ai/query-students` | Ask a question about student records (optional Ollama setup) |

Each student has a generated unique ID, name, date of birth, and at least one contact field (email or phone). Course, address, and enrollment date are optional. Dates use ISO format (`YYYY-MM-DD`).

`GET /students` accepts `name` and `course` partial-match filters, `date_of_birth_after` and `date_of_birth_before` date filters, and pagination through `limit` (1-500, default 100) and `offset` (default 0). The date filters are exclusive.

### Sample requests

Create a record:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/students `
  -ContentType 'application/json' `
  -Body '{"name":"Asha Patel","date_of_birth":"2006-04-15","email":"asha@example.com","course":"Python Backend"}'
```

List students born after a date:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/students?date_of_birth_after=2005-01-01'
```

Update and delete using the `student_id` returned by create:

```powershell
Invoke-RestMethod -Method Patch -Uri http://127.0.0.1:8000/students/1 `
  -ContentType 'application/json' -Body '{"course":"Data Science"}'
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:8000/students/1
```

Missing records return `404`; invalid inputs return `422`. See `/docs` for the complete request and response schemas.

### Optional Ollama AI

Install and start Ollama, then download the default model:

```powershell
ollama pull llama3.2:1b
```

Install the optional Python integration:

```powershell
python -m pip install -r requirements-ai.txt
```

The API uses `OLLAMA_MODEL` (default `llama3.2:1b`) and optionally `OLLAMA_BASE_URL` to configure Ollama. Set either variable in the environment before starting the server if you need a different model or host. The AI endpoint uses a fixed, read-only query and sends student IDs, names, dates of birth, courses, and enrollment dates to the model; it does not send email, phone, or address fields and never lets the model execute SQL. Use fictional student data for demonstrations.

Try the endpoint in `/docs` with:

```json
{"question":"How many students are there?"}
```

The response contains the original question and the model's answer. If the optional package is not installed, the endpoint returns `503`; the CRUD API remains available.

The project is organized as `app/config.py`, `app/database.py`, `app/models.py`, `app/schemas.py`, and `app/routes/` for the individual endpoints. `main.py` exposes the FastAPI app for Uvicorn.

## Tests

```powershell
python -m pytest
```

The tests use a temporary database and do not modify the application database. Use fictional data for demonstrations; do not commit real student personal information.