# Clausify AI ⚡

### AMD-Accelerated Enterprise Document Intelligence

> Upload contracts, quotations, and invoices.
> Ask anything in plain language.
> Get evidence-backed **decisions** — not summaries. Decisions.

**AMD Developer Hackathon: ACT III | lablab.ai | July 2026**

---

## What is Clausify?

Clausify AI reads multiple business documents simultaneously, detects conflicts and contradictions across them, and provides evidence-cited answers to any question — all powered by AMD hardware.

**The problem:** Procurement teams spend hours cross-referencing contracts, invoices, and quotations. They miss overcharges, conflicting terms, and expired deadlines.

**Our solution:** Upload your documents. Clausify finds the $3,300 overcharge your team missed, flags the expired contract deadline, and recommends the best supplier — with exact source citations for every claim.

---

## AMD Integration

| Layer | Technology | Hardware |
|-------|-----------|----------|
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | AMD Instinct MI300X via ROCm |
| LLM Inference | DeepSeek V4 Pro | Fireworks AI on AMD Instinct MI300X |
| Dev/Testing | Llama 3.3 70B Versatile | Groq on AMD MI300X |

- `LLM_PROVIDER=AMD` → for production demo (Fireworks AI on AMD MI300X)
- `LLM_PROVIDER=GROQ` → for development and testing (free, fast)

Switch between them with a single env var. No code changes needed.

---

## Features

- 📄 Multi-document upload (PDF, PNG, JPG, JPEG) — up to 10 files, 10MB each
- 🔍 OCR for scanned invoices and images (pytesseract + PyMuPDF)
- ⚡ Cross-document **Conflict Detection Engine** — flags contradictions automatically
- 📊 Executive summary, risk analysis, supplier comparison matrix, recommendation
- 💬 Decision Copilot chat with SSE streaming responses
- 📎 Evidence-cited structured answers (Answer → Evidence → Risk → Recommendation)
- 📥 PDF & DOCX report export with analytics dashboard (ReportLab + python-docx)
- 🎯 Pre-loaded demo mode (judges can try instantly, zero upload needed)
- 🐳 Fully containerized (Docker + Docker Compose)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite 6 + Tailwind CSS 4 |
| Routing | React Router 7 |
| State | React Context + useReducer (persisted to localStorage) |
| Icons | Lucide React |
| Toasts | Sonner |
| Backend | Python 3.11 + FastAPI + Uvicorn |
| Vector DB | ChromaDB (persistent, per-session collections) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, 384-dim) |
| LLM | Groq SDK / Anthropic SDK / AMD Developer Cloud (httpx) |
| PDF Export | ReportLab |
| OCR | PyMuPDF + pytesseract + Pillow |
| Rate Limiting | slowapi |
| Deployment | Docker / Railway (backend) + Vercel (frontend) |

---

## Quick Start

### Option 1: Docker (Recommended for judges)

```bash
# Clone the repo
git clone https://github.com/your-username/AmdHackthon-main.git
cd AmdHackthon-main

# Create backend env file
cp backend/.env.example backend/.env
# Edit backend/.env — add your GROQ_API_KEY (or AMD keys)

# Run everything
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Demo (no upload needed): http://localhost:3000/demo

### Option 2: Local Development

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env — add GROQ_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173, backend at http://localhost:8000.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | No | `GROQ` | `GROQ`, `CLAUDE`, or `AMD` |
| `GROQ_API_KEY` | Yes (if GROQ) | — | Get free key at https://console.groq.com |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Groq model |
| `ANTHROPIC_API_KEY` | Yes (if CLAUDE) | — | Anthropic API key |
| `AMD_CLOUD_API_KEY` | Yes (if AMD) | — | AMD Developer Cloud key |
| `AMD_CLOUD_ENDPOINT` | Yes (if AMD) | — | AMD API endpoint |
| `ALLOWED_ORIGINS` | No | `*` | CORS origins |
| `PORT` | No | `8000` | Server port |

### Frontend (`frontend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend URL |

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/upload` | Upload documents (multipart/form-data) |
| GET | `/api/session/{id}/check` | Check if session is still valid |
| POST | `/api/analyze` | Run full AI analysis on session |
| POST | `/api/suggest-questions` | Generate contextual quick questions |
| POST | `/api/chat` | RAG Q&A (JSON response) |
| POST | `/api/chat/stream` | RAG Q&A (SSE streaming) |
| POST | `/api/report` | Generate PDF or DOCX report (format param) |
| GET | `/api/demo` | Pre-loaded demo data |
| GET | `/health` | Health check |

---

## Project Structure

```
AmdHackthon-main/
├── docker-compose.yml          # One command to run everything
├── backend/
│   ├── Dockerfile              # Backend container
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt        # Python deps
│   ├── .env.example            # Env var documentation
│   ├── routers/                # API endpoints (5 routers)
│   ├── services/               # Business logic (8 services)
│   ├── models/                 # Pydantic data models
│   ├── prompts/                # LLM prompt templates (6 prompts)
│   ├── tests/                  # pytest test suite
│   └── data/                   # Persisted sessions + ChromaDB
├── frontend/
│   ├── Dockerfile              # Frontend container (nginx)
│   ├── package.json            # Node deps
│   ├── vite.config.ts          # Vite build config
│   └── src/
│       ├── main.tsx            # Entry (ErrorBoundary → AppProvider → App)
│       ├── app/
│       │   ├── App.tsx         # SessionGuard + Router + Toaster
│       │   ├── routes.tsx      # Lazy-loaded routes
│       │   ├── pages/          # Landing, Dashboard, Chat, Demo
│       │   └── components/     # NavigationBar, Badges, Buttons, etc.
│       └── lib/
│           ├── api.ts          # All API calls (fetch-based)
│           ├── store.tsx       # Context + useReducer state
│           └── types.ts        # TypeScript interfaces
└── .kiro/
    ├── agents/                 # 7 Kiro sub-agents for development
    └── specs/                  # UI redesign specification
```

---

## How It Works (Architecture)

```
User uploads files
    ↓
DocumentParser extracts text (PyMuPDF + OCR)
    ↓
EmbeddingService chunks text + generates 384-dim vectors
    ↓
VectorStore saves chunks in ChromaDB (per-session)
    ↓
AnalysisService runs parallel LLM calls:
  • Executive Summary
  • Risk Analysis
  • Comparison Matrix
  • Conflict Detection (pairwise)
  • Recommendation
    ↓
Dashboard displays results
    ↓
Chat uses RAG: embed question → vector search → LLM with context → structured response
```

---

## For Teammates / AI Assistants

If you're a teammate (or an AI helping a teammate), here's what you need to know:

### Rules
- **Never break existing API contracts** — `frontend/src/lib/types.ts` defines the exact shapes
- **Never modify** `api.ts`, `store.tsx`, or `types.ts` without discussing first
- **Use `LLM_PROVIDER=GROQ` for all testing** — AMD credits are for demo day only
- **State management is Context + useReducer** (NOT Redux, NOT Zustand)
- **Routing is React Router 7** (NOT Next.js)
- **Icons are Lucide React** (NOT Material Symbols)

### Key Files to Read First
1. `backend/main.py` — how services are wired together
2. `backend/services/llm_service.py` — LLM provider abstraction
3. `frontend/src/lib/api.ts` — all API calls
4. `frontend/src/lib/store.tsx` — global state shape
5. `frontend/src/lib/types.ts` — TypeScript interfaces (source of truth)

### Running Tests
```bash
cd backend
# Forces GROQ provider — never uses AMD credits
LLM_PROVIDER=GROQ pytest tests/ -v
```

### Kiro Agents Available
There are 7 specialized agents in `.kiro/agents/` for automated development:
1. `clausify-ui-redesign` — Apply new design system
2. `clausify-frontend-integration` — Verify API wiring, add toasts/shortcuts
3. `clausify-backend-hardening` — Production-grade improvements
4. `clausify-testing` — Full test suite (GROQ only)
5. `clausify-performance` — Speed optimization
6. `clausify-deployment` — Railway + Vercel configs
7. `clausify-demo-validator` — Final pre-submission validation

Run them sequentially: 1 → 2 → 3 → 4 → 5 → 6 → 7

---

## Switching to AMD (Demo Day)

```bash
# In backend/.env, change:
LLM_PROVIDER=AMD
AMD_CLOUD_API_KEY=<your-key>
AMD_CLOUD_ENDPOINT=<your-endpoint>

# Restart backend — that's it
```

The system auto-detects AMD ROCm for embeddings and routes LLM calls to AMD Developer Cloud.

---

## Demo for Judges

1. **Zero-upload demo:** Visit `/demo` — 5 pre-loaded procurement docs, full analysis, pre-seeded chat
2. **Upload flow:** Drop PDFs on `/` → analysis in ~15s → dashboard with conflicts highlighted
3. **Chat:** Ask "Which supplier is safest?" → streaming response with evidence citations
4. **Export:** Click export dropdown → choose PDF or DOCX → download professional report with analytics

---

## Team — Clausify AI 🇵🇭

Built by **Rhenmart Dela Cruz** and team
AWS Cloud Club Lead · STI Global City · Taguig, Philippines

**Teammates:** Julie Ann Tiron · Mica Pauline Calingo · Reymark Panes

**AI Orchestration Stack:**
- Claude (planning & architecture)
- Kiro (implementation & code generation)
- Groq (dev/testing LLM — saves AMD credits)
- AMD Developer Cloud (production inference)

---

## License

MIT

---

*Clausify AI — AMD Developer Hackathon: ACT III*
*lablab.ai | July 2026*
