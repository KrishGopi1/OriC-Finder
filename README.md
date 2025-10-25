# OriC Finder — Full-stack (React + Flask)

**OriC Finder** predicts the origin of replication (OriC) in prokaryotic genomes using GC-skew analysis and frequent k-mer detection.
This repo contains a React frontend and a Flask backend (with Matplotlib server-side plotting).

## Ready to use
https://oric-finder.onrender.com/

## Features
- Upload FASTA (*.fna, *.fa) or paste raw sequence
- Compute cumulative G-C skew and find minimum skew position (OriC)
- Extract configurable window around OriC and find most frequent k-mers
- Server-side skew plot (Matplotlib) returned as PNG and displayed in the UI
- Ready for deployment (Procfile, gunicorn)

## Quick start (development)
### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

### Frontend (using npm)
```bash
cd frontend
npm install
npm run dev   # or `npm start` depending on your setup
```


## Project structure
```
OriC_Finder/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ Procfile
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ index.html
│  ├─ src/
│  │  ├─ main.jsx
│  │  ├─ App.jsx
│  │  ├─ api.js
│  │  └─ index.css
└─ README.md
```
