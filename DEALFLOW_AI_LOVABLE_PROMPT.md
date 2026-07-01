# DEALFLOW AI — LOVABLE FRONTEND PROMPT
# Send this entire prompt to Lovable to generate the full frontend

---

## PROMPT START — COPY EVERYTHING BELOW THIS LINE

---

Build a complete, production-ready frontend for **DealFlow AI** — an AMD-accelerated enterprise document intelligence platform. This is for an international hackathon (AMD Developer Hackathon: ACT II on lablab.ai) so it must look premium, corporate, and technically impressive.

---

## 🎨 DESIGN SYSTEM

### Color Palette
```
Background Primary:    #080D1A  (near-black navy — main bg)
Background Secondary:  #0D1528  (slightly lighter navy — cards)
Background Tertiary:   #111E35  (card hover states)
Border:                #1E2D4A  (subtle borders)
Accent Primary:        #3B7BF6  (AMD-inspired electric blue)
Accent Secondary:      #6366F1  (indigo — secondary actions)
Accent Glow:           rgba(59, 123, 246, 0.15) (glow effects)
Text Primary:          #F0F4FF  (near-white)
Text Secondary:        #8B9CC8  (muted blue-grey)
Text Tertiary:         #4A5878  (very muted)
Success:               #10B981  (emerald green)
Warning:               #F59E0B  (amber)
Danger:                #EF4444  (red)
AMD Red Accent:        #ED1C24  (use sparingly — AMD brand)
```

### Typography
```
Display Font:    "DM Sans" — headings, hero text
Body Font:       "Inter" — body copy, labels, UI text
Mono Font:       "JetBrains Mono" — code, data values, document quotes
Import from Google Fonts: DM Sans (300,400,500,600,700) + Inter (400,500,600) + JetBrains Mono (400,500)
```

### Design Feel
- **Bloomberg Terminal meets Linear.app meets ChatGPT Enterprise**
- Dark, data-dense, corporate — NOT consumer/playful
- Subtle grain texture on backgrounds (CSS noise filter)
- Blue glow effects on active elements
- Crisp borders, no rounded corners above 8px except buttons (12px)
- Everything feels precise, intentional, expensive

---

## 🏗️ PAGES & ROUTES

Build these 4 pages:

1. `/` — Landing / Upload Page
2. `/dashboard` — Analysis Dashboard
3. `/chat` — Decision Copilot Chat
4. `/demo` — Demo Mode (pre-loaded with sample documents)

---

## 📄 PAGE 1: LANDING / UPLOAD PAGE (`/`)

### Layout
Full-height dark landing page with centered upload interface.

### Top Navigation Bar
```
Left:  DealFlow AI logo (text logo: "DealFlow" in DM Sans bold + "AI" in blue accent)
       + small AMD badge: "Powered by AMD MI300X" with small AMD logo hint
Right: "View Demo" button (ghost/outline style) + "Launch App" button (blue filled)
Height: 64px, sticky, border-bottom: 1px solid #1E2D4A
Background: rgba(8, 13, 26, 0.95) with backdrop blur
```

### Hero Section
```
Tag above headline: small pill badge — "AMD Developer Hackathon: ACT II" in blue
Main Headline (DM Sans 700, 56px): 
  "Your documents speak.
   We translate them into decisions."

Sub-headline (Inter 400, 18px, text-secondary):
  "Upload contracts, quotations, and invoices. Ask anything in plain language.
   Get evidence-based analysis in under 60 seconds — powered by AMD Instinct MI300X."

Two stats below headline (side by side):
  "< 60s" label: "Analysis time"
  "5.6x"  label: "Faster than CPU"
  "100%"  label: "Evidence-based"
```

### Upload Zone (Main Feature)
```
Large centered drop zone card:
- Size: ~680px wide, 280px tall
- Background: #0D1528
- Border: 2px dashed #1E2D4A (changes to 2px dashed #3B7BF6 on hover/drag)
- Border radius: 16px
- Glow effect on hover: box-shadow: 0 0 40px rgba(59, 123, 246, 0.15)

Inside the drop zone:
- Upload icon (large, 48px, blue)
- Primary text: "Drop your business documents here"
- Secondary text: "PDF, PNG, JPG, JPEG — up to 10 files, 10MB each"
- "or browse files" link in blue
- Below: small chips showing supported formats:
  [PDF] [PNG] [JPG] [JPEG]

After files are dropped — show file list INSIDE the zone:
- Each file: icon (PDF/IMG) + filename + file size + ✓ green check or spinner
- "Analyze Documents →" blue filled button appears at bottom
- Button has subtle pulsing glow animation when files are ready
```

### AMD Trust Banner
```
Below upload zone, horizontal strip:
"⚡ Running on AMD Instinct MI300X  |  ROCm-powered embeddings  |  Enterprise-grade inference"
Text in text-secondary color, small size
```

### How It Works Section (3 steps)
```
Three column cards:
1. 📁 "Upload Documents"
   "Drop your PDFs, contracts, quotations, invoices — any business document"

2. 🤖 "AI Analyzes Everything"  
   "Our AMD-powered AI reads all files simultaneously, extracts key information, and detects conflicts"

3. 💡 "Make Better Decisions"
   "Ask questions in plain language. Get evidence-backed answers with source citations"

Cards: dark background, blue number accent (01, 02, 03), subtle border
```

### Demo Section
```
"See it in action" section with a CTA:
- "Try with sample procurement documents →" 
- Links to /demo page
- Shows small thumbnail preview of the dashboard
```

---

## 📊 PAGE 2: ANALYSIS DASHBOARD (`/dashboard`)

### Layout
Two-column layout:
- Left sidebar (280px): Document list + session info
- Main content area: Analysis results

### Left Sidebar
```
Header: "Session Documents" + document count badge
List of uploaded files:
  Each item:
  - File type icon (PDF red / IMG blue)
  - Filename (truncated if long)
  - Page count or dimensions
  - Status: "Processed ✓" in green or spinner
  
Bottom of sidebar:
  - "Upload More" button
  - "New Session" button (clears everything)
  - AMD badge: small "Powered by AMD MI300X"
```

### Top Bar (Main Area)
```
Left: "Analysis Results" heading + timestamp "Analyzed just now"
Right: "Ask a Question →" button (blue) + "Export PDF" button (outline)
```

### CONFLICT ALERT BANNER (shows when conflicts detected)
```
IMPORTANT: This is the KILLER FEATURE — make it visually striking

Full-width banner ABOVE the cards:
Background: rgba(239, 68, 68, 0.08)
Border: 1px solid rgba(239, 68, 68, 0.3)
Border-left: 4px solid #EF4444
Border-radius: 8px
Padding: 16px 20px

Left side: ⚠️ red warning icon + "Conflicts Detected" in red bold
Right side: "2 conflicts found across your documents" in text-secondary
Bottom: expandable conflict details

EXPANDED STATE — show conflict cards:
Each conflict card:
  - "CONFLICT" tag in red
  - Type: "PAYMENT TERMS MISMATCH" in caps, small
  - Two side-by-side boxes:
    Left box (red tint):  📄 "Contract_A.pdf" → "Payment due in 30 days"
    Right box (red tint): 📄 "Invoice_001.pdf" → "Payment due in 90 days"
  - Risk badge: [HIGH RISK] in red
  - "Clarify payment terms before signing" in text-secondary
```

### Analysis Cards (2x2 Grid)
```
CARD 1: Executive Summary
- Card header: "Executive Summary" + 📋 icon
- Body: AI-generated paragraph text
- Small "Generated by AMD LLM" badge at bottom

CARD 2: Risk Analysis
- Card header: "Risk Analysis" + ⚠️ icon
- List of risks, each with colored badge:
  [HIGH]   red background — risk description
  [MEDIUM] amber background — risk description  
  [LOW]    green background — risk description
- Each risk has a source citation tag: 📄 "Contract_A.pdf"

CARD 3: Comparison Matrix
- Card header: "Document Comparison" + ⚖️ icon
- Clean data table:
  Columns: Feature | Doc A | Doc B | Doc C
  Rows: Price, Payment Terms, Delivery, Warranty, etc.
  Highlight cells in green (best) or red (worst)
  Stripe alternating rows

CARD 4: Recommendation
- Card header: "AI Recommendation" + 💡 icon
- Background slightly different: subtle blue tint (#0D1A35)
- Large recommendation text in slightly larger font
- "Recommended: Supplier B" in big blue text
- Reason paragraph below
- "Ask follow-up questions →" link at bottom
```

### Processing State (loading)
```
While documents are being analyzed, show:
- Skeleton loading on all 4 cards
- Top progress bar (blue, animated)
- Status text that updates:
  "Extracting text from documents..."
  "Generating AMD-accelerated embeddings..."
  "Running conflict detection..."
  "Synthesizing analysis..."
Each status update fades in/out smoothly
```

---

## 💬 PAGE 3: DECISION COPILOT CHAT (`/chat`)

### Layout
Full-height split layout:
- Left panel (320px): Document context + session info
- Right panel: Chat interface (full height)

### Left Panel — Document Context
```
"Active Documents" header
List of uploaded docs (same as sidebar above)
Divider
"Quick Questions" section:
  Pre-written example questions as clickable chips:
  "Which supplier is safest?"
  "What are the payment terms?"
  "Any risks I should know about?"
  "Which option is cheapest?"
  "What deadlines exist?"
  "What information is missing?"
  
Clicking a chip auto-sends that question to chat
```

### Chat Interface (Right Panel)

#### Chat Header
```
"Decision Copilot" title + AI animation (see below)
Right side: "Export Chat as PDF" button
Bottom border separator
```

#### AI CHAT ANIMATION — MOST IMPORTANT VISUAL ELEMENT
```
This is the signature element. Build a custom AI thinking animation.

When AI is processing/thinking, show:
- A circular "thinking" indicator next to the AI avatar
- Animated neural network pulse: 3-4 dots that pulse in a wave pattern
- The dots have a blue glow: color #3B7BF6, box-shadow glow
- Subtle "Processing with AMD MI300X..." text below in text-tertiary
- The entire AI message bubble should have a subtle shimmer/skeleton 
  while content is streaming in

During response streaming (text appears word by word):
- Text streams in with a cursor blink at the end
- Each section (Answer/Evidence/Risk/Recommendation) 
  fades in sequentially, not all at once
- Evidence tags animate in with a subtle slide-up

The AI avatar:
- Hexagonal shape (not circle — feels more technical)
- Dark background with blue gradient
- "DF" initials or small circuit-pattern icon inside
- Pulsing blue ring around it when actively thinking
```

#### Message Bubbles

**User message:**
```
Right-aligned
Background: #1E2D4A
Border-radius: 16px 16px 4px 16px
Text in text-primary
Small timestamp below
```

**AI message:**
```
Left-aligned, full width
Background: #0D1528
Border: 1px solid #1E2D4A
Border-radius: 16px 16px 16px 4px
Left border: 3px solid #3B7BF6 (blue accent strip)

STRUCTURED RESPONSE FORMAT inside bubble:
Every AI response has 4 labeled sections:

┌─────────────────────────────────────┐
│ 💬 ANSWER                           │
│ [Direct answer text in text-primary]│
├─────────────────────────────────────┤
│ 📎 EVIDENCE                         │
│ Quoted text from document           │
│ [📄 Contract_A.pdf] ← source tag   │
├─────────────────────────────────────┤
│ ⚠️ RISK                             │
│ Risk description (amber text)       │
├─────────────────────────────────────┤
│ ✅ RECOMMENDATION                   │
│ Actionable next step (blue text)    │
└─────────────────────────────────────┘

Source tags styling:
- Small pill shape
- Background: #1E2D4A
- Border: 1px solid #2E3D5A
- Icon: 📄 + filename in mono font
- Hover: highlight in blue
- Color coded: PDF=red, IMG=blue
```

#### Chat Input Area
```
Bottom of chat, fixed position
Background: #0D1528
Border-top: 1px solid #1E2D4A
Padding: 16px

Input field:
- Full width text input
- Background: #111E35
- Border: 1px solid #1E2D4A
- Placeholder: "Ask anything about your documents..."
- Focus state: border color #3B7BF6 + subtle glow
- Right side of input: Send button (blue arrow icon)
- Left side: paperclip icon for adding more files

Below input:
Small text: "DealFlow AI only answers from your uploaded documents"
```

#### Empty State (no messages yet)
```
Centered in chat area:
- Large hexagonal AI icon with pulsing animation
- "Ask me anything about your documents"
- Subtitle: "I'll provide evidence-based answers with source citations"
- Show the quick question chips here too
```

---

## 🎮 PAGE 4: DEMO MODE (`/demo`)

### Purpose
Pre-loaded with sample procurement documents so judges/users can try it instantly without uploading files.

### Sample Documents Included
```
Pre-loaded fake business documents (show as if already uploaded):

1. "Supplier_A_Quotation.pdf"
   Content simulation: IT equipment supplier, total $45,200, payment 30 days

2. "Supplier_B_Quotation.pdf" 
   Content simulation: Same equipment, total $42,800, payment 60 days

3. "Existing_Contract_TechCorp.pdf"
   Content simulation: Current supplier contract, payment 30 days, expires Sept 2026

4. "Invoice_TechCorp_March2026.pdf"
   Content simulation: Last invoice, $48,500 (higher than quotation — CONFLICT!)

5. "Company_Procurement_Policy.pdf"
   Content simulation: Max single-vendor spend $50,000, requires 3 quotes for >$40,000
```

### Demo Banner
```
Top of page, amber banner:
"🎯 Demo Mode — Pre-loaded with sample procurement documents. 
 No upload needed. Try asking: 'Which supplier should I choose?'"
```

### Pre-populated Analysis
Show the dashboard already analyzed with:
- Executive summary about the procurement scenario
- Conflict detected: Invoice ($48,500) vs Supplier A quote ($45,200) — price discrepancy
- Comparison matrix of Supplier A vs B
- Recommendation: Supplier B (lower cost + flexible payment)

### Pre-seeded Chat Messages
Show 2-3 example exchanges already in the chat:
```
User: "Which supplier is safest?"
AI:   [Full structured response with evidence tags pointing to demo docs]

User: "Are there any conflicts in these documents?"
AI:   [Highlights the invoice vs quotation price discrepancy]
```

---

## 🧩 SHARED COMPONENTS

### AMD Badge Component
```
Used throughout the app
Small horizontal pill:
"⚡ AMD MI300X" 
Background: rgba(237, 28, 36, 0.08)
Border: 1px solid rgba(237, 28, 36, 0.2)
Text: #ED1C24 (AMD red)
Font: Inter 500, 11px
Icon: small lightning bolt
```

### Evidence Tag Component
```
Clickable pill that references a source document:
[📄 filename.pdf]
Background: #1E2D4A
Border: 1px solid #2E3D5A
Font: JetBrains Mono 12px
Hover: border-color #3B7BF6, cursor pointer
Active: slight scale(0.97)
```

### Risk Badge Component
```
[HIGH]   bg: rgba(239,68,68,0.15)   border: rgba(239,68,68,0.3)   text: #EF4444
[MEDIUM] bg: rgba(245,158,11,0.15)  border: rgba(245,158,11,0.3)  text: #F59E0B
[LOW]    bg: rgba(16,185,129,0.15)  border: rgba(16,185,129,0.3)  text: #10B981
Font: Inter 600, 11px, uppercase, letter-spacing: 0.08em
Border-radius: 4px
```

### Processing Animation Component
```
Used during AI thinking states:
Three dots in a row, each:
- Width/height: 8px
- Border-radius: 50%
- Background: #3B7BF6
- Animation: pulse up and down, staggered 0.15s delay each
- Glow: box-shadow 0 0 8px rgba(59,123,246,0.6)
Total animation duration: 1.2s infinite
```

### File Upload Progress Card
```
While a file is processing after upload:
Shows a card with:
- Filename
- Progress steps (with checkmarks):
  ✓ File received
  ✓ Text extracted
  ✓ OCR completed (for images)
  ⟳ Generating embeddings... (animated spinner, blue)
  ○ Indexing to knowledge base
Each step fades in as it completes
```

---

## ✨ MICRO-ANIMATIONS & INTERACTIONS

### Page Load
```
Staggered fade-in for all elements:
- Nav: 0ms delay
- Hero text: 100ms delay  
- Upload zone: 200ms delay
- Stats: 300ms delay
Each animates: opacity 0→1 + translateY(16px→0)
Duration: 500ms ease-out
```

### Upload Zone Drag State
```
On file drag-over:
- Border: 2px dashed #3B7BF6
- Background: rgba(59,123,246,0.05)
- Box-shadow: 0 0 60px rgba(59,123,246,0.2)
- Scale: 1.01
- Drop zone text changes to: "Drop files here"
Smooth transition: 200ms
```

### Analyze Button Pulse
```
When files are ready to analyze:
Button has continuous subtle glow pulse:
Keyframes:
  0%:   box-shadow: 0 0 0px rgba(59,123,246,0)
  50%:  box-shadow: 0 0 20px rgba(59,123,246,0.4)
  100%: box-shadow: 0 0 0px rgba(59,123,246,0)
Duration: 2s infinite
```

### Dashboard Card Entrance
```
When analysis results load, cards animate in:
- Staggered: 0ms, 100ms, 200ms, 300ms
- From: opacity 0, translateY(20px)
- To: opacity 1, translateY(0)
- Duration: 400ms ease-out
```

### Conflict Banner
```
Slides down from top with bounce:
From: translateY(-100%), opacity 0
To:   translateY(0), opacity 1
Duration: 500ms cubic-bezier(0.175, 0.885, 0.32, 1.275)
```

### Chat Message Entrance
```
User message: slides in from right (translateX 20px → 0)
AI message: slides in from left (translateX -20px → 0)
Both: opacity 0 → 1
Duration: 300ms ease-out
```

### AI Typing Indicator
```
Before AI responds, show typing indicator bubble (left aligned):
Same styling as AI message bubble but only contains:
The three-dot processing animation (see above)
Disappears when actual response starts streaming
```

### Text Streaming Effect
```
AI response text streams in word by word
After each word: append with 20ms delay
At end of streaming: blinking cursor | disappears after 500ms
Sections reveal sequentially:
  ANSWER section: streams immediately
  EVIDENCE section: fades in after ANSWER completes + 200ms
  RISK section: fades in after EVIDENCE + 200ms
  RECOMMENDATION: fades in last + 200ms
```

---

## 📱 RESPONSIVE BREAKPOINTS

```
Desktop (1280px+):  Full layout as described above
Laptop  (1024px):   Sidebar narrows to 240px
Tablet  (768px):    Sidebar collapses to icon-only, expandable
Mobile  (375px+):   Single column, bottom sheet for sidebar
                    Chat takes full screen
                    Upload is full width
```

---

## 🔌 API INTEGRATION STUBS

Create these API functions (mock them with realistic fake data):

```typescript
// lib/api.ts

// Upload documents
POST /api/upload
→ Returns: { session_id, documents[] }

// Get analysis
POST /api/analyze  
→ Returns: { executive_summary, risks[], comparison_matrix[], conflicts[], recommendation }

// Chat
POST /api/chat
→ Returns: { answer, evidence[], risks, recommendation }
Simulate streaming with setTimeout word-by-word

// Export PDF
POST /api/report
→ Simulates download trigger

// Demo mode
GET /api/demo
→ Returns pre-loaded sample data (hardcoded realistic mock data)
```

### Mock Data for Demo Mode
```typescript
// Hardcode realistic mock responses for demo:

const DEMO_ANALYSIS = {
  executive_summary: "Analysis of 5 procurement documents reveals two competing supplier quotations for IT infrastructure equipment. Supplier B presents a more favorable financial profile at $42,800 vs Supplier A at $45,200, with more flexible payment terms. However, a critical price discrepancy has been detected between the existing TechCorp invoice ($48,500) and their current quotation ($45,200), warranting clarification before contract renewal.",
  
  risks: [
    { level: "HIGH", description: "Price discrepancy detected: TechCorp invoice ($48,500) exceeds their current quotation ($45,200) by $3,300", source: "Invoice_TechCorp_March2026.pdf" },
    { level: "MEDIUM", description: "Current contract expires September 2026 — procurement must be completed within 90 days", source: "Existing_Contract_TechCorp.pdf" },
    { level: "LOW", description: "Supplier A payment terms (30 days) are more aggressive than company standard (60 days)", source: "Supplier_A_Quotation.pdf" }
  ],
  
  conflicts: [
    {
      type: "PRICE DISCREPANCY",
      doc_a: { name: "Invoice_TechCorp_March2026.pdf", quote: "Total amount due: $48,500.00" },
      doc_b: { name: "Supplier_A_Quotation.pdf", quote: "Total quotation value: $45,200.00" },
      severity: "HIGH",
      explanation: "TechCorp's last invoice is $3,300 higher than their current quotation for equivalent equipment",
      action: "Request clarification from TechCorp on pricing discrepancy before any contract renewal"
    }
  ],
  
  comparison_matrix: [
    { field: "Total Price", supplier_a: "$45,200", supplier_b: "$42,800", winner: "B" },
    { field: "Payment Terms", supplier_a: "30 days", supplier_b: "60 days", winner: "B" },
    { field: "Delivery Time", supplier_a: "14 days", supplier_b: "21 days", winner: "A" },
    { field: "Warranty", supplier_a: "1 year", supplier_b: "2 years", winner: "B" },
    { field: "Support SLA", supplier_a: "48 hours", supplier_b: "24 hours", winner: "B" }
  ],
  
  recommendation: "Proceed with Supplier B. Lower total cost ($42,800 vs $45,200), more flexible payment terms (60 days), extended warranty (2 years), and better support SLA (24h) make Supplier B the superior choice. Advise procurement team to clarify the TechCorp invoice discrepancy regardless of final decision."
}
```

---

## 🏁 FINAL REQUIREMENTS CHECKLIST

Before considering this complete, verify:

- [ ] All 4 pages built and navigable
- [ ] Upload zone with drag-and-drop working
- [ ] AI chat animation (hexagonal avatar + thinking dots + streaming text)
- [ ] Conflict detection banner visible on dashboard
- [ ] Evidence tags with source citations in chat
- [ ] Comparison matrix table with color-coded winners
- [ ] Risk badges (HIGH/MEDIUM/LOW) with correct colors
- [ ] AMD badge present on landing + dashboard + chat
- [ ] Demo page with pre-loaded sample data
- [ ] Quick question chips in chat sidebar
- [ ] Structured AI response format (Answer/Evidence/Risk/Recommendation)
- [ ] Processing/loading states with AMD-themed copy
- [ ] Responsive on mobile
- [ ] Dark corporate theme consistent across all pages
- [ ] Staggered animations on page load
- [ ] Text streaming simulation in chat

---

## 🎯 PRIORITY ORDER (build in this order)

1. Landing/Upload page — first impression for judges
2. Analysis Dashboard — main value demonstration  
3. Chat interface with AI animation — most visually impressive
4. Demo page with mock data — judges can try it immediately

---

*DealFlow AI Frontend — AMD Developer Hackathon: ACT II*
*Corporate. Precise. AMD-powered. Filipino-built.*
