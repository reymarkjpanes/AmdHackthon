# Components Directory

This directory contains all React components for the Clausify AI frontend.

## Structure

```
components/
├── upload/         # Document upload components (DropZone, FileList, etc.)
├── dashboard/      # Analysis dashboard components (ExecutiveSummary, RiskPanel, etc.)
├── chat/           # Decision Copilot chat components (ChatInterface, MessageBubble, etc.)
├── shared/         # Shared components (AMDBadge, RiskBadge, Navigation, etc.)
└── ui/             # shadcn/ui base components (Button, Card, Input, etc.)
```

## Component Guidelines

- Use TypeScript for all components
- Follow the design system defined in Tailwind config
- Implement proper prop types with TypeScript interfaces
- Add JSDoc comments for complex component logic
- Use Framer Motion for animations
- Follow accessibility best practices (WCAG AA)
