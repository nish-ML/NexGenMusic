## Music Generation API (Django + DRF)

Endpoints:
- POST `/api/register/` — create user
- POST `/api/login/` — get JWT access/refresh
- POST `/api/generate/` — generate music from `prompt`, optional `duration` seconds
- GET `/api/history/` — list current user's generations

### Setup

PowerShell:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Usage

1) Register:

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"t@e.com","password":"Passw0rd!"}'
```

2) Login (JWT):

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Passw0rd!"}'
```

Copy `access` token.

3) Generate music:

```bash
curl -X POST http://localhost:8000/api/generate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"happy upbeat electronic melody","duration":10}'
```

Returns JSON with `audio_file` path, `mood`, `sentiment`.

4) History:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8000/api/history/
```

Audio files are saved under `media/generated/` and served during DEBUG.

Note: On first run, models are downloaded from Hugging Face (MusicGen, DistilBERT, DistilRoBERTa emotion classifier), which can be large (~2.7 GB combined) and may take time.

### Frontend UI

Pages are available once you run the server:

- `http://localhost:8000/` — home overview
- `http://localhost:8000/register/` — create account
- `http://localhost:8000/login/` — obtain JWT and store locally
- `http://localhost:8000/generate/` — submit prompts and download audio
- `http://localhost:8000/history/` — replay saved generations & log out


