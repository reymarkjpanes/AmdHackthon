# Requirements Document

## Introduction

DealFlow AI is an AMD-accelerated enterprise document intelligence platform designed for business document analysis and decision support. The frontend provides a dark, corporate Bloomberg Terminal-style interface for uploading documents, viewing AI-powered analysis results, detecting conflicts across documents, and engaging with a decision copilot chat interface. The application targets enterprise users participating in the AMD Developer Hackathon: ACT II and must deliver a premium, technically impressive, and human-centered user experience.

All icons in this document refer to Google Material Symbols (outlined style) loaded via the `material-symbols` font. No emoji characters are used anywhere in the UI.

## Glossary

- **System**: The DealFlow AI frontend web application
- **User**: An enterprise user analyzing business documents (contracts, quotations, invoices)
- **Document**: A PDF, PNG, JPG, or JPEG file uploaded by the User
- **Session**: A collection of uploaded Documents being analyzed together
- **Analysis**: AI-generated insights including executive summary, risks, comparison matrix, and recommendations
- **Conflict**: A detected discrepancy or contradiction between information in different Documents
- **Evidence_Tag**: A clickable UI element that references a source Document for a piece of information
- **Decision_Copilot**: The AI chat interface that answers User questions about uploaded Documents
- **Demo_Mode**: A pre-loaded demonstration with sample Documents and Analysis results
- **Upload_Zone**: The drag-and-drop file upload interface component
- **Dashboard**: The page displaying Analysis results and detected Conflicts
- **AMD_Badge**: A UI component displaying "Powered by AMD MI300X" branding

## Requirements

### Requirement 1: Document Upload Interface

**User Story:** As a User, I want to upload business documents through a drag-and-drop interface, so that I can quickly initiate document analysis without navigating complex file selection dialogs.

#### Acceptance Criteria

1. THE Upload_Zone SHALL accept PDF, PNG, JPG, and JPEG file formats
2. THE Upload_Zone SHALL accept up to 10 files per upload operation
3. THE Upload_Zone SHALL enforce a maximum file size of 10MB per Document
4. WHEN a User drags a file over the Upload_Zone, THE System SHALL provide visual feedback by changing the border color to electric blue (#3B7BF6) and adding a glow effect
5. WHEN a User drops files into the Upload_Zone, THE System SHALL display each uploaded Document with a `description` icon (Google Material Symbol), filename, human-readable file size (e.g. "2.1 MB"), and processing status
6. WHEN all uploaded Documents are successfully processed, THE System SHALL display an "Analyze Documents" button with a pulsing glow animation
7. IF a User attempts to upload a file larger than 10MB, THEN THE System SHALL reject the file and display an inline error message: "This file exceeds the 10 MB limit. Please reduce the file size and try again." with an `error` icon
8. IF a User attempts to upload more than 10 files, THEN THE System SHALL reject additional files and display an inline message: "You can upload up to 10 files at a time. Remove a file to add another." with an `info` icon
9. IF a User attempts to upload an unsupported file format, THEN THE System SHALL reject the file and display an inline error: "This file type is not supported. Please upload PDF, PNG, JPG, or JPEG files." with an `error` icon
10. THE Upload_Zone SHALL display a `cloud_upload` icon and instructional text "Drag files here, or click to browse" when no files have been added
11. THE Upload_Zone SHALL be keyboard accessible: pressing Enter or Space while the zone is focused SHALL open the native file browser dialog

### Requirement 2: Landing Page Presentation

**User Story:** As a User, I want to see a clear value proposition and upload interface immediately upon visiting the application, so that I can understand what the platform does and quickly begin using it.

#### Acceptance Criteria

1. THE Landing_Page SHALL display the main headline "Your documents speak. We translate them into decisions." in DM Sans 700 at 56px desktop / 36px mobile
2. THE Landing_Page SHALL display a sub-headline in Inter 400 at 20px explaining AMD MI300X acceleration and multi-document analysis
3. THE Landing_Page SHALL display three performance statistics in labeled cards: "Under 60 seconds" for analysis time, "5.6x faster than CPU" for speed, and "100% source-cited" for evidence quality
4. THE Landing_Page SHALL display the Upload_Zone as the primary interactive element, vertically centered below the headline
5. THE Landing_Page SHALL display a "How It Works" section with three numbered steps: "Upload your documents", "AI analyzes everything", and "Make better decisions" — each step uses a `looks_one`, `looks_two`, `looks_three` icon respectively
6. THE Landing_Page SHALL display an AMD_Badge with "Powered by AMD MI300X" text and a `bolt` icon
7. THE Landing_Page SHALL display a "View Demo" text button in the top navigation and a "Launch App" filled button that links to the upload page
8. THE Landing_Page SHALL display a trust banner with the text: "Running on AMD Instinct MI300X — ROCm-powered embeddings — Enterprise-grade inference"

### Requirement 3: Analysis Dashboard Display

**User Story:** As a User, I want to view comprehensive analysis results in a structured dashboard, so that I can quickly understand key insights, risks, and recommendations from my uploaded documents.

#### Acceptance Criteria

1. THE Dashboard SHALL display a sidebar listing all uploaded Documents with a `picture_as_pdf` icon for PDFs and `image` icon for images, plus filenames and a `check_circle` icon for completed processing
2. THE Dashboard SHALL display four analysis cards in a 2x2 grid: Executive Summary, Risk Analysis, Comparison Matrix, and AI Recommendation
3. THE Dashboard SHALL display analysis timestamps in the format "Analyzed at HH:MM on DD MMM YYYY" below the page header
4. THE Dashboard SHALL display a prominent "Ask a Question" button with a `chat` icon that navigates to the Decision_Copilot
5. THE Dashboard SHALL display an "Export PDF" button with a `download` icon in the top action bar
6. WHEN Analysis results are loaded, THE Dashboard SHALL animate cards in with staggered opacity and translateY transitions: 0ms, 100ms, 200ms, 300ms delays
7. THE Dashboard SHALL display an AMD_Badge component in the bottom of the sidebar
8. THE Dashboard SHALL display an "Add Documents" button with a `add` icon and a "New Session" button with a `refresh` icon in the sidebar footer

### Requirement 4: Conflict Detection and Alert System

**User Story:** As a User, I want to be immediately alerted to conflicts and discrepancies across my uploaded documents, so that I can identify critical issues requiring attention before making business decisions.

#### Acceptance Criteria

1. WHEN Conflicts are detected in the Analysis, THE Dashboard SHALL display a conflict alert banner above the analysis cards with a `warning` icon (Google Material Symbol)
2. THE Conflict_Banner SHALL use rgba(239, 68, 68, 0.08) background and a 3px solid #EF4444 left border
3. THE Conflict_Banner SHALL display a `warning` icon, the text "Conflicts Detected", and the count of detected Conflicts in parentheses (e.g. "Conflicts Detected (2)")
4. THE Conflict_Banner SHALL display a `expand_more` icon when collapsed and `expand_less` when expanded; clicking anywhere on the banner header SHALL toggle the expanded state
5. WHEN expanded, THE Conflict_Banner SHALL display individual Conflict cards each containing: conflict type label, names of both affected Documents, a side-by-side comparison of conflicting excerpts, a severity badge (HIGH / MEDIUM / LOW), and a recommended action in plain language
6. THE Conflict_Banner SHALL animate into view with a slide-down motion from the top using cubic-bezier(0.175, 0.885, 0.32, 1.275) easing over 400ms
7. EACH Conflict card SHALL display two comparison boxes side by side with a `compare_arrows` icon between them, showing the conflicting values with their source Document names

### Requirement 5: Risk Analysis Presentation

**User Story:** As a User, I want to see identified risks categorized by severity level, so that I can prioritize which issues to address first and understand the potential impact of each risk.

#### Acceptance Criteria

1. THE Risk_Analysis_Card SHALL display a list of identified risks from the Analysis, preceded by a `shield` icon in the card header
2. EACH risk item SHALL include a severity badge displaying one of three levels: HIGH, MEDIUM, or LOW
3. THE HIGH severity badge SHALL use text color #EF4444 with rgba(239,68,68,0.15) background and a `priority_high` icon
4. THE MEDIUM severity badge SHALL use text color #F59E0B with rgba(245,158,11,0.15) background and a `warning_amber` icon
5. THE LOW severity badge SHALL use text color #10B981 with rgba(16,185,129,0.15) background and a `info` icon
6. EACH risk item SHALL include a one-sentence description of the risk and an Evidence_Tag referencing the source Document
7. THE Risk_Analysis_Card SHALL display risks in descending severity order: HIGH first, then MEDIUM, then LOW
8. IF no risks are detected, THE Risk_Analysis_Card SHALL display the text "No significant risks detected" with a `check_circle` icon in #10B981

### Requirement 6: Comparison Matrix Display

**User Story:** As a User, I want to see a side-by-side comparison of key information across multiple documents, so that I can quickly evaluate differences and identify the best options.

#### Acceptance Criteria

1. THE Comparison_Matrix_Card SHALL display a data table with rows representing comparison fields and columns representing Documents, with a `table_chart` icon in the card header
2. THE Comparison_Matrix SHALL highlight cells with favorable values using #10B981 text and rgba(16,185,129,0.1) background
3. THE Comparison_Matrix SHALL highlight cells with unfavorable values using #EF4444 text and rgba(239,68,68,0.1) background
4. THE Comparison_Matrix SHALL use alternating row backgrounds (#0D1528 and #111E35) for improved readability
5. THE Comparison_Matrix SHALL include fields relevant to the Document types (e.g., Price, Payment Terms, Delivery Time, Warranty, Support SLA)
6. THE Comparison_Matrix SHALL display a `workspace_premium` icon in the winning column header to indicate the recommended option
7. IF only one Document is uploaded, THE Comparison_Matrix_Card SHALL display a message: "Upload more documents to compare" with a `add_circle` icon

### Requirement 7: Decision Copilot Chat Interface

**User Story:** As a User, I want to ask questions in natural language about my uploaded documents and receive evidence-based answers, so that I can get specific information without manually searching through all documents.

#### Acceptance Criteria

1. THE Decision_Copilot SHALL display a split layout: a 320px Document_Context_Panel on the left and the chat area on the right
2. THE Document_Context_Panel SHALL list all active Documents in the Session with appropriate file type icons (`picture_as_pdf` or `image`)
3. THE Document_Context_Panel SHALL display a "Quick Questions" section with clickable question chips below the document list
4. THE Chat_Interface SHALL display conversation history with User messages right-aligned in #1E2D4A background bubbles and AI messages left-aligned in #0D1528 background bubbles
5. THE Chat_Interface SHALL display a textarea input with placeholder text "Ask anything about your documents…"
6. THE Chat_Interface SHALL display a `send` icon button to submit the message, and an `attach_file` icon button for future file attachment (disabled state acceptable for v1)
7. WHEN the chat has no messages, THE Chat_Interface SHALL display a centered empty state with a `forum` icon, the heading "Ask me anything", sub-text "Your documents are ready. Ask about risks, terms, or get a recommendation.", and the Quick Question chips
8. THE Chat_Interface header SHALL display an "Export Chat" button with a `download` icon

### Requirement 8: AI Response Formatting and Structure

**User Story:** As a User, I want AI responses to be clearly structured with labeled sections for answers, evidence, risks, and recommendations, so that I can quickly find the specific information I need and verify its sources.

#### Acceptance Criteria

1. EACH AI message SHALL contain four clearly labeled sections rendered in sequence: ANSWER, EVIDENCE, RISK, and RECOMMENDATION
2. THE ANSWER section SHALL use a `chat_bubble` section label icon and display the direct response in primary text color (#F0F4FF)
3. THE EVIDENCE section SHALL use a `format_quote` section label icon and display quoted excerpts from Documents with Evidence_Tag components
4. THE RISK section SHALL use a `warning` section label icon and display risk-related text in amber (#F59E0B)
5. THE RECOMMENDATION section SHALL use a `lightbulb` section label icon and display actionable next steps in blue (#3B7BF6)
6. THE AI message bubble SHALL have a 3px solid #3B7BF6 left border to visually distinguish it from user messages
7. THE AI message bubble SHALL use #0D1528 background with #1E2D4A border
8. EACH Evidence_Tag SHALL display a `description` icon and the Document filename in JetBrains Mono font
9. EACH Evidence_Tag SHALL be keyboard focusable; on hover the border SHALL change to #3B7BF6; on click it SHALL scale briefly to 0.97 and emit an event for potential document preview

### Requirement 9: AI Chat Animation and Streaming

**User Story:** As a User, I want to see visual feedback indicating when the AI is processing my question and see responses appear progressively, so that I know the system is working and can begin reading answers before the full response is complete.

#### Acceptance Criteria

1. WHEN the AI is processing a User question, THE Chat_Interface SHALL display a hexagonal AI avatar with a pulsing blue ring animation (keyframe: opacity 1→0.3→1, scale 1→1.2→1, 1.5s infinite)
2. WHEN the AI is processing, THE Chat_Interface SHALL display three dots animating in a wave pattern with a blue (#3B7BF6) glow effect below the avatar
3. WHEN the AI is processing, THE Chat_Interface SHALL display the label "Processing with AMD MI300X..." in #8B9CC8 below the three-dot animation — no icons, no emojis
4. WHEN the AI response begins streaming, THE Chat_Interface SHALL reveal the ANSWER section text word-by-word with 20ms delay between each word
5. WHEN streaming text, THE System SHALL display a blinking cursor (1px wide, #3B7BF6 color, 500ms blink rate) at the end of the current text
6. THE ANSWER section SHALL begin streaming immediately when the response begins
7. THE EVIDENCE section SHALL fade in 200ms after the ANSWER section completes streaming
8. THE RISK section SHALL fade in 200ms after the EVIDENCE section appears
9. THE RECOMMENDATION section SHALL fade in 200ms after the RISK section appears
10. WHEN all streaming is complete, THE blinking cursor SHALL fade out after 500ms

### Requirement 10: Demo Mode with Pre-loaded Content

**User Story:** As a User, I want to try the platform with sample documents without uploading my own files, so that I can quickly understand the platform's capabilities and evaluate its usefulness.

#### Acceptance Criteria

1. THE Demo_Mode page SHALL pre-populate the session with five sample procurement Documents, requiring no file upload from the User
2. THE Demo_Mode SHALL display an amber notification banner at the top of the page with an `info` icon and the text: "Demo Mode — Pre-loaded with sample procurement documents"
3. THE Demo_Mode SHALL include the following sample Documents: Supplier_A_Quotation.pdf, Supplier_B_Quotation.pdf, Existing_Contract_TechCorp.pdf, Invoice_TechCorp_March2026.pdf, and Company_Procurement_Policy.pdf
4. THE Demo_Mode Dashboard SHALL display pre-computed Analysis results covering executive summary, risk list, Conflicts, comparison matrix, and recommendation
5. THE Demo_Mode SHALL surface at least one HIGH severity Conflict: invoice total ($48,500) versus quotation total ($45,200) — a $3,300 discrepancy
6. THE Demo_Mode chat SHALL pre-seed 2 to 3 conversation exchanges that demonstrate the Decision_Copilot's answer, evidence, risk, and recommendation structure
7. THE Demo_Mode SHALL allow Users to type and submit additional questions; responses SHALL be simulated with a realistic 800ms delay and contextually relevant content
8. THE Demo_Mode SHALL display a persistent "Try with your own documents" link with a `arrow_forward` icon that navigates to the main upload page

### Requirement 11: Design System Color Palette

**User Story:** As a User, I want a consistent, professional dark theme throughout the application, so that the interface feels cohesive and suitable for corporate enterprise use.

#### Acceptance Criteria

1. THE System SHALL use #080D1A as the primary page background color
2. THE System SHALL use #0D1528 as the secondary background for cards, panels, and AI message bubbles
3. THE System SHALL use #111E35 for card and interactive element hover states
4. THE System SHALL use #1E2D4A for borders, dividers, and user message bubble backgrounds
5. THE System SHALL use #3B7BF6 as the primary accent color for interactive elements, focus rings, and active states
6. THE System SHALL use #F0F4FF for primary text (headings, body)
7. THE System SHALL use #8B9CC8 for secondary text (labels, timestamps, captions)
8. THE System SHALL use #10B981 for success states, #F59E0B for warning states, and #EF4444 for danger/error states
9. THE System SHALL use #ED1C24 (AMD red) only for AMD_Badge components and AMD branding elements

### Requirement 12: Typography System

**User Story:** As a User, I want clear, readable text with appropriate font hierarchy, so that I can easily distinguish headings from body text and navigate the information architecture with confidence.

#### Acceptance Criteria

1. THE System SHALL use "DM Sans" font family for all headings and hero text
2. THE System SHALL use "Inter" font family for all body copy, labels, and UI text
3. THE System SHALL use "JetBrains Mono" font family for code snippets, data values, and document quote text in Evidence_Tags
4. THE System SHALL load DM Sans with weights 300, 400, 500, 600, and 700 via Google Fonts
5. THE System SHALL load Inter with weights 400, 500, and 600 via Google Fonts
6. THE System SHALL load JetBrains Mono with weights 400 and 500 via Google Fonts
7. THE System SHALL load Google Material Symbols (outlined) via the Google Fonts icon CDN for all icons throughout the application

### Requirement 13: Responsive Layout and Breakpoints

**User Story:** As a User, I want the application to adapt to my screen size, so that I can access the platform effectively whether I am on a desktop workstation, a laptop, a tablet, or my phone.

#### Acceptance Criteria

1. WHEN the viewport width is 1280px or greater, THE System SHALL display the full desktop layout with full-width sidebars and 2x2 analysis card grids
2. WHEN the viewport width is between 1024px and 1279px, THE System SHALL narrow sidebars to 240px width
3. WHEN the viewport width is between 768px and 1023px, THE System SHALL collapse sidebars to icon-only width (56px) with a `chevron_right` icon to expand them
4. WHEN the viewport width is below 768px, THE System SHALL display single-column layouts and convert sidebars to bottom sheets accessible via a `menu` icon
5. WHEN on a mobile viewport, THE Chat_Interface SHALL occupy the full screen width with the Document_Context_Panel accessible as a bottom sheet
6. WHEN on a mobile viewport, THE Upload_Zone SHALL expand to full width

### Requirement 14: Page Load Animations

**User Story:** As a User, I want smooth, purposeful animations when pages load, so that the application feels polished and the content hierarchy is visually communicated.

#### Acceptance Criteria

1. WHEN a page loads, THE navigation bar SHALL become visible immediately (0ms delay)
2. WHEN a page loads, THE hero text SHALL fade in with a 100ms delay
3. WHEN a page loads, THE Upload_Zone SHALL fade in with a 200ms delay
4. WHEN a page loads, THE statistics section SHALL fade in with a 300ms delay
5. EACH page load animation SHALL transition opacity from 0 to 1 and translateY from 16px to 0
6. EACH page load animation SHALL use a 500ms duration with ease-out easing
7. THE System SHALL respect the User's OS-level `prefers-reduced-motion` setting by disabling all entrance animations when motion reduction is preferred

### Requirement 15: File Processing Status Display

**User Story:** As a User, I want to see real-time progress of document processing, so that I understand what the system is doing and can estimate how long the analysis will take.

#### Acceptance Criteria

1. WHEN Documents are being processed, THE System SHALL display a progress row for each Document within the file list
2. THE progress row SHALL show the following ordered steps: "File received", "Text extracted", "OCR completed" (images only), "Generating embeddings", "Indexing to knowledge base"
3. EACH completed step SHALL display a `check_circle` icon in #10B981
4. THE currently active step SHALL display a circular animated spinner icon using `sync` with a CSS rotation animation in #3B7BF6
5. EACH pending step SHALL display a `radio_button_unchecked` icon in #8B9CC8
6. EACH step label SHALL fade in as it transitions to completed state (200ms opacity transition)
7. WHEN all steps are complete, THE Document row SHALL display a "Processed" label with a `check_circle` icon in #10B981 — no text symbols or emojis

### Requirement 16: Navigation and Routing

**User Story:** As a User, I want clear, consistent navigation between sections of the application, so that I can move between uploading, viewing analysis, chatting, and exploring the demo without losing my place.

#### Acceptance Criteria

1. THE System SHALL provide a route at "/" for the Landing and Upload page
2. THE System SHALL provide a route at "/dashboard" for the Analysis Dashboard
3. THE System SHALL provide a route at "/chat" for the Decision Copilot chat interface
4. THE System SHALL provide a route at "/demo" for Demo Mode
5. THE top navigation bar SHALL include a "View Demo" ghost button with a `play_circle` icon
6. THE top navigation bar SHALL include a "Launch App" filled button with a `rocket_launch` icon
7. THE Dashboard SHALL display an "Ask a Question" button with a `chat` icon that links to "/chat"
8. WHEN navigating from the Dashboard to "/chat", THE Chat_Interface SHALL load with the current Session's Documents pre-populated in the Document_Context_Panel

### Requirement 17: AMD Branding Integration

**User Story:** As a User, I want to clearly see that the platform is powered by AMD technology, so that I understand the technical foundation and can appreciate the acceleration benefits.

#### Acceptance Criteria

1. THE top navigation bar SHALL display an AMD_Badge with "Powered by AMD MI300X" text and a `bolt` icon in #ED1C24
2. THE Landing_Page trust banner SHALL include the text "AMD Instinct MI300X" and "ROCm-powered embeddings"
3. THE Dashboard sidebar footer SHALL display a compact AMD_Badge
4. EACH Analysis card footer SHALL display a "Generated by AMD LLM" label in #8B9CC8 with a `bolt` icon in #ED1C24
5. THE AI thinking animation label SHALL read "Processing with AMD MI300X..." — displayed in #8B9CC8 plain text, no icons in this label
6. THE AMD_Badge component SHALL use #ED1C24 text color with rgba(237, 28, 36, 0.08) background
7. THE AMD_Badge component SHALL always include the `bolt` icon (Google Material Symbol) preceding the text

### Requirement 18: Interaction Micro-animations

**User Story:** As a User, I want interactive elements to respond immediately and naturally to my actions, so that the interface feels alive and I receive clear confirmation that my interactions are registered.

#### Acceptance Criteria

1. WHEN a User hovers over any button, THE button SHALL respond within 150ms with a background lightening of 10% or a subtle box-shadow glow
2. WHEN a User hovers over the Upload_Zone, THE Upload_Zone SHALL scale to 1.01 and display a #3B7BF6 box-shadow glow (transition: 200ms ease)
3. WHEN a User hovers over an Evidence_Tag, THE Evidence_Tag border SHALL transition to #3B7BF6 within 150ms
4. WHEN a User clicks an Evidence_Tag, THE Evidence_Tag SHALL scale to 0.97 for 100ms then return to 1.0
5. WHEN all Documents are ready to analyze, THE "Analyze Documents" button SHALL display a continuous pulsing glow: box-shadow animates from 0px to 20px blur with rgba(59,123,246,0.4), 2s ease-in-out infinite
6. WHEN a User sends a message, THE User message bubble SHALL slide in from translateX(20px) to translateX(0) over 300ms ease-out
7. WHEN an AI response appears, THE AI message bubble SHALL slide in from translateX(-20px) to translateX(0) over 300ms ease-out
8. THE System SHALL respect `prefers-reduced-motion` by replacing all transforms with a simple opacity fade when motion reduction is preferred

### Requirement 19: Document Context Management

**User Story:** As a User, I want the system to maintain awareness of which documents are active in my session across different pages, so that I can navigate freely between analysis and chat without losing context.

#### Acceptance Criteria

1. THE System SHALL maintain a Session state object containing all uploaded Documents and their metadata
2. THE Session state SHALL persist without loss when the User navigates between the Dashboard and the Chat page
3. THE Dashboard sidebar SHALL display all Documents in the current Session
4. THE Chat Document_Context_Panel SHALL display all Documents in the current Session
5. THE System SHALL allow Users to add more Documents to an existing Session from the Dashboard sidebar via the "Add Documents" button
6. THE System SHALL allow Users to start a new Session via the "New Session" button, which clears all existing Documents and Analysis
7. WHEN a User clicks "New Session" and an Analysis exists, THE System SHALL display a confirmation dialog with a `warning` icon and the text: "Starting a new session will clear your current analysis. This cannot be undone." with "Cancel" and "Start New Session" actions

### Requirement 20: Export and Reporting

**User Story:** As a User, I want to export analysis results and chat conversations to PDF, so that I can share findings with stakeholders and maintain a record of my analysis.

#### Acceptance Criteria

1. THE Dashboard top bar SHALL display an "Export PDF" button with a `download` icon
2. THE Chat_Interface header SHALL display an "Export Chat" button with a `download` icon
3. WHEN a User clicks "Export PDF" on the Dashboard, THE System SHALL generate a PDF containing: executive summary, risk analysis, comparison matrix, detected conflicts, and recommendation
4. WHEN a User clicks "Export Chat", THE System SHALL generate a PDF containing the full conversation history with User questions and AI responses, preserving section labels (ANSWER, EVIDENCE, RISK, RECOMMENDATION)
5. THE exported PDF SHALL maintain logical reading order and visual hierarchy matching the on-screen layout
6. THE exported PDF SHALL include the DealFlow AI logo, "Powered by AMD MI300X" label, and a generation timestamp in the footer
7. WHEN the PDF is ready, THE System SHALL trigger a browser file download named "dealflow-analysis-[date].pdf" or "dealflow-chat-[date].pdf"

### Requirement 21: Error Handling and User Feedback

**User Story:** As a User, I want clear, actionable feedback when something goes wrong, so that I understand the problem and know exactly what to do next.

#### Acceptance Criteria

1. IF document upload fails, THEN THE System SHALL display an inline error with an `error` icon and a specific message: "Upload failed — [reason]. Please try again."
2. IF analysis processing fails, THEN THE System SHALL display an error card with an `error` icon, the message "Analysis failed. We couldn't process your documents.", and a "Retry" button with a `refresh` icon
3. IF the chat service is unavailable, THEN THE System SHALL display an inline error within the chat area with a `cloud_off` icon and the message: "Unable to reach the AI service. Check your connection and try again."
4. IF PDF export fails, THEN THE System SHALL display a toast notification with an `error` icon and a "Try again" link
5. ALL error messages SHALL use #EF4444 for the icon and border accent; the message text SHALL use #F0F4FF for readability
6. ALL error messages SHALL provide specific, actionable guidance — never generic messages like "An error occurred"
7. WHEN an error is dismissed or resolved, THE error element SHALL fade out with a 300ms opacity transition

### Requirement 22: API Integration Architecture

**User Story:** As a developer, I want a well-structured API client layer, so that frontend components can easily communicate with backend services and mock data can substitute during development and demo mode.

#### Acceptance Criteria

1. THE System SHALL implement a POST /api/upload endpoint integration that accepts multipart Document files and returns session_id and a documents array
2. THE System SHALL implement a POST /api/analyze endpoint integration that returns Analysis results including executive_summary, risks, comparison_matrix, conflicts, and recommendation
3. THE System SHALL implement a POST /api/chat endpoint integration that accepts a session_id and question, returning a structured response with answer, evidence, risks, and recommendation fields
4. THE System SHALL implement a POST /api/report endpoint integration that returns a PDF binary blob for download
5. THE System SHALL implement a GET /api/demo endpoint integration that returns pre-loaded sample data for Demo_Mode
6. THE System SHALL provide mock implementations for all API endpoints using realistic fake data so the full UI is exercisable without a live backend
7. THE chat API mock SHALL simulate word-by-word streaming using setTimeout at 20ms intervals to demonstrate the streaming UI in development and Demo_Mode

### Requirement 23: Accessibility Compliance Foundation

**User Story:** As a User with accessibility needs, I want the application to follow web accessibility best practices, so that I can navigate and use the platform confidently with assistive technologies.

#### Acceptance Criteria

1. THE System SHALL use semantic HTML5 elements (header, nav, main, section, article, aside) for proper document structure
2. ALL interactive elements SHALL be reachable and operable via keyboard Tab navigation with a visible focus indicator: 2px solid #3B7BF6 outline with 2px offset
3. ALL Google Material Symbol icons that convey meaning SHALL have an accompanying aria-label; decorative icons SHALL have aria-hidden="true"
4. THE color contrast ratio between primary text (#F0F4FF) and primary background (#080D1A) SHALL meet WCAG AA minimum of 4.5:1
5. ALL form inputs SHALL have an associated visible label or an aria-label
6. THE Upload_Zone SHALL be operable via keyboard: Tab to focus, Enter or Space to open the file browser dialog
7. THE System SHALL use aria-live="polite" regions to announce dynamic content changes including new chat messages and analysis completion
8. ALL buttons and links SHALL have descriptive accessible names that convey their purpose without relying on icon-only labeling

### Requirement 24: Performance and Loading States

**User Story:** As a User, I want the application to feel fast and keep me informed during processing, so that I remain confident the system is working and I do not abandon the process.

#### Acceptance Criteria

1. WHILE Documents are being uploaded, THE System SHALL display a linear progress bar per Document showing upload percentage (0–100%)
2. WHILE Analysis is being generated, THE System SHALL display skeleton loading placeholders (animated shimmer) on all four analysis cards
3. WHILE Analysis is being generated, THE System SHALL display a thin animated progress bar at the top of the Dashboard viewport
4. WHILE Analysis is being generated, THE System SHALL cycle through status messages: "Extracting text from documents...", "Generating AMD-accelerated embeddings...", "Running conflict detection...", "Synthesizing analysis..." — each fading in and out over 400ms
5. THE page shell (navigation bar, sidebar structure, card outlines) SHALL render within 1 second of navigation
6. THE System SHALL prioritize above-the-fold content loading; below-the-fold components SHALL use dynamic imports
7. ALL images and non-critical assets SHALL use lazy loading via the Next.js Image component with loading="lazy"

### Requirement 25: Quick Question Functionality

**User Story:** As a User, I want pre-written example questions I can click to send instantly, so that I can get started exploring the AI's capabilities without having to compose questions from scratch.

#### Acceptance Criteria

1. THE Document_Context_Panel SHALL include a "Quick Questions" section header with a `help` icon
2. THE Quick Questions section SHALL display at least 6 question chips: "Which supplier is safest?", "What are the payment terms?", "Any risks I should know about?", "Which option is cheapest?", "What deadlines exist?", and "What information is missing?"
3. EACH quick question chip SHALL be styled as a pill with 4px border-radius, a 1px #1E2D4A border, and #0D1528 background
4. WHEN a User clicks a quick question chip, THE System SHALL immediately populate the chat input field with that question text and submit it without requiring a second action
5. WHEN the chat is in empty state, THE same quick question chips SHALL also appear centered in the main chat area below the empty state message
6. WHEN a User hovers over a quick question chip, THE chip border SHALL transition to #3B7BF6 and the background SHALL lighten to #111E35 within 150ms
