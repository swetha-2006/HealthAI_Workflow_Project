# HealthAI_Workflow_Project (Corrected)

This corrected package contains a fixed `app.py` and supporting files. The Flask app runs in MOCK mode by default so you can demo without an OpenAI API key.

## Quick start (Windows / VS Code)

1. Extract the ZIP and open the folder in VS Code.
2. Create a `.env` file (or copy `.env.example`) with:
```
OPENAI_API_KEY=
SECRET_KEY=demo123
PORT=5000
```
(Leave `OPENAI_API_KEY` empty to use mock mode.)

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run:
```
python app.py
```

5. Test (exact curl):
```
curl -X POST http://localhost:5000/process ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: demo123" ^
  -d "{"prompt":"Persistent cough and mild fever for 3 days","note_id":"case001","timestamp":"2025-12-11T12:00:00Z"}"
```

Expected JSON response is included in `sample_output.json`.

## Files
- `app.py` — corrected Flask app
- `requirements.txt`
- `.env.example`
- `demo.http`
- `sample_output.json`
- `README.md`