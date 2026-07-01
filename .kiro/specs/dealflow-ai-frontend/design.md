# Design Document: DealFlow AI Frontend

## Overview

### Product Identity
DealFlow AI is an AMD-accelerated enterprise document intelligence platform designed to help business professionals analyze contracts, quotations, invoices, and procurement documents. The frontend application provides a Bloomberg Terminal-style dark interface with four primary experiences: document upload, AI-powered analysis dashboard, decision copilot chat interface, and a pre-loaded demo mode for instant evaluation.

### Target Audience
Enterprise users including procurement managers, operations teams, and business decision-makers who need to quickly analyze multiple business documents, detect conflicts, and receive evidence-based recommendations under time pressure.

### Core Value Proposition
Transforms hours of manual document review into a 60-second AI-powered analysis experience, featuring automatic conflict detection across documents, evidence-cited responses, and risk categorization—all accelerated by AMD MI300X infrastructure.

### Technology Foundation
- **Framework**: Next.js 14 (App Router) with React 18
- **Styling**: Tailwind CSS with custom dark corporate theme
- **Component Library**: shadcn/ui for base components
- **Icons**: Google Material Symbols (outlined) via CDN — `material-symbols` font. No emoji characters used anywhere in the UI.
- **State Management**: Zustand for global state
- **Animation**: Framer Motion for complex animations
- **API Communication**: Axios for HTTP requests with TypeScript type safety
- **Deployment**: Vercel (optimized for Next.js)

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER                                  │
│                   (Desktop / Tablet / Mobile)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS / REST API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                  NEXT.JS 14 FRONTEND                            │
│                     (App Router)                                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    APP LAYER                              │  │
│  │  /              → Landing + Upload                        │  │
│  │  /dashboard     → Analysis Dashboard                      │  │
│  │  /chat          → Decision Copilot                        │  │
│  │  /demo          → Pre-loaded Demo                         │  │
│  │  layout.tsx     → Shared layout + navigation              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐  │
│  │               COMPONENT LAYER                              │  │
│  │  upload/   → DropZone, FileList, ProcessingState         │  │
│  │  dashboard/→ ExecutiveSummary, RiskPanel, ConflictAlert  │  │
│  │  chat/     → ChatInterface, MessageBubble, EvidenceTag   │  │
│  │  shared/   → AMDBadge, RiskBadge, Navigation             │  │
│  │  ui/       → shadcn/ui primitives (Button, Card, etc.)   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐  │
│  │                  SERVICE LAYER                             │  │
│  │  api.ts          → API client (Axios + TypeScript)        │  │
│  │  mock-data.ts    → Demo mode + development mocks          │  │
│  │  session-store.ts→ Zustand store (session state)          │  │
│  │  types.ts        → TypeScript definitions                 │  │
│  │  utils.ts        → Formatting, validation helpers         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API Calls
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    FASTAPI BACKEND                              │
│               (Python 3.11 on Railway.app)                      │
│                                                                  │
│  POST /api/upload    → Document ingestion                       │
│  POST /api/analyze   → Full analysis generation                 │
│  POST /api/chat      → RAG-powered Q&A                          │
│  POST /api/report    → PDF export                               │
│  GET  /api/demo      → Pre-loaded sample data                   │
│                                                                  │
│  Document Pipeline: PyMuPDF → pytesseract → embeddings          │
│  AI Services: AMD Cloud (Llama 3.2 Vision) + Claude fallback   │
│  Vector Store: ChromaDB (in-memory per session)                 │
│  Conflict Engine: Cross-document comparison logic               │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

**1. Document Upload Flow**
```
User drags files → DropZone validates → POST /api/upload → Backend returns session_id
→ Store session in Zustand → Display processing states → Poll for completion
→ Enable "Analyze Documents" button → User clicks → Trigger analysis
```

**2. Analysis Flow**
```
User clicks "Analyze" → POST /api/analyze with session_id → Backend processes
→ Frontend displays skeleton loaders → Poll for completion → Receive analysis JSON
→ Parse into structured data → Render 4 analysis cards + conflict banner (if applicable)
→ Store in session state → Enable navigation to chat
```

**3. Chat Flow**
```
User enters question → POST /api/chat with question + session_id → Backend RAG query
→ Frontend displays AI thinking animation → Receive structured response
→ Stream text word-by-word (simulated) → Fade in sections sequentially
→ Render evidence tags as clickable pills → Store message in conversation history
```

**4. Demo Mode Flow**
```
User navigates to /demo → GET /api/demo → Backend returns pre-loaded mock data
→ Render dashboard with sample analysis → Pre-seed 2-3 chat messages
→ Enable full interaction with simulated data → No actual file processing
```

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         VERCEL CDN                              │
│  - Static assets (JS, CSS, images)                             │
│  - Edge functions for SSR pages                                 │
│  - Automatic HTTPS + domain                                     │
│  - Preview deployments per git branch                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Proxy
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     RAILWAY.APP                                 │
│  - FastAPI backend container                                    │
│  - Environment variables (AMD API keys)                         │
│  - Auto-scaling + health checks                                 │
│  - CORS configured for Vercel domain                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Metadata only
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        SUPABASE                                 │
│  - Session metadata (timestamps, user logs)                     │
│  - NOT storing actual documents                                 │
│  - Future: user authentication                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components and Interfaces

### Component Hierarchy

```
App
├── layout.tsx (Navigation, AMD Badge, Global Providers)
├── page.tsx (Landing / Upload)
│   ├── Navigation
│   ├── HeroSection
│   ├── DropZone
│   │   ├── FileUploadIcon
│   │   └── FileList
│   │       └── FileItem (with ProcessingState)
│   ├── TrustBanner
│   └── HowItWorksSection
├── dashboard/page.tsx
│   ├── DocumentSidebar
│   │   ├── DocumentList
│   │   │   └── DocumentItem
│   │   ├── AMDBadge
│   │   └── SessionActions
│   ├── DashboardTopBar
│   ├── ConflictAlertBanner (conditional)
│   │   └── ConflictCard[]
│   └── AnalysisGrid
│       ├── ExecutiveSummaryCard
│       ├── RiskAnalysisCard
│       │   └── RiskItem (with RiskBadge)
│       ├── ComparisonMatrixCard
│       │   └── ComparisonTable
│       └── RecommendationCard
├── chat/page.tsx
│   ├── ChatLayout
│   │   ├── DocumentContextPanel
│   │   │   ├── ActiveDocumentsList
│   │   │   └── QuickQuestionChips
│   │   └── ChatInterface
│   │       ├── ChatHeader
│   │       ├── MessageList
│   │       │   ├── UserMessage
│   │       │   └── AIMessage
│   │       │       ├── AIAvatar (with thinking animation)
│   │       │       ├── AnswerSection
│   │       │       ├── EvidenceSection
│   │       │       │   └── EvidenceTag[]
│   │       │       ├── RiskSection
│   │       │       └── RecommendationSection
│   │       └── ChatInputArea
│   │           ├── TextInput
│   │           └── SendButton
└── demo/page.tsx
    ├── DemoBanner
    └── (Reuses dashboard + chat components with mock data)
```

### Core Components

#### 1. DropZone Component
```typescript
interface DropZoneProps {
  onFilesAccepted: (files: File[]) => void;
  maxFiles: number;
  maxFileSizeMB: number;
  acceptedFormats: string[];
}

interface DropZoneState {
  isDragActive: boolean;
  uploadedFiles: UploadedFile[];
  isProcessing: boolean;
  errors: FileError[];
}

// Key Behaviors:
// - Validates file types (PDF, PNG, JPG, JPEG)
// - Enforces 10 file limit and 10MB per file
// - Visual feedback on drag-over (border blue glow)
// - Displays processing state per file
// - Shows "Analyze Documents" button when ready
```

#### 2. ConflictAlertBanner Component
```typescript
interface ConflictAlertBannerProps {
  conflicts: Conflict[];
  isExpanded: boolean;
  onToggle: () => void;
}

interface Conflict {
  type: string;
  documentA: { name: string; excerpt: string };
  documentB: { name: string; excerpt: string };
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  explanation: string;
  recommendedAction: string;
}

// Key Behaviors:
// - Slides down from top with bounce animation
// - Red color scheme for high visibility
// - Expandable to show detailed conflict cards
// - Side-by-side comparison boxes
// - Risk severity badges
```

#### 3. ChatInterface Component
```typescript
interface ChatInterfaceProps {
  sessionId: string;
  documents: Document[];
  onExportPDF: () => void;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  structuredResponse?: StructuredAIResponse;
  timestamp: Date;
  isStreaming?: boolean;
}

interface StructuredAIResponse {
  answer: string;
  evidence: Evidence[];
  risks: string;
  recommendation: string;
}

interface Evidence {
  quote: string;
  sourceDocument: string;
  documentType: 'pdf' | 'image';
}

// Key Behaviors:
// - AI thinking animation (hexagonal avatar + pulsing ring)
// - Word-by-word text streaming simulation
// - Sequential section reveal (Answer → Evidence → Risk → Rec)
// - Clickable evidence tags
// - Quick question chips for instant queries
```

#### 4. AIThinkingAnimation Component
```typescript
interface AIThinkingAnimationProps {
  isThinking: boolean;
}

// Key Behaviors:
// - Hexagonal avatar (not circular — more technical feel)
// - Pulsing blue ring animation around avatar (keyframe: opacity 1→0.3→1, scale 1→1.2→1, 1.5s infinite)
// - Three-dot wave animation with blue glow (#3B7BF6)
// - "Processing with AMD MI300X..." label in #8B9CC8, Inter 400 — no icons, no emoji
// - Smooth fade-in/fade-out on mount/unmount (300ms opacity transition)
// - respects prefers-reduced-motion: disables pulse and wave, shows static state
```

#### 5. EvidenceTag Component
```typescript
interface EvidenceTagProps {
  documentName: string;
  documentType: 'pdf' | 'image';
  onClick: () => void;
}

// Key Behaviors:
// - Pill-shaped clickable element
// - Google Material Symbol icon: `description` + filename in JetBrains Mono
// - Color-coded by type: PDF uses `picture_as_pdf` icon in #EF4444, Image uses `image` icon in #3B7BF6
// - Hover state: border transitions to #3B7BF6 within 150ms
// - Click state: scales to 0.97 for 100ms then returns to 1.0
// - aria-label set to "Source: [documentName]" for screen readers
```

#### 6. RiskBadge Component
```typescript
interface RiskBadgeProps {
  level: 'HIGH' | 'MEDIUM' | 'LOW';
}

// Styling:
// HIGH:   red (#EF4444) with rgba(239,68,68,0.15) bg
// MEDIUM: amber (#F59E0B) with rgba(245,158,11,0.15) bg  
// LOW:    green (#10B981) with rgba(16,185,129,0.15) bg
```

#### 7. ComparisonMatrix Component
```typescript
interface ComparisonMatrixProps {
  data: ComparisonRow[];
}

interface ComparisonRow {
  field: string;
  values: { [documentId: string]: string };
  winner?: string; // documentId of best option
}

// Key Behaviors:
// - Data table with alternating row backgrounds
// - Highlight winner cells in green
// - Highlight loser cells in red (if applicable)
// - Responsive: horizontal scroll on mobile
```

#### 8. AMDBadge Component
```typescript
interface AMDBadgeProps {
  variant: 'navigation' | 'sidebar' | 'card' | 'inline';
  showBenchmark?: boolean;
  benchmarkValue?: string;
}

// Styling:
// - AMD red accent (#ED1C24)
// - Google Material Symbol icon: `bolt` (aria-hidden="true")
// - "Powered by AMD MI300X" text in Inter 500
// - Optional benchmark display: "5.6x faster"
// - No emoji characters
```

### Shared UI Components (shadcn/ui)

```typescript
// Base components from shadcn/ui library:
- Button (with variants: default, outline, ghost, destructive)
- Card, CardHeader, CardTitle, CardContent
- Input, Textarea
- Badge
- Separator
- Skeleton (for loading states)
- Dialog, Sheet (for modals/sidebars)
- DropdownMenu
- Tooltip
```

---

## Data Models

### TypeScript Type Definitions

```typescript
// lib/types.ts

// ==================== DOCUMENTS ====================

export interface Document {
  id: string;
  filename: string;
  fileType: 'pdf' | 'image';
  fileSize: number; // bytes
  pageCount?: number;
  dimensions?: { width: number; height: number };
  uploadedAt: Date;
  processingStatus: ProcessingStatus;
}

export type ProcessingStatus = 
  | 'uploading'
  | 'uploaded'
  | 'extracting_text'
  | 'running_ocr'
  | 'generating_embeddings'
  | 'indexing'
  | 'completed'
  | 'failed';

export interface ProcessingStep {
  step: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  timestamp?: Date;
}

// ==================== SESSION ====================

export interface Session {
  sessionId: string;
  documents: Document[];
  createdAt: Date;
  lastUpdatedAt: Date;
  analysisStatus: 'not_started' | 'analyzing' | 'completed' | 'failed';
  analysis?: AnalysisResult;
}

// ==================== ANALYSIS ====================

export interface AnalysisResult {
  sessionId: string;
  analyzedAt: Date;
  executiveSummary: string;
  risks: Risk[];
  comparisonMatrix: ComparisonRow[];
  conflicts: Conflict[];
  recommendation: Recommendation;
  metadata: {
    processingTimeMs: number;
    documentsAnalyzed: number;
    amdAccelerated: boolean;
  };
}

export interface Risk {
  id: string;
  level: 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  sourceDocument: string;
  category?: string;
}

export interface ComparisonRow {
  field: string;
  values: { [documentId: string]: string };
  winner?: string;
  explanation?: string;
}

export interface Conflict {
  id: string;
  type: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  documentA: {
    id: string;
    name: string;
    excerpt: string;
  };
  documentB: {
    id: string;
    name: string;
    excerpt: string;
  };
  explanation: string;
  recommendedAction: string;
}

export interface Recommendation {
  title: string;
  summary: string;
  reasoning: string;
  nextSteps: string[];
  confidence: number; // 0-1
}

// ==================== CHAT ====================

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  structuredResponse?: StructuredAIResponse;
  timestamp: Date;
  isStreaming?: boolean;
}

export interface StructuredAIResponse {
  answer: string;
  evidence: Evidence[];
  risks: string;
  recommendation: string;
}

export interface Evidence {
  quote: string;
  sourceDocument: string;
  documentType: 'pdf' | 'image';
  pageNumber?: number;
}

export interface ChatState {
  sessionId: string;
  messages: ChatMessage[];
  isAIThinking: boolean;
  activeDocuments: Document[];
}

// ==================== API RESPONSES ====================

export interface UploadResponse {
  sessionId: string;
  documents: Document[];
  message: string;
}

export interface AnalyzeResponse {
  sessionId: string;
  status: 'processing' | 'completed';
  analysis?: AnalysisResult;
  estimatedTimeSeconds?: number;
}

export interface ChatResponse {
  messageId: string;
  role: 'assistant';
  structuredResponse: StructuredAIResponse;
  processingTimeMs: number;
}

export interface ErrorResponse {
  error: string;
  code: string;
  details?: any;
}

// ==================== DEMO MODE ====================

export interface DemoData {
  sessionId: string;
  documents: Document[];
  analysis: AnalysisResult;
  preSeededMessages: ChatMessage[];
}
```

---

## API Contracts

### API Client Architecture

```typescript
// lib/api.ts

import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class DealFlowAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 60000, // 60 seconds
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for auth (future)
    this.client.interceptors.request.use((config) => {
      // Add auth token when implemented
      return config;
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        // Handle common errors
        if (error.response?.status === 401) {
          // Handle unauthorized
        }
        return Promise.reject(error);
      }
    );
  }

  // ... API methods below
}

export const api = new DealFlowAPI();
```

### Endpoint Specifications

#### 1. Upload Documents
```typescript
/**
 * POST /api/upload
 * Upload business documents for analysis
 */
async uploadDocuments(files: File[]): Promise<UploadResponse> {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file);
  });

  const response = await this.client.post<UploadResponse>(
    '/api/upload',
    formData,
    {
      headers: { 'Content-Type': 'multipart/form-data' },
    }
  );

  return response.data;
}

// Request:
// - Content-Type: multipart/form-data
// - Body: FormData with 'files' array
// - Max 10 files, each max 10MB
// - Supported: PDF, PNG, JPG, JPEG

// Response:
{
  "sessionId": "uuid-v4-string",
  "documents": [
    {
      "id": "doc-uuid",
      "filename": "Contract_A.pdf",
      "fileType": "pdf",
      "fileSize": 2048576,
      "pageCount": 12,
      "uploadedAt": "2026-07-06T14:30:00Z",
      "processingStatus": "uploaded"
    }
  ],
  "message": "5 documents uploaded successfully"
}

// Error Response (400):
{
  "error": "File size exceeds 10MB limit",
  "code": "FILE_SIZE_EXCEEDED",
  "details": {
    "filename": "large_file.pdf",
    "size": 15728640,
    "maxSize": 10485760
  }
}
```

#### 2. Analyze Documents
```typescript
/**
 * POST /api/analyze
 * Generate comprehensive analysis for uploaded documents
 */
async analyzeDocuments(sessionId: string): Promise<AnalyzeResponse> {
  const response = await this.client.post<AnalyzeResponse>(
    '/api/analyze',
    { sessionId }
  );

  return response.data;
}

// Request:
{
  "sessionId": "uuid-v4-string"
}

// Response (Initial):
{
  "sessionId": "uuid-v4-string",
  "status": "processing",
  "estimatedTimeSeconds": 45
}

// Response (Completed - poll for this):
{
  "sessionId": "uuid-v4-string",
  "status": "completed",
  "analysis": {
    "sessionId": "uuid-v4-string",
    "analyzedAt": "2026-07-06T14:31:15Z",
    "executiveSummary": "Analysis summary text...",
    "risks": [
      {
        "id": "risk-1",
        "level": "HIGH",
        "description": "Price discrepancy detected...",
        "sourceDocument": "Invoice_March.pdf",
        "category": "Financial"
      }
    ],
    "comparisonMatrix": [
      {
        "field": "Total Price",
        "values": {
          "doc-1": "$45,200",
          "doc-2": "$42,800"
        },
        "winner": "doc-2",
        "explanation": "Lower cost"
      }
    ],
    "conflicts": [
      {
        "id": "conflict-1",
        "type": "PRICE_DISCREPANCY",
        "severity": "HIGH",
        "documentA": {
          "id": "doc-1",
          "name": "Invoice_March.pdf",
          "excerpt": "Total amount due: $48,500.00"
        },
        "documentB": {
          "id": "doc-2",
          "name": "Quotation_A.pdf",
          "excerpt": "Total quotation value: $45,200.00"
        },
        "explanation": "$3,300 discrepancy detected",
        "recommendedAction": "Request clarification before proceeding"
      }
    ],
    "recommendation": {
      "title": "Proceed with Supplier B",
      "summary": "Lower cost and better terms",
      "reasoning": "Supplier B offers...",
      "nextSteps": [
        "Clarify TechCorp pricing discrepancy",
        "Request formal proposal from Supplier B"
      ],
      "confidence": 0.85
    },
    "metadata": {
      "processingTimeMs": 8500,
      "documentsAnalyzed": 5,
      "amdAccelerated": true
    }
  }
}
```

#### 3. Chat with Decision Copilot
```typescript
/**
 * POST /api/chat
 * Ask questions about uploaded documents
 */
async sendChatMessage(
  sessionId: string,
  question: string
): Promise<ChatResponse> {
  const response = await this.client.post<ChatResponse>(
    '/api/chat',
    {
      sessionId,
      question,
    }
  );

  return response.data;
}

// Request:
{
  "sessionId": "uuid-v4-string",
  "question": "Which supplier should I choose?"
}

// Response:
{
  "messageId": "msg-uuid",
  "role": "assistant",
  "structuredResponse": {
    "answer": "Based on the uploaded documents, Supplier B is the recommended choice. They offer a lower total cost of $42,800 compared to Supplier A's $45,200, more flexible payment terms (60 days vs 30 days), extended warranty (2 years vs 1 year), and better support SLA (24 hours vs 48 hours).",
    "evidence": [
      {
        "quote": "Total quotation value: $42,800.00 | Payment terms: Net 60",
        "sourceDocument": "Supplier_B_Quotation.pdf",
        "documentType": "pdf",
        "pageNumber": 1
      },
      {
        "quote": "Total quotation value: $45,200.00 | Payment terms: Net 30",
        "sourceDocument": "Supplier_A_Quotation.pdf",
        "documentType": "pdf",
        "pageNumber": 1
      }
    ],
    "risks": "However, note that a price discrepancy exists between the existing TechCorp invoice ($48,500) and their current quotation ($45,200). This should be clarified before any contract renewal with TechCorp.",
    "recommendation": "Proceed with Supplier B. Request formal proposal and clarify the TechCorp pricing discrepancy regardless of final decision."
  },
  "processingTimeMs": 2400
}
```

#### 4. Export PDF Report
```typescript
/**
 * POST /api/report
 * Generate and download PDF report
 */
async exportReport(
  sessionId: string,
  includeChat: boolean = false
): Promise<Blob> {
  const response = await this.client.post(
    '/api/report',
    {
      sessionId,
      includeChat,
    },
    {
      responseType: 'blob',
    }
  );

  return response.data;
}

// Request:
{
  "sessionId": "uuid-v4-string",
  "includeChat": false
}

// Response:
// - Content-Type: application/pdf
// - Binary PDF data
// - Frontend triggers download: 
//   const blob = new Blob([data], { type: 'application/pdf' });
//   const url = window.URL.createObjectURL(blob);
//   const link = document.createElement('a');
//   link.href = url;
//   link.download = 'dealflow-analysis.pdf';
//   link.click();
```

#### 5. Demo Mode Data
```typescript
/**
 * GET /api/demo
 * Retrieve pre-loaded demo data
 */
async getDemoData(): Promise<DemoData> {
  const response = await this.client.get<DemoData>('/api/demo');
  return response.data;
}

// Response: Same structure as analyze response but with hardcoded sample data
// - 5 sample procurement documents
// - Pre-computed analysis with conflicts
// - 2-3 pre-seeded chat messages
```

### Error Handling Strategy

```typescript
// Centralized error handling

export class APIError extends Error {
  constructor(
    public code: string,
    public message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Error codes:
// - FILE_SIZE_EXCEEDED: File larger than 10MB
// - FILE_COUNT_EXCEEDED: More than 10 files
// - UNSUPPORTED_FORMAT: Not PDF/PNG/JPG/JPEG
// - UPLOAD_FAILED: Network or server error during upload
// - ANALYSIS_FAILED: Processing error during analysis
// - SESSION_NOT_FOUND: Invalid session ID
// - NETWORK_ERROR: Connection timeout or failed request

// Frontend error display:
// - Toast notifications for non-critical errors
// - Inline error messages for form validation
// - Full-page error state for critical failures
// - Retry buttons for recoverable errors
```

---

## Implementation Approach

### Development Phases

#### Phase 1: Foundation Setup (Day 1)
**Goal**: Project initialized with routing, styling, and basic structure

**Tasks**:
1. Initialize Next.js 14 project with TypeScript
2. Configure Tailwind CSS with custom theme
3. Install and configure shadcn/ui components
4. Set up Zustand store structure
5. Create routing structure (/, /dashboard, /chat, /demo)
6. Implement shared layout with navigation
7. Set up API client with Axios
8. Create TypeScript type definitions
9. Build AMDBadge component
10. Deploy to Vercel (initial deployment)

**Deliverables**:
- Functional Next.js app with navigation
- Dark corporate theme applied globally
- API client ready for integration
- Type-safe data models

#### Phase 2: Upload Experience (Day 1-2)
**Goal**: Fully functional document upload interface

**Tasks**:
1. Build DropZone component with react-dropzone
2. Implement file validation (format, size, count)
3. Create FileList component with processing states
4. Add drag-and-drop visual feedback
5. Connect to backend /api/upload endpoint
6. Display processing steps per file
7. Enable "Analyze Documents" button when ready
8. Add error handling for upload failures
9. Build Landing page hero section
10. Implement page load animations

**Deliverables**:
- Working drag-and-drop upload
- Real-time file processing feedback
- Error messages for invalid files
- Smooth animations and transitions

#### Phase 3: Dashboard Analysis (Day 2-3)
**Goal**: Complete analysis dashboard with all visualization components

**Tasks**:
1. Build DocumentSidebar component
2. Create ExecutiveSummaryCard component
3. Build RiskAnalysisCard with RiskBadge
4. Implement ComparisonMatrix component
5. Create RecommendationCard component
6. Build ConflictAlertBanner (expandable)
7. Connect to /api/analyze endpoint
8. Implement skeleton loading states
9. Add card entrance animations (staggered)
10. Build export to PDF functionality

**Deliverables**:
- Functional dashboard with all 4 analysis cards
- Conflict detection banner with visual prominence
- Loading states during analysis
- PDF export capability

#### Phase 4: Decision Copilot Chat (Day 3-4)
**Goal**: Interactive chat interface with AI animations

**Tasks**:
1. Build ChatInterface layout (split panel)
2. Create DocumentContextPanel with quick questions
3. Implement MessageBubble components (user + AI)
4. Build AIThinkingAnimation (hexagonal avatar + pulsing)
5. Create EvidenceTag component
6. Implement text streaming simulation
7. Add sequential section reveal (Answer → Evidence → Risk → Rec)
8. Connect to /api/chat endpoint
9. Build ChatInputArea with send button
10. Implement message history management

**Deliverables**:
- Fully functional chat interface
- Custom AI thinking animations
- Word-by-word streaming effect
- Evidence-cited responses with clickable tags

#### Phase 5: Demo Mode (Day 4-5)
**Goal**: Pre-loaded demonstration with sample data

**Tasks**:
1. Create mock data for 5 sample procurement documents
2. Generate realistic analysis with conflicts
3. Write 2-3 pre-seeded chat conversations
4. Build DemoBanner component
5. Connect to /api/demo endpoint
6. Reuse dashboard components with mock data
7. Enable full interaction with simulated responses
8. Add clear "Demo Mode" indicators throughout
9. Test all features in demo context
10. Create smooth transition to main app

**Deliverables**:
- Fully functional demo mode
- Realistic sample data
- No upload required for judges to evaluate
- Clear demo vs. production distinction

#### Phase 6: Polish & Optimization (Day 5-6)
**Goal**: Production-ready application with performance optimization

**Tasks**:
1. Responsive design testing (desktop, tablet, mobile)
2. Accessibility audit (keyboard navigation, ARIA labels)
3. Performance optimization (lazy loading, code splitting)
4. Error handling refinement
5. Animation polish and timing adjustments
6. Cross-browser testing
7. Final deployment to Vercel
8. Demo video recording
9. README documentation
10. Final QA testing

**Deliverables**:
- Mobile-responsive application
- Accessibility compliance
- Optimized performance
- Production deployment
- Demo video

### Technology Integration Details

#### AMD Branding Integration Points

1. **Navigation Bar**: "Powered by AMD MI300X" badge
2. **Landing Page**: Trust banner with AMD Instinct MI300X mention
3. **Dashboard Sidebar**: AMD badge at bottom
4. **Analysis Cards**: "Generated by AMD LLM" badge
5. **Chat Thinking State**: "Processing with AMD MI300X..." text
6. **Performance Stats**: Benchmark display (e.g., "5.6x faster")

#### Animation Strategy

**CSS Animations (Tailwind)**:
- Simple transitions (hover states, focus rings)
- Opacity fades
- Scale transforms

**Framer Motion (Complex Animations)**:
- Page transitions
- Staggered card reveals
- Chat message entrance
- Text streaming effect
- Conflict banner slide-down
- AI thinking pulse animation

**Animation Timing**:
```typescript
// Standard easing curves
const easings = {
  easeOut: [0.0, 0.0, 0.2, 1.0],
  easeInOut: [0.4, 0.0, 0.2, 1.0],
  bounce: [0.175, 0.885, 0.32, 1.275],
};

// Durations
const durations = {
  fast: 200,      // Micro-interactions
  medium: 300,    // Standard transitions
  slow: 500,      // Page loads
  verySlow: 1000, // Emphasis animations
};

// Delays for staggered animations
const stagger = {
  cards: 100,     // Between dashboard cards
  list: 50,       // Between list items
  sections: 200,  // Between major sections
};
```

#### State Management Architecture

```typescript
// session-store.ts (Zustand)

interface SessionStore {
  // Session state
  session: Session | null;
  documents: Document[];
  analysis: AnalysisResult | null;
  
  // Chat state
  messages: ChatMessage[];
  isAIThinking: boolean;
  
  // UI state
  isUploading: boolean;
  isAnalyzing: boolean;
  uploadProgress: { [fileId: string]: number };
  
  // Actions
  setSession: (session: Session) => void;
  addDocuments: (documents: Document[]) => void;
  updateDocumentStatus: (docId: string, status: ProcessingStatus) => void;
  setAnalysis: (analysis: AnalysisResult) => void;
  addMessage: (message: ChatMessage) => void;
  setAIThinking: (thinking: boolean) => void;
  clearSession: () => void;
}

// Usage in components:
const { session, addDocuments, setAnalysis } = useSessionStore();
```

#### API Mock Strategy (Development & Demo)

```typescript
// lib/mock-data.ts

export const USE_MOCK_API = process.env.NODE_ENV === 'development' 
  || window.location.pathname === '/demo';

export class MockAPI {
  // Simulate network delay
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  async uploadDocuments(files: File[]): Promise<UploadResponse> {
    await this.delay(1000);
    return MOCK_UPLOAD_RESPONSE;
  }
  
  async analyzeDocuments(sessionId: string): Promise<AnalyzeResponse> {
    await this.delay(3000); // Simulate processing time
    return MOCK_ANALYSIS_RESPONSE;
  }
  
  async sendChatMessage(
    sessionId: string,
    question: string
  ): Promise<ChatResponse> {
    await this.delay(800);
    return MOCK_CHAT_RESPONSES[question] || MOCK_DEFAULT_RESPONSE;
  }
}

// API client automatically uses mock in development
export const api = USE_MOCK_API ? new MockAPI() : new DealFlowAPI();
```

#### Responsive Design Strategy

**Breakpoints**:
```typescript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '375px',   // Mobile
      'md': '768px',   // Tablet
      'lg': '1024px',  // Laptop
      'xl': '1280px',  // Desktop
      '2xl': '1536px', // Large desktop
    },
  },
};
```

**Layout Adaptations**:
```
Desktop (1280px+):
  - Full two-column layouts
  - Sidebars at 280-320px
  - 2x2 card grids
  - Full-width comparison tables

Laptop (1024px):
  - Narrower sidebars (240px)
  - Tighter spacing
  - Same grid structure

Tablet (768px):
  - Sidebars collapse to icon-only
  - Expandable via hamburger menu
  - 2x2 grid becomes 1x4 stack
  - Horizontal scroll for tables

Mobile (375px+):
  - Single column layout
  - Bottom sheet navigation
  - Full-width cards
  - Chat takes full screen
  - Upload zone full width
  - Smaller typography scale
```

### Performance Optimization

**Code Splitting**:
```typescript
// Dynamic imports for heavy components
const ChatInterface = dynamic(() => import('@/components/chat/ChatInterface'));
const ComparisonMatrix = dynamic(() => import('@/components/dashboard/ComparisonMatrix'));
```

**Image Optimization**:
```typescript
// Use Next.js Image component for all images
import Image from 'next/image';

<Image
  src="/demo-docs/contract.png"
  alt="Contract thumbnail"
  width={120}
  height={160}
  loading="lazy"
/>
```

**API Caching**:
```typescript
// Cache analysis results in Zustand
// Avoid re-fetching on navigation
const cachedAnalysis = useSessionStore(state => state.analysis);
if (!cachedAnalysis) {
  // Fetch from API
}
```

**Font Loading**:
```typescript
// app/layout.tsx
import { DM_Sans, Inter, JetBrains_Mono } from 'next/font/google';

const dmSans = DM_Sans({ 
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-dm-sans',
  display: 'swap',
});

const inter = Inter({ 
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-inter',
  display: 'swap',
});

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-jetbrains',
  display: 'swap',
});
```

### Testing Strategy

**Unit Tests** (Example-based):
```typescript
// Example test: RiskBadge component
describe('RiskBadge', () => {
  it('renders HIGH severity with correct styling', () => {
    render(<RiskBadge level="HIGH" />);
    const badge = screen.getByText('HIGH');
    expect(badge).toHaveClass('text-red-500');
    expect(badge).toHaveStyle({ 
      backgroundColor: 'rgba(239, 68, 68, 0.15)' 
    });
  });
  
  it('renders MEDIUM severity with correct styling', () => {
    render(<RiskBadge level="MEDIUM" />);
    const badge = screen.getByText('MEDIUM');
    expect(badge).toHaveClass('text-amber-500');
  });
  
  it('renders LOW severity with correct styling', () => {
    render(<RiskBadge level="LOW" />);
    const badge = screen.getByText('LOW');
    expect(badge).toHaveClass('text-green-500');
  });
});

// Example test: File validation
describe('DropZone validation', () => {
  it('rejects files larger than 10MB', () => {
    const largeFile = new File(['x'.repeat(11 * 1024 * 1024)], 'large.pdf');
    const result = validateFile(largeFile);
    expect(result.isValid).toBe(false);
    expect(result.error).toBe('FILE_SIZE_EXCEEDED');
  });
  
  it('rejects unsupported file formats', () => {
    const docFile = new File(['content'], 'document.docx');
    const result = validateFile(docFile);
    expect(result.isValid).toBe(false);
    expect(result.error).toBe('UNSUPPORTED_FORMAT');
  });
  
  it('accepts valid PDF files', () => {
    const pdfFile = new File(['content'], 'contract.pdf', { 
      type: 'application/pdf' 
    });
    const result = validateFile(pdfFile);
    expect(result.isValid).toBe(true);
  });
});

// Example test: Evidence tag formatting
describe('EvidenceTag', () => {
  it('displays document name correctly', () => {
    render(
      <EvidenceTag 
        documentName="Contract_A.pdf" 
        documentType="pdf"
        onClick={() => {}}
      />
    );
    expect(screen.getByText('Contract_A.pdf')).toBeInTheDocument();
  });
  
  it('shows PDF icon for PDF documents', () => {
    render(
      <EvidenceTag 
        documentName="Contract_A.pdf" 
        documentType="pdf"
        onClick={() => {}}
      />
    );
    const icon = screen.getByTestId('document-icon');
    expect(icon).toHaveClass('pdf-icon');
  });
  
  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(
      <EvidenceTag 
        documentName="Contract_A.pdf" 
        documentType="pdf"
        onClick={handleClick}
      />
    );
    fireEvent.click(screen.getByText('Contract_A.pdf'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

**Integration Tests**:
```typescript
// Example test: Upload flow
describe('Document Upload Flow', () => {
  it('uploads files and displays processing states', async () => {
    render(<UploadPage />);
    
    const file = new File(['content'], 'contract.pdf', { 
      type: 'application/pdf' 
    });
    const dropzone = screen.getByTestId('drop-zone');
    
    // Simulate file drop
    fireEvent.drop(dropzone, {
      dataTransfer: { files: [file] },
    });
    
    // Verify file appears in list
    await waitFor(() => {
      expect(screen.getByText('contract.pdf')).toBeInTheDocument();
    });
    
    // Verify processing state
    expect(screen.getByText('uploading')).toBeInTheDocument();
    
    // Wait for completion
    await waitFor(() => {
      expect(screen.getByText('Processed ✓')).toBeInTheDocument();
    });
    
    // Verify analyze button is enabled
    const analyzeButton = screen.getByText('Analyze Documents');
    expect(analyzeButton).not.toBeDisabled();
  });
});

// Example test: Chat interaction
describe('Chat Interface', () => {
  it('sends question and displays AI response', async () => {
    render(<ChatPage />);
    
    const input = screen.getByPlaceholderText('Ask anything about your documents...');
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    // Type question
    fireEvent.change(input, { 
      target: { value: 'Which supplier should I choose?' } 
    });
    fireEvent.click(sendButton);
    
    // Verify user message appears
    await waitFor(() => {
      expect(screen.getByText('Which supplier should I choose?')).toBeInTheDocument();
    });
    
    // Verify AI thinking animation
    expect(screen.getByText('Processing with AMD MI300X...')).toBeInTheDocument();
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText(/ANSWER/i)).toBeInTheDocument();
      expect(screen.getByText(/EVIDENCE/i)).toBeInTheDocument();
      expect(screen.getByText(/RISK/i)).toBeInTheDocument();
      expect(screen.getByText(/RECOMMENDATION/i)).toBeInTheDocument();
    }, { timeout: 3000 });
  });
});
```

**E2E Tests** (Playwright):
```typescript
// Example test: Complete workflow
test('complete analysis workflow', async ({ page }) => {
  await page.goto('/');
  
  // Upload files
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles([
    'tests/fixtures/contract_a.pdf',
    'tests/fixtures/quotation_b.pdf',
  ]);
  
  // Wait for processing
  await page.waitForSelector('text=Processed ✓');
  
  // Click analyze
  await page.click('text=Analyze Documents');
  
  // Wait for analysis completion
  await page.waitForSelector('text=Executive Summary');
  
  // Verify conflict banner appears
  await expect(page.locator('text=Conflicts Detected')).toBeVisible();
  
  // Navigate to chat
  await page.click('text=Ask a Question');
  
  // Ask question
  await page.fill('input[placeholder*="Ask anything"]', 'What are the risks?');
  await page.click('button:has-text("Send")');
  
  // Verify AI response
  await expect(page.locator('text=ANSWER')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('[data-testid="evidence-tag"]')).toBeVisible();
});
```

### Error Handling

**Error Boundary**:
```typescript
// components/ErrorBoundary.tsx
export class ErrorBoundary extends React.Component<Props, State> {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
    // Send to error tracking service
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="error-state">
          <h2>Something went wrong</h2>
          <button onClick={() => window.location.reload()}>
            Reload application
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

**API Error Handling**:
```typescript
// Centralized error handler
function handleAPIError(error: any): never {
  if (error.response) {
    // Server responded with error
    const apiError = new APIError(
      error.response.data.code,
      error.response.data.error,
      error.response.data.details
    );
    
    // Display user-friendly message
    toast.error(apiError.message);
    throw apiError;
  } else if (error.request) {
    // Request made but no response
    const networkError = new APIError(
      'NETWORK_ERROR',
      'Unable to reach server. Please check your connection.',
    );
    toast.error(networkError.message);
    throw networkError;
  } else {
    // Unknown error
    toast.error('An unexpected error occurred');
    throw error;
  }
}
```

### Accessibility

**Keyboard Navigation**:
- All interactive elements accessible via Tab
- Upload zone: Enter to open file dialog
- Quick question chips: Enter/Space to select
- Chat input: Enter to send message
- Evidence tags: Enter to trigger onClick

**Screen Reader Support**:
```typescript
// Example: Chat message structure
<div
  role="article"
  aria-label={`Message from ${message.role}`}
  tabIndex={0}
>
  <div aria-live="polite">
    {message.isStreaming && (
      <span className="sr-only">AI is generating response</span>
    )}
    {message.content}
  </div>
</div>

// Example: Upload zone
<div
  role="button"
  aria-label="Drop files or click to upload"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter') openFileDialog();
  }}
>
  {/* Upload zone content */}
</div>
```

**Color Contrast**:
- Text primary (#F0F4FF) on background (#080D1A): 12.5:1 ✓
- Text secondary (#8B9CC8) on background (#080D1A): 7.2:1 ✓
- Accent blue (#3B7BF6) on background (#080D1A): 4.8:1 ✓
- All combinations exceed WCAG AA standards

**Focus Indicators**:
```css
/* Custom focus ring (more visible than default) */
.focus-visible:focus {
  outline: 2px solid #3B7BF6;
  outline-offset: 2px;
}
```

---

## Error Handling

### Client-Side Error Types

**1. Validation Errors** (User Input)
```typescript
interface ValidationError {
  field: string;
  message: string;
  code: 'REQUIRED' | 'INVALID_FORMAT' | 'OUT_OF_RANGE';
}

// Example: File validation
if (file.size > MAX_FILE_SIZE) {
  return {
    isValid: false,
    error: {
      field: 'file',
      message: `File size exceeds 10MB limit (${formatBytes(file.size)} provided)`,
      code: 'OUT_OF_RANGE',
    },
  };
}
```

**2. API Errors** (Server Response)
```typescript
// Handled by centralized error handler
// Displayed as toast notifications
// Logged to console in development
// Sent to error tracking in production
```

**3. Network Errors** (Connection Issues)
```typescript
// Automatic retry logic for transient failures
// User-friendly messaging: "Connection lost. Retrying..."
// Offline indicator in navigation bar
```

**4. Runtime Errors** (Unexpected Exceptions)
```typescript
// Caught by ErrorBoundary component
// Full-page error state with reload option
// Error details logged for debugging
```

### Error Recovery Strategies

**Upload Failures**:
- Automatic retry (up to 3 attempts)
- Clear error message with file name
- Option to remove failed file and continue
- Preserve successfully uploaded files

**Analysis Failures**:
- Retry button with progress indicator
- Fallback to partial results if available
- Option to return to upload and adjust documents

**Chat Failures**:
- Retry button on failed message
- Error message inline with conversation
- Preserve conversation history
- Suggest simplifying question

### User Feedback Patterns

**Success States**:
- Green checkmarks for completed steps
- Success toast notifications
- Smooth transitions to next step

**Loading States**:
- Skeleton loaders for content
- Progress bars for long operations
- Status text updates during processing
- Animated spinners for short waits

**Error States**:
- Red icons for failures
- Clear error messages with actionable guidance
- Retry buttons where applicable
- Support contact for critical errors

---

## Testing Strategy

### Test Coverage Goals

- **Unit Tests**: 80% coverage for components and utilities
- **Integration Tests**: All critical user flows
- **E2E Tests**: Happy path + error scenarios
- **Accessibility Tests**: Automated checks + manual testing
- **Visual Regression**: Snapshot tests for UI components

### Testing Tools

```json
{
  "devDependencies": {
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.4",
    "@testing-library/user-event": "^14.5.1",
    "@playwright/test": "^1.40.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0"
  }
}
```

### Test Organization

```
frontend/
├── __tests__/
│   ├── unit/
│   │   ├── components/
│   │   │   ├── RiskBadge.test.tsx
│   │   │   ├── EvidenceTag.test.tsx
│   │   │   └── AMDBadge.test.tsx
│   │   ├── utils/
│   │   │   ├── validation.test.ts
│   │   │   └── formatting.test.ts
│   │   └── api/
│   │       └── api-client.test.ts
│   ├── integration/
│   │   ├── upload-flow.test.tsx
│   │   ├── dashboard-render.test.tsx
│   │   └── chat-interaction.test.tsx
│   └── e2e/
│       ├── complete-workflow.spec.ts
│       ├── demo-mode.spec.ts
│       └── error-scenarios.spec.ts
├── tests/
│   └── fixtures/
│       ├── contract_a.pdf
│       ├── quotation_b.pdf
│       └── mock-responses.ts
```

---

## Conclusion

This technical design provides a comprehensive blueprint for building the DealFlow AI frontend application. The architecture emphasizes:

1. **Type Safety**: TypeScript throughout with strict mode
2. **Component Reusability**: Modular component structure with shadcn/ui base
3. **Performance**: Code splitting, lazy loading, optimized assets
4. **User Experience**: Smooth animations, real-time feedback, clear error messages
5. **Accessibility**: Keyboard navigation, screen reader support, WCAG AA compliance
6. **Maintainability**: Clear folder structure, separation of concerns, comprehensive testing

The phased development approach ensures iterative progress with testable milestones. The AMD branding integration is strategic and prominent without being overwhelming. The demo mode provides immediate value for judges and evaluators without requiring file uploads.

**Key Differentiators**:
- Conflict detection engine (automatically flags contradictions between documents)
- Evidence-cited AI responses (every answer links to source documents)
- Bloomberg Terminal aesthetic (corporate, data-dense, premium)
- AMD MI300X integration (visible performance benefits)
- Instant demo mode (zero friction evaluation)

This design is production-ready and hackathon-optimized, balancing technical excellence with practical delivery constraints.