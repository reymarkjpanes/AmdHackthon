# ============================================================
# DEALFLOW AI — MASTER PLAN v2.0
# AMD Developer Hackathon: ACT II
# Team: Rhenmart, Julie, Mica, Panes 🇵🇭
# Deadline: July 11, 2026 — 11PM PST
# ============================================================

---

# 🧭 SECTION 1: STRATEGIC DECISIONS

## ❓ Web App, Mobile App, or Business System Integration?

### SHORT ANSWER FOR HACKATHON: WEB APP ONLY

Here's the full breakdown so the team understands WHY:

### Option A — Web App Only ✅ (DO THIS)
```
Pros:
- Judges access it instantly from any browser
- No install required — zero friction demo
- Fastest to build in 6 days
- Vercel deployment = always live
- Works on desktop, tablet, mobile via responsive design

Cons:
- Not a "native" mobile experience
- Can't access phone camera directly
```

### Option B — Mobile App ❌ (DON'T — for now)
```
Pros:
- Could snap photos of invoices with camera
- More impressive in theory

Cons:
- App Store/Play Store submission takes days
- React Native adds complexity and build time
- Judges won't install an app to judge a hackathon project
- Kills your timeline
```

### Option C — Business System Integration ❌ (DON'T — for hackathon)
```
"Integration" means connecting to SAP, Oracle, Microsoft 365,
Salesforce, etc. This is:
- Enterprise sales cycle = months
- Requires OAuth, API keys, enterprise agreements
- Way outside 6-day scope
- Judges don't expect this at hackathon level

BUT — mention it as a roadmap item in your pitch:
"Phase 2: Native integrations with SAP, Microsoft 365,
and Google Workspace via API connectors"
This shows business maturity without having to build it.
```

### The RIGHT Play: Responsive Web App + API-Ready Backend
```
What you actually build:
✅ Responsive web app (works perfectly on mobile browser)
✅ Backend with clean REST API (shows integration-ready)
✅ "Integrations" section in pitch deck (roadmap slide)
✅ Demo on desktop for judges (best experience)

This gives you:
- Speed of web development
- "Mobile-ready" claim (responsive)
- "Integration-ready" claim (REST API)
- "Enterprise-scalable" claim (AMD cloud backend)

Without killing your timeline.
```

---

# 🎯 SECTION 2: FINAL PROJECT IDENTITY

## Product Name
**DealFlow AI**

## Tagline
*"Upload documents. Ask anything. Decide with confidence."*

## Track Selection
**Track 3: Vision & Multimodal AI** ← LOOPHOLE (less competition than Track 1)

Why Track 3 fits:
- DealFlow processes PDFs (text) + PNG/JPG (images) = multimodal
- OCR on scanned invoices = vision processing
- Uses Llama 3.2 Vision optimized for ROCm
- Most teams go Track 1 — you stand out in Track 3

## One-Line Pitch
> "DealFlow AI is an AMD-accelerated multimodal document intelligence platform that helps procurement and operations teams make better business decisions — in under 60 seconds."

## Killer Differentiator
**Conflict Detection Engine** — automatically flags contradictions BETWEEN documents.
Nobody else will have this at this level of polish.

---

# 🏗️ SECTION 3: FINAL ARCHITECTURE

```
┌─────────────────────────────────────────────────┐
│              USER (Browser / Mobile Browser)     │
└────────────────────────┬────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────┐
│           NEXT.JS 14 FRONTEND                   │
│         Tailwind CSS + shadcn/ui                │
│    Responsive: Desktop → Tablet → Mobile        │
│    Hosted: Vercel (free tier)                   │
│                                                 │
│  Pages:                                         │
│  /           → Landing + Upload                 │
│  /dashboard  → Analysis Results                 │
│  /chat       → Decision Copilot                 │
│  /demo       → Pre-loaded Demo (no upload)      │
└────────────────────────┬────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────┐
│           FASTAPI BACKEND (Python 3.11)         │
│           Hosted: Railway.app (free tier)       │
│                                                 │
│  /api/upload    → Ingest documents              │
│  /api/analyze   → Full AI analysis              │
│  /api/chat      → RAG-powered Q&A               │
│  /api/compare   → Conflict detection            │
│  /api/report    → PDF export                    │
│  /api/demo      → Pre-loaded mock data          │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │         DOCUMENT PIPELINE               │   │
│  │  PDF  → PyMuPDF (text extraction)       │   │
│  │  IMG  → pytesseract + Pillow (OCR)      │   │  ← MULTIMODAL
│  │  Text → Custom chunker (512 tokens)     │   │
│  └──────────────────┬──────────────────────┘   │
│                     │                           │
│  ┌──────────────────▼──────────────────────┐   │
│  │      EMBEDDING SERVICE                  │   │
│  │  sentence-transformers (all-MiniLM-L6)  │   │  ← AMD GPU
│  │  Running on ROCm / AMD MI300X           │   │
│  └──────────────────┬──────────────────────┘   │
│                     │                           │
│  ┌──────────────────▼──────────────────────┐   │
│  │      VECTOR STORE                       │   │
│  │  ChromaDB (in-memory, per session)      │   │
│  └──────────────────┬──────────────────────┘   │
│                     │                           │
│  ┌──────────────────▼──────────────────────┐   │
│  │      LLM SERVICE                        │   │
│  │  Primary: AMD Developer Cloud API       │   │  ← AMD GPU
│  │  Model: Llama 3.2 Vision 11B (ROCm)     │   │
│  │  Fallback: Claude API (Anthropic)       │   │
│  └──────────────────┬──────────────────────┘   │
│                     │                           │
│  ┌──────────────────▼──────────────────────┐   │
│  │      CONFLICT DETECTION ENGINE          │   │
│  │  Cross-document comparison              │   │
│  │  Numerical + clause contradiction check │   │
│  └─────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│              SUPABASE                           │
│  Session metadata + upload logs (no doc store) │
└─────────────────────────────────────────────────┘
```

---

# 🛠️ SECTION 4: COMPLETE TECH STACK

## Frontend
```
Framework:     Next.js 14 (App Router)
Styling:       Tailwind CSS
Components:    shadcn/ui
State:         Zustand
HTTP:          Axios
Upload:        react-dropzone
Charts:        Recharts (for future analytics)
Animation:     Framer Motion (AI chat animations)
Icons:         Lucide React
Font:          DM Sans + Inter + JetBrains Mono (Google Fonts)
Deploy:        Vercel
```

## Backend
```
Framework:     FastAPI (Python 3.11)
PDF Parser:    PyMuPDF (fitz)
OCR:           pytesseract + Pillow
Embeddings:    sentence-transformers
GPU Framework: ROCm (AMD)
Vector Store:  ChromaDB
LLM Primary:   AMD Developer Cloud (Llama 3.2 Vision)
LLM Fallback:  Claude API (Anthropic)
PDF Export:    ReportLab
Server:        Uvicorn
Deploy:        Railway.app
```

## Infrastructure
```
Frontend:      Vercel (free)
Backend:       Railway.app (free tier)
Database:      Supabase (free tier)
AI Compute:    AMD Developer Cloud ($100 x 4 members = $400)
CI/CD:         GitHub Actions
Repo:          GitHub (public — required for submission)
```

---

# 📁 SECTION 5: FOLDER STRUCTURE

```
dealflow-ai/                          ← GitHub repo root
│
├── frontend/                         ← Next.js 14
│   ├── app/
│   │   ├── page.tsx                  ← Landing + Upload
│   │   ├── dashboard/page.tsx        ← Analysis Dashboard
│   │   ├── chat/page.tsx             ← Decision Copilot
│   │   ├── demo/page.tsx             ← Demo Mode
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/                       ← shadcn components
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
│   │   │   └── AIThinkingAnimation.tsx ← Custom animation
│   │   └── shared/
│   │       ├── AMDBadge.tsx
│   │       ├── RiskBadge.tsx
│   │       └── ProcessingState.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── mock-data.ts              ← Demo mode data
│   │   └── types.ts
│   └── public/
│       └── demo-docs/               ← Sample doc thumbnails
│
├── backend/                          ← FastAPI
│   ├── main.py
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
│   │   └── pdf_generator.py          ← Report export
│   ├── prompts/
│   │   ├── system_prompt.py
│   │   ├── executive_summary.py
│   │   ├── risk_analysis.py
│   │   ├── conflict_detection.py
│   │   ├── chat_copilot.py
│   │   └── recommendation.py
│   ├── models/
│   │   ├── document.py
│   │   └── response.py
│   ├── tests/
│   │   ├── test_upload.py
│   │   ├── test_analysis.py
│   │   └── test_conflict.py
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── ci.yml                    ← GitHub Actions
│
├── .kiro/
│   └── steering/
│       └── project.md                ← ECC Steering Doc
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AMD_INTEGRATION.md            ← Benchmark results here
│   └── API.md
│
├── README.md                         ← Polished for judges
├── docker-compose.yml
└── .env.example
```

---

# 🎨 SECTION 6: UI/UX DESIGN SYSTEM

## Color Palette
```
Background Primary:    #080D1A  ← main bg
Background Secondary:  #0D1528  ← cards
Background Tertiary:   #111E35  ← hover states
Border:                #1E2D4A  ← subtle borders
Accent Blue:           #3B7BF6  ← primary actions, AMD glow
Accent Indigo:         #6366F1  ← secondary actions
Glow:                  rgba(59,123,246,0.15)
Text Primary:          #F0F4FF
Text Secondary:        #8B9CC8
Text Tertiary:         #4A5878
Success:               #10B981
Warning:               #F59E0B
Danger:                #EF4444
AMD Red:               #ED1C24  ← use sparingly
```

## Typography
```
Display:   DM Sans 700    ← headings
Body:      Inter 400/500  ← all UI text
Mono:      JetBrains Mono ← evidence quotes, filenames, data
```

## Design Feel
```
Bloomberg Terminal + Linear.app + ChatGPT Enterprise
Dark, precise, data-dense, corporate
Subtle grain texture on bg
Blue glow on active/hover states
Border radius: 8px cards, 12px buttons max
Feel: expensive, trustworthy, fast
```

---

# 📋 SECTION 7: AI BEHAVIOR SPECS

## Core Principle
Every AI response = structured enterprise analysis, not casual chat.

## Mandatory Response Format
```
ANSWER:
[Direct, specific answer]

EVIDENCE:
[Exact quote from document]
Source: [filename]

RISK:
[Concern or "No immediate risks identified"]

RECOMMENDATION:
[Specific actionable next step]
```

## Hard Rules
```
✅ Always cite source document
✅ Conservative language for risks
✅ "Insufficient evidence in uploaded documents" when missing
✅ Compare across documents when multiple uploaded
✅ Flag numerical inconsistencies

❌ Never invent facts
❌ Never assume missing info
❌ Never give legal advice
❌ Never answer from general knowledge alone
```

## Conflict Detection Logic
```
Scan for:
1. Price discrepancies (same item, different amounts)
2. Date conflicts (contradicting deadlines)
3. Payment term differences
4. Quantity mismatches
5. Party name inconsistencies

Severity:
HIGH   → >20% numerical difference or legal contradiction
MEDIUM → Different terms for same concept
LOW    → Minor wording differences
```

## System Prompt
```
You are DealFlow AI, an enterprise document intelligence analyst.

Your role is to help business professionals make better decisions
by analyzing uploaded business documents — contracts, quotations,
invoices, purchase orders, and reports.

STRICT RULES:
1. Only use information from provided document context
2. Always cite sources with exact document names
3. Structure every response: ANSWER → EVIDENCE → RISK → RECOMMENDATION
4. If information missing: "Insufficient evidence found in uploaded documents"
5. Flag numerical inconsistencies, conflicting terms, missing clauses
6. Be conservative — when in doubt, flag as risk
7. Never give legal advice — flag legal concerns only
8. Use professional enterprise language always

CONTEXT: {retrieved_chunks}
SESSION DOCUMENTS: {document_list}
```

---

# 🔴 SECTION 8: AMD INTEGRATION STRATEGY

## Where AMD GPUs Are Used
```
1. EMBEDDING GENERATION
   Service: embedding_service.py
   Model: all-MiniLM-L6-v2 via sentence-transformers
   Hardware: AMD Instinct MI300X (ROCm)
   Comment in code: # AMD: GPU-accelerated embedding generation

2. LLM INFERENCE
   Service: llm_service.py
   Model: Llama 3.2 Vision 11B (multimodal — covers Track 3)
   Hardware: AMD Developer Cloud API
   Comment in code: # AMD: Cloud inference on MI300X

3. VISION/OCR PIPELINE
   Service: document_parser.py
   Model: Llama 3.2 Vision for image understanding
   Hardware: AMD MI300X
   Comment in code: # AMD: Vision model for multimodal doc processing
```

## Benchmark Plan (CRITICAL — run this Day 4)
```
Test setup:
- 5 business documents, avg 8 pages each
- Process: extract → chunk → embed → retrieve

Measure:
CPU baseline:  record total time (seconds)
AMD MI300X:    record total time (seconds)
Speedup ratio: CPU time / AMD time = Xx faster

Put this number on:
- Slide 6 of pitch deck
- README.md
- AMD badge in UI: "Xx faster on AMD MI300X"
- Demo video narration

Even 2x faster = impressive. Don't fake it — run the real test.
```

## AMD Setup Steps (ALL 4 MEMBERS — Day 1)
```
1. Go to: amd.com/en/developer/ai-dev-program.html
2. Sign up for AMD AI Developer Program (free)
3. Each member gets $100 credits = $400 team total
4. Access AMD Developer Cloud console
5. Spin up MI300X instance
6. Install ROCm environment
7. Test connection from backend
```

---

# 🕳️ SECTION 9: LOOPHOLE EXPLOITATION PLAN

## Loophole 1 — Track 3 (Less Competition)
```
Action: Submit under Track 3: Vision & Multimodal AI
Why: Most teams go Track 1 (labeled "for beginners")
How: DealFlow processes images (OCR) = multimodal
Add to description: "Multimodal document processing using
Llama 3.2 Vision optimized for ROCm on AMD MI300X"
```

## Loophole 2 — Build in Public (Extra Prize Pool)
```
Action: Post DAILY on X + LinkedIn
Required: Only 2 posts — post more to stand out

Post schedule:
Day 1: "Just kicked off DealFlow AI for @AIatAMD hackathon.
        Team of 4 Filipino junior devs building enterprise
        document intelligence. Watch us ship. 🇵🇭⚡ #AMDHackathon"

Day 2: Architecture diagram post
Day 3: Backend pipeline working — short video
Day 4: Conflict Detection feature demo clip
Day 5: Full demo video teaser
Day 6: "We shipped. @lablab @AIatAMD 🚀"

Tag every post: @lablab @AIatAMD
Platform: X + LinkedIn (both)
```

## Loophole 3 — Benchmark Number
```
Action: Run actual CPU vs AMD timing test Day 4
Put the number EVERYWHERE:
- Slide deck
- README
- UI badge
- Demo video

Judges remember specific numbers. "5.6x faster" > "faster"
```

## Loophole 4 — Demo Page (Zero Judge Friction)
```
Action: /demo page pre-loaded, NO upload needed
Why: Judges review 50+ projects. They're tired.
     Your demo = click one button, see full product.
     Others = figure out what files to upload.

This alone could be your tiebreaker.
```

## Loophole 5 — Filipino Dev Narrative
```
Action: Own the story in README, pitch, video closing
Script: "Four Filipino junior developers from Taguig built
        an enterprise AI platform in 6 days on AMD cloud
        infrastructure. No senior engineers. No big tech
        backing. Just execution."

AMD + lablab love this story. Nobody else can claim it.
Put it on Slide 9 (Team slide) — make it proud, not humble.
```

## Loophole 6 — Referral Points
```
Action: Generate referral links from dashboard
Share in: STI network, Filipino dev Facebook groups,
          local Discord servers, Cloud Club contacts
200 points per referral who submits = leaderboard visibility
More leaderboard presence = judges see your name more
```

## Loophole 7 — Early Submission
```
Action: Submit Day 5 (July 10), not Day 6 deadline
Why: Shows professionalism + confidence
     Judges sometimes look at early submitters first
     Avoids last-minute technical failures
     Still can update submission until deadline
```

---

# 📅 SECTION 10: 6-DAY EXECUTION SPRINT

## Pre-Hackathon (NOW — June 11 onward)

### This Week (Before July 6 Kickoff)
```
Rhenmart:
  ✅ Send Lovable prompt → generate full frontend
  ✅ Review + polish generated UI
  ✅ Create GitHub repo: dealflow-ai (public)
  ✅ Set up branch strategy
  ✅ Sign up AMD AI Developer Program

Panes:
  ✅ Set up FastAPI project locally
  ✅ Test PyMuPDF PDF extraction
  ✅ Test pytesseract OCR on sample image
  ✅ Sign up AMD AI Developer Program

Julie:
  ✅ Sign up AMD AI Developer Program
  ✅ Access AMD Developer Cloud
  ✅ Test Llama 3.2 Vision via AMD API
  ✅ Write system prompt v1

Mica:
  ✅ Sign up AMD AI Developer Program
  ✅ Create Supabase project
  ✅ Prepare 5 realistic sample business documents
  ✅ Start slide deck template

TEAM:
  ✅ Create lablab Discord team channel
  ✅ Set up daily standup schedule (15 mins, 9PM daily)
  ✅ Post Day 0 Build in Public tweet
```

---

## DAY 1 — July 6 (Kickoff Day)

### Morning (Kick-off stream at 12AM PST = 3PM PH time)
```
All: Watch kick-off stream on Twitch
All: Join Discord Q&A session
All: Confirm AMD credits are active
```

### Afternoon/Evening
```
Rhenmart:
  ✅ Next.js project initialized from Lovable output
  ✅ Upload page working (dropzone + file list UI)
  ✅ API client skeleton (axios + TypeScript types)
  ✅ Push to feat/frontend

Panes:
  ✅ FastAPI boilerplate live
  ✅ POST /api/upload endpoint working
  ✅ PDF text extraction working with PyMuPDF
  ✅ Push to feat/backend

Julie:
  ✅ AMD Developer Cloud connected + tested
  ✅ Llama 3.2 Vision API call working
  ✅ Basic embedding generation on AMD confirmed
  ✅ Push to feat/ai

Mica:
  ✅ Supabase tables created (sessions, documents)
  ✅ GitHub Actions CI/CD configured
  ✅ Sample documents finalized (5 procurement docs)
  ✅ Post Day 1 Build in Public (X + LinkedIn)

MILESTONE: Repo live, frontend shell, basic upload works
```

---

## DAY 2 — July 7

```
Rhenmart:
  ✅ Connect upload UI to backend API
  ✅ File processing states (skeleton loaders)
  ✅ Dashboard page layout built (4 card grid)

Panes:
  ✅ OCR pipeline (pytesseract) working on images
  ✅ Text chunker service (512 token chunks)
  ✅ ChromaDB integration — store + retrieve chunks
  ✅ POST /api/analyze skeleton

Julie:
  ✅ Embedding service on AMD ROCm working
  ✅ Basic RAG query: question → retrieve → LLM → answer
  ✅ POST /api/chat v1 working
  ✅ Response format enforced (Answer/Evidence/Risk/Rec)

Mica:
  ✅ End-to-end test: upload PDF → extract → embed → query
  ✅ Document all bugs in GitHub Issues
  ✅ ReportLab PDF template started

MILESTONE: Upload → Parse → Embed → Basic Q&A working
```

---

## DAY 3 — July 8

```
Rhenmart:
  ✅ Chat interface fully built (Framer Motion animations)
  ✅ AI thinking animation (hexagonal avatar + pulsing dots)
  ✅ Text streaming simulation (word by word)
  ✅ Evidence tag components

Panes:
  ✅ Conflict detection engine v1 (POST /api/compare)
  ✅ Cross-document comparison logic
  ✅ POST /api/analyze complete (all 4 analysis types)
  ✅ Session management working

Julie:
  ✅ Executive summary prompt tuned
  ✅ Risk analysis prompt tuned
  ✅ Conflict detection prompt done
  ✅ Multi-document reasoning working

Mica:
  ✅ Full test with real procurement docs
  ✅ List all hallucinations or errors
  ✅ PDF export endpoint v1 (POST /api/report)
  ✅ Post Day 3 Build in Public (show pipeline working)

MILESTONE: Full analysis pipeline end-to-end working
```

---

## DAY 4 — July 9

```
Rhenmart:
  ✅ Connect dashboard to backend (real data)
  ✅ Conflict alert banner (red, visually striking)
  ✅ Comparison matrix table (color-coded winners)
  ✅ Mobile responsive check

Panes:
  ✅ PDF report endpoint complete
  ✅ Performance optimization (async processing)
  ✅ Error handling on all endpoints
  ✅ Run AMD BENCHMARK TEST ← CRITICAL TODAY

Julie:
  ✅ Multi-doc reasoning polished
  ✅ Evidence citations accurate (filename tags)
  ✅ Edge cases handled (bad OCR, empty docs)
  ✅ Record benchmark results

Mica:
  ✅ Full regression test all features
  ✅ Document AMD benchmark numbers
  ✅ Update slide deck with benchmark slide
  ✅ Post Day 4 Build in Public (show conflict detection)

MILESTONE: Everything connected + benchmark numbers ready
```

---

## DAY 5 — July 10

```
Rhenmart:
  ✅ UI final polish (spacing, micro-interactions)
  ✅ Demo page (/demo) with pre-loaded mock data
  ✅ AMD badge updated with real benchmark number
  ✅ Record demo video (scripted, 3-5 mins)

Panes:
  ✅ Deploy backend to Railway.app
  ✅ Environment variables secured (.env)
  ✅ CORS configured for Vercel domain
  ✅ Load test — can handle 5 simultaneous users

Julie:
  ✅ Final prompt tuning based on test results
  ✅ Review demo video for AI accuracy
  ✅ Fallback to Claude API confirmed working

Mica:
  ✅ Slide deck finalized (10 slides)
  ✅ Project description written (short + long)
  ✅ Deploy frontend to Vercel
  ✅ Full end-to-end test on deployed version

MILESTONE: Live on Vercel + Railway, demo video done
```

---

## DAY 6 — July 11 🚨 SUBMIT DAY

```
Morning:
  ✅ Final bug fixes only (no new features)
  ✅ Test on deployed Vercel URL
  ✅ Verify /demo page works without login

Afternoon:
  ✅ Submit on lablab.ai (submit EARLY — before 6PM PST)
  ✅ Fill all fields:
      - Project title: DealFlow AI
      - Short description (ready)
      - Long description (ready)
      - GitHub URL (public)
      - Demo video URL
      - App URL (Vercel link)
      - Track: Vision & Multimodal AI (Track 3)
      - Technology tags: AMD, ROCm, FastAPI, Next.js, RAG

After submit:
  ✅ Post final Build in Public tweet with demo video
  ✅ Tag @lablab @AIatAMD
  ✅ Share in Filipino dev communities

HARD DEADLINE: July 11 — 11:00 PM Philippine Standard Time
```

---

# 🎬 SECTION 11: DEMO VIDEO SCRIPT

## Full Script (3 minutes 30 seconds)

### OPENING — 0:00 to 0:15
```
[DealFlow AI logo fades in on dark background]
[AMD x lablab.ai badge appears]

VO: "Business decisions move at the speed of data.
     But most teams are still reading documents manually."
```

### PROBLEM — 0:15 to 0:35
```
[Show messy folder of PDF files]

VO: "A procurement manager receives four supplier quotations,
     an existing contract, and last month's invoice.
     She needs a decision by end of day.
     Manually? That's four hours of work."
```

### SOLUTION INTRO — 0:35 to 0:50
```
[DealFlow AI interface appears]

VO: "DealFlow AI is an AMD-accelerated document intelligence
     platform. Upload any business document. Ask anything.
     Get evidence-based decisions — in under 60 seconds."
```

### LIVE DEMO — 0:50 to 2:20
```
[Upload 4 documents — show drag and drop]
VO: "She drops in her documents."

[Processing animation — "AMD MI300X processing..."]
VO: "AMD Instinct MI300X processes all files simultaneously —
     multimodal analysis across PDFs and scanned images."

[Dashboard appears — Executive Summary]
VO: "Instant executive summary."

[Risk panel]
VO: "Risks, automatically flagged and categorized."

[CONFLICT ALERT BANNER slides in — red]
VO: "And here — DealFlow AI detected a conflict."

[Show conflict detail]
VO: "The existing invoice shows $48,500 — but the supplier's
     current quotation says $45,200. A $3,300 discrepancy
     a human might miss under time pressure."

[Comparison matrix]
VO: "Side-by-side comparison across all suppliers."

[Chat — ask "Which supplier should I choose?"]
VO: "She asks the question."

[Response streams in with evidence tags]
VO: "Every answer — backed by exact evidence from the
     documents. Source-cited. Verifiable. Trustworthy."

[PDF export button click]
VO: "One click — a boardroom-ready PDF report."
```

### AMD SLIDE — 2:20 to 2:40
```
[Show benchmark graphic — CPU vs AMD MI300X]

VO: "DealFlow AI runs on AMD Instinct MI300X via
     AMD Developer Cloud. Our embedding and inference
     pipeline is [Xx] faster than CPU-based alternatives.
     Enterprise speed. Real infrastructure. AMD."
```

### TEAM + CLOSING — 2:40 to 3:00
```
[Team slide — 4 photos]

VO: "Built by four Filipino junior developers in six days.
     No senior engineers. No big tech backing.
     Just execution — on AMD."

[DealFlow AI logo]
VO: "DealFlow AI. Your documents. Your decisions. Accelerated."

[lablab.ai + AMD logos]
```

---

# 🏆 SECTION 12: SLIDE DECK (10 SLIDES)

```
Slide 1:  Cover
          DealFlow AI logo + tagline
          "AMD Developer Hackathon: ACT II"
          Team names

Slide 2:  The Problem
          Procurement manager story
          "4 hours → 60 seconds"
          Visual: messy folder of docs

Slide 3:  Our Solution
          What DealFlow AI does (3 bullets max)
          Screenshot of dashboard

Slide 4:  Live Demo
          Best screenshot of product
          Show conflict detection prominently

Slide 5:  The Conflict Detection Engine
          The killer feature
          Side-by-side conflict card visual
          "The feature that prevents costly mistakes"

Slide 6:  AMD Integration
          Architecture diagram
          BENCHMARK: "[X]x faster on AMD MI300X"
          ROCm + MI300X + Llama 3.2 Vision

Slide 7:  Tech Stack
          Clean stack diagram
          Track 3: Vision & Multimodal AI

Slide 8:  Business Value
          Market: "50M+ SMEs globally"
          Cost: "Replaces $300+/month BI tools"
          Time: "Saves 4+ hours per procurement decision"
          Roadmap: "Phase 2 — SAP, MS365, Google Workspace integrations"

Slide 9:  The Team
          4 photos, names, roles
          "Four Filipino junior developers. Taguig, Philippines."
          "International stage. Full send. 🇵🇭"

Slide 10: Thank You
          Live demo URL
          GitHub URL
          "Try it now — no upload needed → /demo"
```

---

# ⚠️ SECTION 13: RISK MITIGATION

| Risk | Probability | Mitigation |
|------|------------|------------|
| AMD cloud setup delay | Medium | Set up Day 1, Claude API as fallback |
| OCR bad quality | Medium | Use clean PDFs for demo docs |
| Scope creep | High | MAXIMUM 5 features — cut anything else |
| Team coordination | Medium | Daily 15-min standup 9PM on Discord |
| Deploy fails Day 6 | Low | Deploy and test Day 5 |
| AMD credits run out | Low | $400 total ($100 x 4), use sparingly in dev |
| Conflict detection inaccurate | Medium | Tune prompts Day 3-4, test with real docs |
| Video recording bad quality | Low | Script ready, record Day 5 with time buffer |

---

# 🔧 SECTION 14: ENVIRONMENT VARIABLES

```env
# .env.example — commit this, never commit .env

# AMD Developer Cloud
AMD_CLOUD_API_KEY=your_key_here
AMD_CLOUD_ENDPOINT=https://api.amd-developer-cloud.com/v1
AMD_MODEL_ID=llama-3.2-vision-11b

# Fallback LLM
ANTHROPIC_API_KEY=your_key_here

# Supabase
SUPABASE_URL=your_url_here
SUPABASE_ANON_KEY=your_key_here

# App
SECRET_KEY=generate_random_string
ENVIRONMENT=development
MAX_FILE_SIZE_MB=10
MAX_FILES_PER_SESSION=10

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=DealFlow AI
NEXT_PUBLIC_AMD_BENCHMARK=5.6x  # Update after Day 4 test
```

---

# 📣 SECTION 15: BUILD IN PUBLIC POSTS

## Post Templates (copy-paste ready)

### Day 1 Post
```
Just kicked off @DealFlowAI for the @lablab + @AIatAMD
Developer Hackathon ACT II 🔥

Team of 4 Filipino junior devs building enterprise
document intelligence on AMD MI300X.

Day 1: architecture locked, repo live, first API call ⚡

Watch us ship. 🇵🇭
#AMDHackathon #BuildInPublic #lablab
```

### Day 3 Post
```
Day 3 update — DealFlow AI conflict detection is LIVE 🚨

Uploaded a supplier contract + invoice.
AI caught a $3,300 price discrepancy automatically.

This is what AMD-accelerated multimodal analysis looks like.

[attach screen recording]

@AIatAMD @lablab
#AMDHackathon #BuildInPublic
```

### Day 5 Post
```
Day 5. DealFlow AI is deployed. 🚀

✅ Multi-document upload
✅ AMD MI300X embeddings ([X]x faster than CPU)
✅ Conflict detection engine
✅ AI Decision Copilot with evidence citations
✅ One-click PDF reports

4 Filipino devs. 5 days. Enterprise AI.

Live demo: [vercel link]
@AIatAMD @lablab
#AMDHackathon
```

### Submission Day Post
```
We shipped. ✅

DealFlow AI — AMD-accelerated enterprise document
intelligence. Built in 6 days by 4 Filipino junior
developers from Taguig.

"Your documents speak. We translate them into decisions."

Try it: [demo link]
GitHub: [repo link]

@AIatAMD @lablab
🇵🇭 #AMDHackathon #DealFlowAI
```

---

# 💬 SECTION 16: KIRO INSTRUCTIONS

When Kiro works on this project:

1. Always follow the folder structure in Section 5
2. TypeScript strict mode on frontend (no `any` types)
3. Pydantic models for all FastAPI schemas
4. Every AI response follows Answer/Evidence/Risk/Recommendation
5. Never hardcode API keys — always use environment variables
6. Loading states on all async operations
7. Mobile-responsive by default (Tailwind responsive classes)
8. Comment all AMD-specific code: `# AMD: [explanation]`
9. New feature = new test file in backend/tests/
10. Git commits: `feat:` `fix:` `docs:` `style:` `test:`
11. Prioritize: Working > Perfect (6-day timeline)
12. Demo mode (/demo) must always work — never break this page

---

# 📊 SECTION 17: PROJECT SUBMISSION CHECKLIST

## lablab.ai Submission Fields
```
Project Title:        DealFlow AI
Short Description:    AMD-accelerated enterprise document intelligence
                      platform. Upload business documents, ask anything
                      in plain language, get evidence-based decisions
                      with source citations — in under 60 seconds.

Long Description:     [Full project description — 300-500 words]

Track:                Track 3: Vision & Multimodal AI

Technology Tags:      AMD, ROCm, AMD MI300X, FastAPI, Next.js,
                      RAG, LangChain, Llama 3.2 Vision, ChromaDB,
                      Supabase, Vercel, Railway

GitHub URL:           https://github.com/[team]/dealflow-ai
Demo URL:             https://dealflow-ai.vercel.app/demo
Video URL:            [YouTube or Loom link]
Cover Image:          Dark corporate screenshot of dashboard
```

## Final Checklist Before Submit
```
□ GitHub repo is PUBLIC
□ README.md is polished (Section in this doc)
□ Demo video uploaded (YouTube/Loom)
□ /demo page works without login
□ All env vars working on deployed version
□ AMD benchmark number confirmed and added everywhere
□ Slide deck PDF ready
□ Build in Public posts done (X + LinkedIn)
□ All 4 team members credited in submission
□ Submit before 11PM PST July 11 ← NON-NEGOTIABLE
```

---

*DealFlow AI — Master Plan v2.0*
*AMD Developer Hackathon: ACT II*
*🇵🇭 Rhenmart · Julie · Mica · Panes*
*Filipino Junior Developers. International Stage. Full Send.*
