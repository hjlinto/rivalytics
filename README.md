# marvel-rivals-meta-tracker

# Load up virtual env
source api/.venv/Scripts/activate

# Start up backend API
python -m uvicorn api.main:app --reload --port 8000

# API endpoints
http://127.0.0.1:8000/health
http://127.0.0.1:8000/heroes

# Start up frontend
npm run dev

# Load frontend @
http://localhost:3000