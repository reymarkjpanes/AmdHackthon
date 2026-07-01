PROMPT 0 — DESIGN SYSTEM (RUN THIS FIRST)
═══════════════════════════════════════════
Create a design system page for DealFlow AI with the following exact specifications. This will be referenced by all other screens.

COLORS — Create as Figma color styles:
Background/Primary #080D1A Background/Secondary #0D1528 Background/Tertiary #111E35 Border/Default #1E2D4A Border/Active #3B7BF6 Accent/Blue #3B7BF6 Accent/Glow rgba(59, 123, 246, 0.15) Text/Primary #F0F4FF Text/Secondary #8B9CC8 Text/Tertiary #4A5878 Status/Success #10B981 Status/Warning #F59E0B Status/Danger #EF4444 AMD/Red #ED1C24

TYPOGRAPHY — Create as Figma text styles:
Display/Hero DM Sans Bold 56px line-height 64px #F0F4FF Display/H1 DM Sans Bold 40px line-height 48px #F0F4FF Display/H2 DM Sans SemiBold 28px line-height 36px #F0F4FF Display/H3 DM Sans SemiBold 20px line-height 28px #F0F4FF Body/Large Inter Regular 18px line-height 28px #F0F4FF Body/Default Inter Regular 16px line-height 24px #8B9CC8 Body/Small Inter Regular 14px line-height 20px #8B9CC8 Label/Default Inter Medium 14px line-height 20px #F0F4FF Label/Small Inter Medium 12px line-height 16px #8B9CC8 Label/Caps Inter SemiBold 11px line-height 16px #8B9CC8 letter-spacing 0.08em UPPERCASE Mono/Default JetBrains Mono Regular 13px #8B9CC8 Mono/Small JetBrains Mono Regular 11px #4A5878

COMPONENTS — Create these as Figma components:
--- COMPONENT: AMD Badge --- Size: auto width, 24px height Background: rgba(237, 28, 36, 0.08) Border: 1px solid rgba(237, 28, 36, 0.20) Border radius: 100px Padding: 4px 10px Content: ⚡ icon (12px, #ED1C24) + "AMD MI300X" text (Label/Small, #ED1C24) Gap between icon and text: 4px

--- COMPONENT: Risk Badge (3 variants) --- Variant HIGH: Background: rgba(239, 68, 68, 0.12) Border: 1px solid rgba(239, 68, 68, 0.25) Text: "HIGH" Label/Caps #EF4444 Border radius: 4px Padding: 3px 8px

Variant MEDIUM: Background: rgba(245, 158, 11, 0.12) Border: 1px solid rgba(245, 158, 11, 0.25) Text: "MEDIUM" Label/Caps #F59E0B Border radius: 4px Padding: 3px 8px

Variant LOW: Background: rgba(16, 185, 129, 0.12) Border: 1px solid rgba(16, 185, 129, 0.25) Text: "LOW" Label/Caps #10B981 Border radius: 4px Padding: 3px 8px

--- COMPONENT: Evidence Tag --- Background: #111E35 Border: 1px solid #1E2D4A Border radius: 6px Padding: 4px 10px Content: 📄 icon (12px) + filename in Mono/Small #8B9CC8 Height: 24px

--- COMPONENT: Primary Button --- Background: #3B7BF6 Border radius: 10px Padding: 12px 24px Text: Label/Default #F0F4FF Height: 44px Hover state: background #2D6AE0 Box shadow: 0 0 20px rgba(59, 123, 246, 0.3)

--- COMPONENT: Ghost Button --- Background: transparent Border: 1px solid #1E2D4A Border radius: 10px Padding: 12px 24px Text: Label/Default #8B9CC8 Height: 44px Hover state: border #3B7BF6, text #F0F4FF

--- COMPONENT: Card --- Background: #0D1528 Border: 1px solid #1E2D4A Border radius: 12px Padding: 24px Width: flexible

--- COMPONENT: Navigation Bar --- Width: 1440px (full width) Height: 64px Background: rgba(8, 13, 26, 0.95) Border bottom: 1px solid #1E2D4A Layout: horizontal flex, space-between, align center Padding: 0 40px

Left side: Logo text: "DealFlow" DM Sans Bold 20px #F0F4FF + "AI" DM Sans Bold 20px #3B7BF6 Gap: 0px between words AMD Badge component next to logo, gap 12px

Right side: "View Demo" Ghost Button (smaller: padding 8px 16px, height 36px) "Launch App" Primary Button (smaller: padding 8px 16px, height 36px) Gap between buttons: 8px

═══════════════════════════════════════════
PROMPT 1 — SCREEN 1: LANDING / UPLOAD PAGE
═══════════════════════════════════════════
Create a full desktop screen (1440 x 900px) for the DealFlow AI landing page. This is the first thing users see.

BACKGROUND: Fill entire frame with #080D1A Add subtle grain/noise texture overlay at 3% opacity on top

NAVIGATION BAR
Use the Navigation Bar component from design system. Position: top, full width, y=0

HERO SECTION
Position: centered horizontally, y=120px from top Width: 720px, centered on 1440px canvas

Element 1 — Event Badge: Pill shape, background rgba(59,123,246,0.08), border 1px solid rgba(59,123,246,0.2), border-radius 100px Text: "⚡ AMD Developer Hackathon: ACT II" Font: Label/Small #3B7BF6 Padding: 6px 16px Center aligned

Element 2 — Main Headline (48px gap below badge): Line 1: "Your documents speak." Line 2: "We translate them into decisions." Font: Display/Hero DM Sans Bold 56px #F0F4FF Text align: center Line height: 64px

Element 3 — Subheadline (24px below headline): "Upload contracts, quotations, and invoices. Ask anything in plain language. Get evidence-based decisions in under 60 seconds — powered by AMD Instinct MI300X." Font: Body/Large Inter Regular 18px #8B9CC8 Text align: center Max width: 580px

Element 4 — Stats Row (32px below subheadline): 3 stats side by side, centered, gap 48px between each

Stat 1: Number: "< 60s" DM Sans Bold 32px #F0F4FF Label: "Analysis time" Label/Small #8B9CC8

Stat 2: Number: "5.6x" DM Sans Bold 32px #3B7BF6 Label: "Faster on AMD GPU" Label/Small #8B9CC8

Stat 3: Number: "100%" DM Sans Bold 32px #F0F4FF Label: "Evidence-based" Label/Small #8B9CC8

Add thin vertical dividers (#1E2D4A) between stats

UPLOAD ZONE (Main CTA)
Position: 48px below hero section, horizontally centered Width: 680px, Height: 260px

Background: #0D1528 Border: 2px dashed #1E2D4A Border radius: 16px

Inside the upload zone — centered vertically and horizontally:

Icon: Upload cloud icon, 48x48px, color #3B7BF6 Add soft glow: background circle 80x80px rgba(59,123,246,0.08) behind the icon

Primary text (16px below icon): "Drop your business documents here" Font: Display/H3 DM Sans SemiBold 20px #F0F4FF

Secondary text (8px below): "PDF, PNG, JPG, JPEG — up to 10 files, 10MB each" Font: Body/Small #4A5878

Browse link (12px below): "or browse files" Font: Label/Default #3B7BF6 (underline)

Format chips (16px below, horizontal row, centered, gap 8px): 4 chips: [PDF] [PNG] [JPG] [JPEG] Each chip: background #111E35, border 1px solid #1E2D4A, border-radius 6px, padding 4px 10px, Mono/Small #4A5878

IMPORTANT: Add subtle blue glow on the entire upload zone card: box-shadow: 0 0 60px rgba(59, 123, 246, 0.06) (very subtle outer glow)

AMD TRUST STRIP
Position: 24px below upload zone, full width Height: 40px Background: rgba(59, 123, 246, 0.04) Border top: 1px solid rgba(59, 123, 246, 0.08) Border bottom: 1px solid rgba(59, 123, 246, 0.08)

Content (centered horizontally, vertically centered): "⚡ Running on AMD Instinct MI300X · ROCm-powered embeddings · Enterprise-grade inference" Font: Label/Small #4A5878 Use · as separator (not |)

HOW IT WORKS SECTION
Position: 64px below AMD strip Width: 1040px, centered

Section label (centered): "HOW IT WORKS" Label/Caps #4A5878

Section title (12px below label, centered): "From documents to decisions in 3 steps" Font: Display/H2 #F0F4FF

Three cards (48px below title, horizontal row, gap 24px): Each card: 320px wide, use Card component

Card 1 — Upload: Number: "01" DM Sans Bold 40px rgba(59,123,246,0.2) Icon: folder upload icon 28px #3B7BF6 (12px below number) Title: "Upload Documents" Display/H3 #F0F4FF (12px below icon) Body: "Drop your PDFs, contracts, quotations, invoices — any business document" Font: Body/Default #8B9CC8 (8px below title)

Card 2 — Analyze: Number: "02" (same style) Icon: cpu/chip icon 28px #3B7BF6 Title: "AMD AI Analyzes Everything" Body: "Our AMD-powered AI reads all files simultaneously, extracts key information, and detects conflicts across documents"

Card 3 — Decide: Number: "03" (same style) Icon: lightbulb icon 28px #3B7BF6 Title: "Make Better Decisions" Body: "Ask questions in plain language. Get evidence-backed answers with exact source citations from your documents"

DEMO CTA SECTION
Position: 64px below how it works Centered, width 600px

Background: rgba(59, 123, 246, 0.04) Border: 1px solid rgba(59, 123, 246, 0.12) Border radius: 16px Padding: 32px 40px

Content centered: Title: "See it in action — no upload needed" Font: Display/H3 #F0F4FF

Subtitle (8px below): "Try with pre-loaded procurement documents" Font: Body/Default #8B9CC8

Button (20px below): Primary Button "Try Demo →"

═══════════════════════════════════════════
PROMPT 2 — SCREEN 2: ANALYSIS DASHBOARD
═══════════════════════════════════════════
Create a full desktop screen (1440 x 960px) for the DealFlow AI analysis dashboard. This shows results after documents are processed.

BACKGROUND: #080D1A full frame

NAVIGATION BAR
Same as landing page. Show "DealFlow AI" logo. Add breadcrumb below nav (y=64px): "← Upload" #4A5878 → "Analysis Dashboard" #F0F4FF Font: Label/Small, padding-left 40px

LEFT SIDEBAR
Position: x=0, y=64px Width: 280px, Height: full page height Background: #0D1528 Border right: 1px solid #1E2D4A

Sidebar contents:

Section header (padding 20px): "Session Documents" Label/Default #8B9CC8

pill badge "5" (background #1E2D4A, text #F0F4FF, font Label/Small, border-radius 100px, padding 2px 8px)
Document list (5 items, each 56px tall):

Each document item: Left padding 16px, right padding 16px Hover state: background #111E35

Item 1: Supplier_A_Quotation.pdf Icon: PDF badge (24x24px, background rgba(239,68,68,0.1), border-radius 6px, text "PDF" Label/Small #EF4444) Filename: "Supplier_A_Quotation.pdf" Label/Default #F0F4FF (truncate) Sub: "3 pages · Processed" Mono/Small #10B981

Item 2: Supplier_B_Quotation.pdf (same style) Sub: "3 pages · Processed"

Item 3: Existing_Contract_TechCorp.pdf Sub: "8 pages · Processed"

Item 4: Invoice_TechCorp_March2026.pdf Sub: "2 pages · Processed"

Item 5: Procurement_Policy.png Icon: IMG badge (background rgba(59,123,246,0.1), text "IMG" #3B7BF6) Sub: "Image · OCR Complete"

Divider: 1px solid #1E2D4A

Bottom of sidebar (padding 16px): "Upload More" Ghost Button (full width, height 36px) "New Session" text link (center aligned, Label/Small #4A5878) AMD Badge component (centered, 16px margin top)

MAIN CONTENT AREA
Position: x=280px, y=64px Width: 1160px

TOP BAR
Height: 56px Background: #080D1A Border bottom: 1px solid #1E2D4A Padding: 0 32px Flex: space-between, align center

Left: "Analysis Results" Display/H3 #F0F4FF

"· Analyzed just now" Label/Small #4A5878 (8px gap)
Right (gap 12px between): "Ask a Question →" Primary Button (height 36px, padding 8px 20px) "Export PDF" Ghost Button (height 36px, padding 8px 20px)

download icon 16px before text
CONFLICT ALERT BANNER (CRITICAL — most visible element)
Position: 16px from top of content, 32px horizontal margin Full width of content area minus margins

Background: rgba(239, 68, 68, 0.06) Border: 1px solid rgba(239, 68, 68, 0.25) Border left: 4px solid #EF4444 Border radius: 10px Padding: 16px 20px

Layout: horizontal flex, space-between

Left side: ⚠️ icon 20px #EF4444 + gap 12px "Conflict Detected" DM Sans SemiBold 16px #EF4444

gap 16px "1 critical conflict found across your documents" Body/Small #8B9CC8
Right side: "View Details ↓" Label/Small #EF4444

Below (expanded state — show by default): 16px margin top, padding top 16px, border top 1px solid rgba(239,68,68,0.15)

Conflict card inside the banner: Background: rgba(239, 68, 68, 0.04) Border radius: 8px Padding: 16px

Top row: "PRICE DISCREPANCY" Label/Caps #EF4444 + Risk Badge HIGH (gap 8px)

Two side-by-side boxes (gap 16px, margin top 12px): Each box: Background: rgba(239, 68, 68, 0.06) Border: 1px solid rgba(239, 68, 68, 0.15) Border radius: 8px Padding: 12px Width: 50%


Box A:
  Evidence Tag: "Invoice_TechCorp_March2026.pdf"
  Quote (12px below): 
    "Total amount due: $48,500.00"
    Mono/Default #F0F4FF

Box B:
  Evidence Tag: "Supplier_A_Quotation.pdf"
  Quote (12px below):
    "Total quotation value: $45,200.00"
    Mono/Default #F0F4FF
Action (12px below boxes): "→ Request written clarification from TechCorp before any contract renewal." Body/Small #8B9CC8

ANALYSIS CARDS — 2x2 GRID
Position: 24px below conflict banner Padding: 0 32px Grid: 2 columns, gap 20px

--- CARD 1: EXECUTIVE SUMMARY --- Width: 100% of column, use Card component

Card header row: "Executive Summary" Display/H3 #F0F4FF

📋 icon 18px #4A5878 (right aligned)
Divider: 1px solid #1E2D4A (12px margin)

Body text: "Analysis of 5 procurement documents reveals two competing supplier quotations for IT infrastructure equipment. Supplier B presents a more favorable financial profile at $42,800 vs Supplier A at $45,200, with more flexible 60-day payment terms. A critical price discrepancy has been detected between the existing TechCorp invoice and their current quotation." Font: Body/Default #8B9CC8 Line height: 24px

Footer (16px below, top border 1px solid #1E2D4A, padding top 12px): "Generated by AMD Llama 3.2 Vision" Label/Small #4A5878

AMD Badge component (right aligned)
--- CARD 2: RISK ANALYSIS --- Card header: "Risk Analysis" + ⚠️ icon

3 risk items (gap 12px between):

Risk item layout: horizontal flex, align start, gap 12px Left: Risk Badge (HIGH / MEDIUM / LOW) Right: Description: Body/Default #F0F4FF Source (4px below): Evidence Tag component

Risk 1: [HIGH] "Price discrepancy: TechCorp invoice ($48,500) exceeds current quotation ($45,200) by $3,300 — 7.3% variance" Source: Invoice_TechCorp_March2026.pdf

Risk 2: [MEDIUM] "TechCorp contract expires September 2026 — procurement must close within 90 days" Source: Existing_Contract_TechCorp.pdf

Risk 3: [LOW] "Supplier A requires 30-day payment terms — more aggressive than company 60-day standard" Source: Supplier_A_Quotation.pdf

--- CARD 3: COMPARISON MATRIX --- Card header: "Document Comparison" + ⚖️ icon

Table (full width of card): Border: 1px solid #1E2D4A Border radius: 8px Overflow: hidden

Header row: Background: #111E35 Height: 40px Columns: "Feature" | "Supplier A" | "Supplier B" | "Winner" Font: Label/Small #4A5878 Padding: 0 16px Border bottom: 1px solid #1E2D4A

Data rows (height 48px each, alternating bg): Row 1 bg: #0D1528 Row 2 bg: rgba(17, 30, 53, 0.5)

Data (Label/Default): Total Price | $45,200 | $42,800 | ✓ Supplier B (green text) Payment Terms| 30 days | 60 days | ✓ Supplier B Delivery | 14 days ✓ | 21 days | ✓ Supplier A (green) Warranty | 1 year | 2 years | ✓ Supplier B Support SLA | 48 hours | 24 hours | ✓ Supplier B

Winner column: show "✓ [name]" in #10B981 for winner rows Padding: 0 16px

--- CARD 4: RECOMMENDATION --- Background: rgba(59, 123, 246, 0.04) Border: 1px solid rgba(59, 123, 246, 0.15) (slightly different from regular card — blue tint)

Card header: "AI Recommendation" + 💡 icon

Recommendation badge (12px below header): Pill: background rgba(16,185,129,0.12), border rgba(16,185,129,0.25) Text: "✓ Recommended: Supplier B" Label/Default #10B981 Padding: 8px 16px, border-radius: 100px

Body text (16px below): "Proceed with Supplier B. At $42,800 vs $45,200, Supplier B is $2,400 cheaper while offering superior terms: 60-day payment flexibility, 2-year warranty, and 24-hour support SLA. Regardless of final choice, clarify the TechCorp invoice discrepancy — a $3,300 variance is a procurement risk." Font: Body/Default #8B9CC8

CTA link (16px below, top border): "Ask follow-up questions →" Label/Default #3B7BF6

═══════════════════════════════════════════
PROMPT 3 — SCREEN 3: DECISION COPILOT CHAT
═══════════════════════════════════════════
Create a full desktop screen (1440 x 900px) for the DealFlow AI Decision Copilot chat interface.

BACKGROUND: #080D1A full frame

NAVIGATION BAR (same as other screens)
LEFT PANEL — DOCUMENT CONTEXT
Position: x=0, y=64px Width: 300px, height: full Background: #0D1528 Border right: 1px solid #1E2D4A

Panel title (padding 20px): "Active Documents" Label/Default #8B9CC8

Document list (same 5 docs as dashboard, compact version): Each item 44px tall, padding 12px 16px: PDF/IMG badge + filename Label/Small #F0F4FF (truncated)

Divider 1px solid #1E2D4A + 20px spacing

Section: "Quick Questions" Label: "QUICK QUESTIONS" Label/Caps #4A5878 (padding 0 16px)

6 clickable chips (12px below label, padding 0 16px, gap 8px, wrap): Each chip: Background: #111E35 Border: 1px solid #1E2D4A Border radius: 8px Padding: 8px 12px Font: Body/Small #8B9CC8 Hover: border #3B7BF6, text #F0F4FF

Chips: "Which supplier is safest?" "What are payment terms?" "Any risks I should know?" "Which option is cheapest?" "What deadlines exist?" "What info is missing?"

MAIN CHAT AREA
Position: x=300px, y=64px Width: 1140px Height: full page

CHAT HEADER
Height: 64px Background: #0D1528 Border bottom: 1px solid #1E2D4A Padding: 0 28px Flex: space-between, align center

Left side: AI AVATAR (hexagonal shape): Size: 36x36px Shape: hexagon (clip path) Background: linear gradient 135deg #1E2D4A → #0D1528 Border: 2px solid #3B7BF6 Inside: "DF" text DM Sans Bold 14px #3B7BF6 Outer ring: 40x40px hexagon, border 1px solid rgba(59,123,246,0.3)


THINKING ANIMATION (show on this screen):
  3 dots below/beside the hexagon avatar
  Each dot: 6x6px circle, background #3B7BF6
  Spacing: 4px between dots
  Staggered opacity animation: dot1 full, dot2 medium, dot3 low
  This represents "AI is processing"
Text (12px right of avatar, flex column): "Decision Copilot" DM Sans SemiBold 16px #F0F4FF "Analyzing 5 documents · AMD MI300X active" Label/Small #10B981

Right side: "Export Chat as PDF" Ghost Button (height 32px, small)

CHAT MESSAGES AREA
Position: below header, above input Padding: 28px Overflow: scrollable Background: #080D1A

Show these messages in order:

--- USER MESSAGE 1 --- Alignment: RIGHT Max width: 520px, aligned to right edge

Bubble: Background: #1E2D4A Border radius: 16px 16px 4px 16px Padding: 14px 18px

Text: "Which supplier should I choose?" Font: Body/Default #F0F4FF

Timestamp below (right aligned): "just now" Mono/Small #4A5878

--- AI MESSAGE 1 --- Alignment: LEFT Max width: 720px

Bubble: Background: #0D1528 Border: 1px solid #1E2D4A Border left: 3px solid #3B7BF6 Border radius: 4px 16px 16px 16px Padding: 20px

Inside the bubble — 4 labeled sections:

SECTION 1 — ANSWER: Label: "ANSWER" Label/Caps #4A5878 + thin line divider (rgba(255,255,255,0.06)) Content (12px below): "Supplier B is the recommended choice based on overall value, payment flexibility, and support terms." Font: Body/Default #F0F4FF

SECTION 2 — EVIDENCE: Label: "EVIDENCE" Label/Caps #4A5878 (16px margin top) 3 evidence items (8px gap each): Each item: left border 2px solid rgba(59,123,246,0.3), background rgba(59,123,246,0.04), border-radius 0 6px 6px 0, padding 8px 12px

Item 1: Quote: "$42,800.00 total quotation value" Mono/Default #F0F4FF Below: Evidence Tag "Supplier_B_Quotation.pdf"

Item 2: Quote: "Payment terms: Net 60 days from invoice date" Evidence Tag: "Supplier_B_Quotation.pdf"

Item 3: Quote: "Warranty period: 24 months from delivery" Evidence Tag: "Supplier_B_Quotation.pdf"

SECTION 3 — RISK: Label: "RISK" Label/Caps #4A5878 (16px margin top) Risk line: ⚠️ icon 14px #F59E0B + gap 8px "Supplier B delivery timeline is 21 days vs Supplier A at 14 days." Font: Body/Small #F59E0B

SECTION 4 — RECOMMENDATION: Label: "RECOMMENDATION" Label/Caps #4A5878 (16px margin top) Background: rgba(16,185,129,0.04) Border radius: 8px Padding: 12px

→ icon 14px #10B981 + gap 8px "Initiate contract discussions with Supplier B. Negotiate delivery timeline if 14 days is critical to operations." Font: Body/Small #10B981

CHAT INPUT AREA
Position: bottom, fixed Height: 80px Background: #0D1528 Border top: 1px solid #1E2D4A Padding: 16px 28px

Input container: Background: #111E35 Border: 1px solid #1E2D4A Border radius: 12px Height: 48px Padding: 0 16px Flex: row, align center

Left: 📎 paperclip icon 18px #4A5878 Center: placeholder text "Ask anything about your documents..." Body/Default #4A5878 Right: Send button — circle 32x32px, background #3B7BF6, arrow-right icon 16px #F0F4FF

Below input: "DealFlow AI only answers from your uploaded documents · Powered by AMD" Label/Small #4A5878, centered

═══════════════════════════════════════════
PROMPT 4 — SCREEN 4: DEMO MODE
═══════════════════════════════════════════
Create a full desktop screen (1440 x 900px) for DealFlow AI Demo Mode. This page shows everything pre-loaded — no upload needed.

BACKGROUND: #080D1A full frame

NAVIGATION BAR (same style)
Add active indicator on "Demo" nav item

DEMO BANNER (TOP — most prominent)
Position: y=64px, full width Height: 52px Background: rgba(245, 158, 11, 0.08) Border bottom: 1px solid rgba(245, 158, 11, 0.2) Padding: 0 40px Flex: space-between, align center

Left: 🎯 icon 16px #F59E0B + gap 10px "Demo Mode — Pre-loaded with sample procurement documents" Font: Label/Default #F59E0B

Right: "Try with your own documents →" Label/Default #3B7BF6

MAIN CONTENT — SPLIT LAYOUT
Below demo banner, y=116px

Left column (x=0, width=340px): Document list (same as dashboard sidebar)

Right column (x=340px, width=1100px): Full analysis view

RIGHT COLUMN CONTENT
Sub-header (padding 24px 32px): Left: "Sample Procurement Analysis" Display/H3 #F0F4FF + "5 documents · Demo data" Label/Small #4A5878 Right: AMD Badge component

Conflict banner (same as dashboard — show it prominently)

Analysis cards (2x2 grid, same as dashboard) but with mock data clearly shown

Below the grid — CHAT PREVIEW SECTION: Background: #0D1528 Border: 1px solid #1E2D4A Border radius: 12px Padding: 24px Margin top: 20px

Header: Hexagonal AI avatar + "Decision Copilot Preview" Display/H3 #F0F4FF + "See how the AI answers questions" Body/Small #8B9CC8

Show 2 pre-seeded chat exchanges (same as chat screen style) But smaller/compact (Body/Small instead of Body/Default)

Bottom CTA: Background: rgba(59,123,246,0.06) Border: 1px solid rgba(59,123,246,0.15) Border radius: 10px Padding: 20px 24px


"Ready to analyze your own documents?"
Display/H3 #F0F4FF

Two buttons side by side (gap 12px, margin top 16px):
  "Upload Documents" Primary Button
  "Open Full Chat" Ghost Button
═══════════════════════════════════════════
PROMPT 5 — MOBILE SCREENS (375px)
═══════════════════════════════════════════
Create mobile versions (375 x 812px) of:

MOBILE SCREEN 1 — Upload Page
Full dark background #080D1A

Mobile nav (64px height): Logo left: "DealFlow AI" (smaller, 18px) Right: hamburger menu icon #F0F4FF

Hero section (padding 24px, top margin 32px): Badge: "⚡ AMD Hackathon: ACT II" (smaller pill) Headline: "Your documents speak." (DM Sans Bold 36px, centered) Sub-headline: shortened version (14px)

Upload zone (margin 24px, full width, height 200px): Same style but adapted for touch: Replace "drop" text with "Tap to upload" Larger touch target

Stats (horizontal, 3 items, smaller text): < 60s · 5.6x · 100%

MOBILE SCREEN 2 — Chat (full screen)
Mobile nav with back arrow

Document pills (horizontal scroll): Small file chips at top: [PDF] Supplier_A... [PDF] Supplier_B... (scrollable)

Chat takes full screen height

Input bar at bottom (same style, full width)

Quick questions: horizontal scroll chips above input

═══════════════════════════════════════════
PROMPT 6 — PROTOTYPE CONNECTIONS
═══════════════════════════════════════════
Set up Figma prototype connections between all screens:

Landing Page (Screen 1): "Launch App" button → Dashboard (Screen 2) "View Demo" button → Demo Mode (Screen 4) "Try Demo →" button in demo CTA → Demo Mode (Screen 4) Upload zone click → trigger overlay "Processing..." state

Dashboard (Screen 2): "Ask a Question →" button → Chat (Screen 3) "← Upload" breadcrumb → Landing (Screen 1) Conflict "View Details ↓" → expand/collapse toggle "Export PDF" → show overlay "Generating PDF..." toast

Chat (Screen 3): Back arrow → Dashboard (Screen 2) Quick question chips → show response (overlay or variant) "Export Chat as PDF" → toast notification

Demo Mode (Screen 4): "Upload Documents" → Landing (Screen 1) "Open Full Chat" → Chat (Screen 3)

Set prototype: Transition: Smart Animate Duration: 300ms Easing: Ease Out Start screen: Landing Page

FIGMA MAKE USAGE ORDER
Send prompts in this exact order:

PROMPT 0 → Design System (creates shared styles + components)
PROMPT 1 → Landing/Upload Page
PROMPT 2 → Analysis Dashboard
PROMPT 3 → Decision Copilot Chat
PROMPT 4 → Demo Mode
PROMPT 5 → Mobile Screens
PROMPT 6 → Prototype Connections
After each prompt, verify the screen looks correct before moving to the next prompt.

If Figma Make misses a detail, paste the specific section again with "Fix this specific element: [detail]"

DealFlow AI — Figma Make Design Prompt v1.0 AMD Developer Hackathon: ACT II 