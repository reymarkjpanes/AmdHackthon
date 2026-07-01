# DEALFLOW AI — KIRO ECC STEERING DOCUMENT v2.0
# AMD Developer Hackathon: ACT II
# Team: Rhenmart, Julie, Mica, Panes 🇵🇭
# Deadline: July 11, 2026 — 11PM PST
# Track: Vision & Multimodal AI (Track 3)
# ============================================================

---

## 🧠 PROJECT IDENTITY

Product Name:    DealFlow AI
Tagline:         "Upload documents. Ask anything. Decide with confidence."
Track:           Track 3 — Vision & Multimodal AI (lablab.ai AMD Hackathon)
Core Value:      Upload any business document. Ask in plain language.
                 Get evidence-based decisions in under 60 seconds.
AMD Stack:       Llama 3.2 Vision on AMD MI300X via AMD Developer Cloud
                 + sentence-transformers embeddings on ROCm
Hosted:          Frontend → Vercel | Backend → Railway.app
Repo:            github.com/[team]/dealflow-ai (PUBLIC)

---

## 🎯 PROBLEM WE SOLVE

Procurement managers, operations directors, and business analysts
spend hours manually reading contracts, quotations, and invoices
before making decisions.

DealFlow AI reads all documents simultaneously, detects conflicts,
compares options, and answers questions — with evidence.

---

## 🏗️ SYSTEM ARCHITECTURE

```
USER BROWSER (Desktop + Mobile Responsive)
     │
     ▼
NEXT.JS 14 FRONTEND — Vercel
  /              → Landing + Upload
  /dashboard     → Analysis Results
  /chat          → Decision Copilot
  /demo          → Pre-loaded Demo (NO upload required)
     │
     │ REST API (HTTPS)
     ▼
FASTAPI BACKEND — Railway.app
  POST /api/upload    → Document ingestion
  POST /api/analyze   → Full AI analysis
  POST /api/chat      → RAG-powered Q&A
  POST /api/compare   → Conflict detection
  POST /api/report    → PDF export
  GET  /api/demo      → Pre-loaded mock data
     │
     ├── DOCUMENT PIPELINE
     │     PDF  → PyMuPDF (text extraction)
     │     IMG  → pytesseract + Pillow (OCR) ← MULTIMODAL
     │     Text → Custom chunker (512 tokens, 50 overlap)
     │
     ├── EMBEDDING SERVICE ← AMD GPU (ROCm)
     │     Model: all-MiniLM-L6-v2
     │     Hardware: AMD Instinct MI300X
     │     # AMD: GPU-accelerated embedding generation
     │
     ├── VECTOR STORE
     │     ChromaDB (in-memory, per-session)
     │
     ├── LLM SERVICE ← AMD GPU (Cloud)
     │     Primary: Llama 3.2 Vision 11B (AMD Developer Cloud)
     │     Fallback: Claude API (Anthropic)
     │     # AMD: Cloud inference on MI300X
     │
     └── CONFLICT DETECTION ENGINE
           Cross-document comparison
           Numerical + clause contradiction detection

SUPABASE
  Session metadata + upload logs (NO document storage)
```

---

## 📁 EXACT FOLDER STRUCTURE

```
dealflow-ai/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                  ← Landing + Upload
│   │   ├── dashboard/
│   │   │   └── page.tsx              ← Analysis Dashboard
│   │   ├── chat/
│   │   │   └── page.tsx              ← Decision Copilot
│   │   ├── demo/
│   │   │   └── page.tsx              ← Demo Mode (pre-loaded)
│   │   └── layout.tsx                ← Root layout + fonts
│   ├── components/
│   │   ├── ui/                       ← shadcn/ui components
│   │   ├── upload/
│   │   │   ├── DropZone.tsx
│   │   │   └── FileList.tsx
│   │   ├── dashboard/
│   │   │   ├── ExecutiveSummary.tsx
│   │   │   ├── RiskPanel.tsx
│   │   │   ├── ComparisonMatrix.tsx
│   │   │   ├── ConflictAlert.tsx     ← KILLER FEATURE
│   │   │   └── RecommendationCard.tsx
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── EvidenceTag.tsx
│   │   │   └── AIThinkingAnimation.tsx
│   │   └── shared/
│   │       ├── AMDBadge.tsx
│   │       ├── RiskBadge.tsx
│   │       ├── Navbar.tsx
│   │       └── ProcessingState.tsx
│   ├── lib/
│   │   ├── api.ts                    ← All API calls
│   │   ├── mock-data.ts              ← Demo mode hardcoded data
│   │   └── types.ts                  ← TypeScript interfaces
│   ├── hooks/
│   │   ├── useUpload.ts
│   │   ├── useAnalysis.ts
│   │   └── useChat.ts
│   └── public/
│       └── demo-docs/               ← Sample doc thumbnails for UI
│
├── backend/
│   ├── main.py                       ← FastAPI app entry
│   ├── routers/
│   │   ├── upload.py
│   │   ├── analyze.py
│   │   ├── chat.py
│   │   ├── compare.py
│   │   └── report.py
│   ├── services/
│   │   ├── document_parser.py        ← PDF + OCR
│   │   ├── embedding_service.py      ← AMD ROCm
│   │   ├── vector_store.py           ← ChromaDB
│   │   ├── llm_service.py            ← AMD Cloud + fallback
│   │   ├── conflict_engine.py        ← Cross-doc comparison
│   │   ├── analysis_service.py       ← Dashboard generation
│   │   └── pdf_generator.py          ← ReportLab export
│   ├── prompts/
│   │   ├── system_prompt.py
│   │   ├── executive_summary.py
│   │   ├── risk_analysis.py
│   │   ├── conflict_detection.py
│   │   ├── chat_copilot.py
│   │   └── recommendation.py
│   ├── models/
│   │   ├── document.py               ← Pydantic schemas
│   │   └── response.py               ← Pydantic schemas
│   ├── tests/
│   │   ├── test_upload.py
│   │   ├── test_analysis.py
│   │   ├── test_conflict.py
│   │   └── test_chat.py
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .kiro/
│   └── steering/
│       └── project.md                ← THIS FILE
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AMD_INTEGRATION.md
│   └── API.md
│
├── README.md
├── docker-compose.yml
└── .env.example
```

---

## 🛠️ TECH STACK

### Frontend
```
Framework:    Next.js 14 (App Router)
Styling:      Tailwind CSS
Components:   shadcn/ui
Animation:    Framer Motion
State:        Zustand
HTTP:         Axios
Upload:       react-dropzone
Icons:        Lucide React
Fonts:        DM Sans + Inter + JetBrains Mono
Deploy:       Vercel (free tier)
```

### Backend
```
Framework:    FastAPI (Python 3.11)
PDF:          PyMuPDF (fitz)
OCR:          pytesseract + Pillow
Embeddings:   sentence-transformers (AMD ROCm)
Vector DB:    ChromaDB (in-memory)
LLM:          AMD Developer Cloud (Llama 3.2 Vision 11B)
Fallback:     Claude API (Anthropic)
PDF Export:   ReportLab
Server:       Uvicorn
Deploy:       Railway.app (free tier)
```

### Infrastructure
```
Database:     Supabase (metadata only)
AI Compute:   AMD Developer Cloud ($100 x 4 = $400 total)
GPU:          AMD Instinct MI300X
Framework:    ROCm
CI/CD:        GitHub Actions
```

---

## 🎨 DESIGN SYSTEM

### Colors
```typescript
const colors = {
  bgPrimary:   '#080D1A',   // main background
  bgSecondary: '#0D1528',   // cards
  bgTertiary:  '#111E35',   // hover states
  border:      '#1E2D4A',   // subtle borders
  accentBlue:  '#3B7BF6',   // primary, AMD glow
  accentGlow:  'rgba(59,123,246,0.15)',
  textPrimary: '#F0F4FF',
  textMuted:   '#8B9CC8',
  success:     '#10B981',
  warning:     '#F59E0B',
  danger:      '#EF4444',
  amdRed:      '#ED1C24',   // AMD brand — use sparingly
}
```

### Typography
```
Display: DM Sans 700       → headings, hero
Body:    Inter 400/500     → all UI text
Mono:    JetBrains Mono    → evidence quotes, filenames, data
```

### Design Rules
```
- Dark corporate aesthetic — Bloomberg meets Linear.app
- Border radius: 8px cards, 12px buttons (max)
- Glow effects on active/hover: box-shadow with accentGlow
- Subtle grain texture on backgrounds (CSS noise)
- Never use bright/playful colors
- Information-dense but organized
- Every loading state has AMD-themed copy
```

---

## 🤖 AI BEHAVIOR — STRICT RULES

### Every AI Response Must Follow This Format
```
ANSWER:
[Direct, specific answer — no fluff]

EVIDENCE:
[Exact reference from uploaded document]
Source: [filename]

RISK:
[Concern flagged — or "No immediate risks identified"]

RECOMMENDATION:
[Specific, actionable next step]
```

### Hard Constraints (Never Violate)
```python
MUST_DO = [
    "Always cite source document by filename",
    "Use conservative language for risks",
    "Say 'Insufficient evidence in uploaded documents' when missing",
    "Compare across documents when multiple uploaded",
    "Flag all numerical inconsistencies (price, dates, quantities)",
]

MUST_NOT = [
    "Invent facts not in documents",
    "Assume missing information",
    "Give legal advice (flag legal concerns only)",
    "Answer from general knowledge alone",
    "Hallucinate document content",
]
```

### System Prompt
```python
SYSTEM_PROMPT = """
You are DealFlow AI, an enterprise document intelligence analyst.

Your role is to help business professionals make better decisions
by analyzing uploaded business documents — contracts, quotations,
invoices, purchase orders, and reports.

STRICT RULES:
1. Only use information from the provided document context below
2. Always cite your sources with exact document filenames
3. Structure EVERY response: ANSWER → EVIDENCE → RISK → RECOMMENDATION
4. If information is missing: "Insufficient evidence found in uploaded documents"
5. Flag any numerical inconsistencies, conflicting terms, or missing clauses
6. Be conservative — when in doubt, flag as a risk
7. Never give legal advice — flag legal concerns only
8. Use professional enterprise language at all times

DOCUMENT CONTEXT:
{retrieved_chunks}

UPLOADED DOCUMENTS IN THIS SESSION:
{document_list}
"""
```

### Conflict Detection Prompt
```python
CONFLICT_PROMPT = """
Analyze these business documents for inconsistencies and conflicts.

Documents:
{document_summaries}

Find ALL conflicts including:
- Price discrepancies for same item/service
- Contradicting payment terms or deadlines  
- Different party names or entity descriptions
- Quantity mismatches
- Conflicting legal clauses

For each conflict output EXACTLY:
CONFLICT TYPE: [category]
DOCUMENT A: [filename] — [exact quote]
DOCUMENT B: [filename] — [exact quote]
SEVERITY: [HIGH / MEDIUM / LOW]
EXPLANATION: [why this is a risk]
SUGGESTED ACTION: [what to do]

Severity guide:
HIGH   = numerical difference >20% OR legal contradiction
MEDIUM = different terms for same concept
LOW    = minor wording differences

If no conflicts: "No conflicts detected across uploaded documents."
"""
```

---

## 🔌 API ENDPOINTS — FULL SPEC

### POST /api/upload
```python
# Input
{
  "files": [multipart/form-data]  # PDF, PNG, JPG, JPEG
}

# Output
{
  "session_id": "uuid",
  "documents": [
    {
      "id": "uuid",
      "name": "Contract_A.pdf",
      "type": "pdf",
      "page_count": 5,
      "status": "processed",
      "extracted_text_length": 3420
    }
  ]
}

# Process flow:
# 1. Validate file type + size (max 10MB)
# 2. Extract text (PyMuPDF for PDF, pytesseract for images)
# 3. Chunk text (512 tokens, 50 token overlap)
# 4. Generate embeddings (AMD ROCm)
# 5. Store in ChromaDB (keyed by session_id)
# 6. Return document metadata
```

### POST /api/analyze
```python
# Input
{
  "session_id": "uuid"
}

# Output
{
  "executive_summary": "string",
  "risks": [
    {
      "level": "HIGH|MEDIUM|LOW",
      "description": "string",
      "source": "filename.pdf"
    }
  ],
  "comparison_matrix": [
    {
      "field": "string",
      "values": {"doc_a": "value", "doc_b": "value"},
      "winner": "doc_a|doc_b|tie"
    }
  ],
  "conflicts": [
    {
      "type": "string",
      "doc_a": {"name": "filename", "quote": "string"},
      "doc_b": {"name": "filename", "quote": "string"},
      "severity": "HIGH|MEDIUM|LOW",
      "explanation": "string",
      "action": "string"
    }
  ],
  "recommendation": "string"
}
```

### POST /api/chat
```python
# Input
{
  "session_id": "uuid",
  "message": "string",
  "history": [
    {"role": "user", "content": "string"},
    {"role": "assistant", "content": "string"}
  ]
}

# Output
{
  "answer": "string",
  "evidence": [
    {
      "quote": "string",
      "source_doc": "filename.pdf",
      "relevance_score": 0.92
    }
  ],
  "risk": "string",
  "recommendation": "string"
}
```

### POST /api/report
```python
# Input
{
  "session_id": "uuid"
}

# Output: PDF file download (application/pdf)
# Content: Executive Summary + Risks + Comparison + Conflicts + Recommendation
```

### GET /api/demo
```python
# No input required
# Output: Pre-loaded mock analysis data (hardcoded realistic data)
# Used by /demo page — zero upload required
```

---

## 🔴 AMD INTEGRATION — CODE COMMENTS REQUIRED

Every AMD-specific section MUST have this comment pattern:

```python
# AMD: [what this does on AMD hardware]
# Model: [model name]
# Hardware: AMD Instinct MI300X
# Framework: ROCm

# Example in embedding_service.py:
# AMD: GPU-accelerated document embedding generation
# AMD: Using sentence-transformers on ROCm backend
# AMD: ~5x faster than CPU baseline (measured Day 4)

# Example in llm_service.py:
# AMD: LLM inference via AMD Developer Cloud API
# AMD: Model: Llama 3.2 Vision 11B
# AMD: Enables multimodal document understanding (Track 3)
```

---

## 📦 REQUIREMENTS.TXT

```
fastapi==0.111.0
uvicorn==0.30.0
python-multipart==0.0.9
PyMuPDF==1.24.0
pytesseract==0.3.10
Pillow==10.3.0
sentence-transformers==3.0.0
chromadb==0.5.0
pydantic==2.7.0
httpx==0.27.0
anthropic==0.28.0
reportlab==4.2.0
python-jose==3.3.0
supabase==2.4.0
```

---

## 🗃️ MOCK DATA (Demo Mode)

```typescript
// frontend/lib/mock-data.ts

export const DEMO_DOCUMENTS = [
  { id: '1', name: 'Supplier_A_Quotation.pdf', type: 'pdf', pages: 3, status: 'processed' },
  { id: '2', name: 'Supplier_B_Quotation.pdf', type: 'pdf', pages: 3, status: 'processed' },
  { id: '3', name: 'Existing_Contract_TechCorp.pdf', type: 'pdf', pages: 8, status: 'processed' },
  { id: '4', name: 'Invoice_TechCorp_March2026.pdf', type: 'pdf', pages: 2, status: 'processed' },
  { id: '5', name: 'Procurement_Policy.png', type: 'image', status: 'processed' }, // ← multimodal
]

export const DEMO_ANALYSIS = {
  executive_summary: `Analysis of 5 procurement documents reveals two competing 
    supplier quotations for IT infrastructure equipment. Supplier B presents a more 
    favorable financial profile at $42,800 vs Supplier A at $45,200, with more flexible 
    60-day payment terms. A critical price discrepancy has been detected between the 
    existing TechCorp invoice ($48,500) and their current quotation ($45,200) — a $3,300 
    variance warranting clarification before any contract renewal decision.`,

  risks: [
    {
      level: 'HIGH',
      description: 'Price discrepancy: TechCorp invoice ($48,500) exceeds their current quotation ($45,200) by $3,300 — 7.3% variance',
      source: 'Invoice_TechCorp_March2026.pdf'
    },
    {
      level: 'MEDIUM',
      description: 'Current TechCorp contract expires September 2026 — procurement must close within 90 days to avoid service gap',
      source: 'Existing_Contract_TechCorp.pdf'
    },
    {
      level: 'LOW',
      description: 'Supplier A requires 30-day payment terms — more aggressive than company standard 60-day policy',
      source: 'Supplier_A_Quotation.pdf'
    }
  ],

  conflicts: [
    {
      type: 'PRICE DISCREPANCY',
      doc_a: { name: 'Invoice_TechCorp_March2026.pdf', quote: 'Total amount due: $48,500.00' },
      doc_b: { name: 'Supplier_A_Quotation.pdf', quote: 'Total quotation value: $45,200.00' },
      severity: 'HIGH',
      explanation: 'TechCorp\'s last invoice is $3,300 higher than their current quotation for equivalent equipment. Pricing inconsistency detected.',
      action: 'Request written clarification from TechCorp explaining the $3,300 price difference before any contract renewal.'
    }
  ],

  comparison_matrix: [
    { field: 'Total Price', values: { 'Supplier A': '$45,200', 'Supplier B': '$42,800' }, winner: 'Supplier B' },
    { field: 'Payment Terms', values: { 'Supplier A': '30 days', 'Supplier B': '60 days' }, winner: 'Supplier B' },
    { field: 'Delivery Time', values: { 'Supplier A': '14 days', 'Supplier B': '21 days' }, winner: 'Supplier A' },
    { field: 'Warranty', values: { 'Supplier A': '1 year', 'Supplier B': '2 years' }, winner: 'Supplier B' },
    { field: 'Support SLA', values: { 'Supplier A': '48 hours', 'Supplier B': '24 hours' }, winner: 'Supplier B' },
  ],

  recommendation: `Proceed with Supplier B. At $42,800 vs $45,200, Supplier B is $2,400 
    cheaper while offering superior terms: 60-day payment flexibility, 2-year warranty 
    (vs 1-year), and 24-hour support SLA. Regardless of final supplier choice, clarify 
    the TechCorp invoice discrepancy — a $3,300 unexplained variance is a procurement risk.`
}

export const DEMO_CHAT_HISTORY = [
  {
    role: 'user',
    content: 'Which supplier should I choose?'
  },
  {
    role: 'assistant',
    answer: 'Supplier B is the recommended choice based on overall value and terms.',
    evidence: [
      { quote: 'Total quotation value: $42,800.00', source_doc: 'Supplier_B_Quotation.pdf', relevance_score: 0.97 },
      { quote: 'Warranty period: 24 months from delivery date', source_doc: 'Supplier_B_Quotation.pdf', relevance_score: 0.91 },
    ],
    risk: 'Supplier B\'s 21-day delivery timeline may be a constraint if procurement is urgent.',
    recommendation: 'Initiate contract discussions with Supplier B. Negotiate delivery timeline if 14 days is critical.'
  }
]
```

---

## ⚙️ GITHUB ACTIONS CI

```yaml
# .github/workflows/ci.yml
name: DealFlow AI CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install and build
        run: |
          cd frontend
          npm install
          npm run build
      - name: Type check
        run: |
          cd frontend
          npm run type-check
```

---

## 📝 BRANCH STRATEGY

```
main          → production only — merge from develop after testing
develop       → integration branch — all features merge here first
feat/frontend → Rhenmart (Next.js, UI components)
feat/backend  → Panes (FastAPI, document pipeline)
feat/ai       → Julie (LLM, RAG, prompts, AMD integration)
feat/testing  → Mica (tests, PDF export, demo data)
```

Commit message format:
```
feat:     new feature
fix:      bug fix
docs:     documentation
style:    formatting, no logic change
test:     adding tests
amd:      AMD-specific integration work ← custom type
```

---

## 🔧 KIRO CODING RULES

When Kiro generates code for DealFlow AI:

1. TypeScript strict — no `any` types on frontend
2. Pydantic v2 models for all FastAPI schemas
3. Every AI response enforces Answer/Evidence/Risk/Recommendation
4. Zero hardcoded API keys — always `process.env` or `os.environ`
5. Every async operation has a loading state in UI
6. Tailwind responsive classes on everything (mobile-first)
7. AMD code gets `# AMD:` comment prefix
8. New feature = new test file in backend/tests/
9. /demo page must never break — it's the judge experience
10. Error states must show helpful messages (not raw errors)
11. Working > Perfect (6-day timeline constraint)
12. After any AMD API call, log response time for benchmark doc

---

*DealFlow AI — Kiro ECC Steering v2.0*
*🇵🇭 Filipino Junior Developers. International Stage. Full Send.*
