export interface UploadedDocument {
  id: string;
  filename: string;
  fileType: string;
  fileSize: number;
  uploadedAt: string;
  processingStatus: string;
}

export interface UploadResponse {
  sessionId: string;
  documents: UploadedDocument[];
  message: string;
}

export interface Risk {
  id: string;
  level: 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  sourceDocument: string;
  category: string;
}

export interface Conflict {
  id: string;
  type: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  documentA: { name: string; excerpt: string };
  documentB: { name: string; excerpt: string };
  explanation: string;
  recommendedAction: string;
}

export interface ComparisonRow {
  field: string;
  values: Record<string, string>;
  winner: string;
}

export interface Recommendation {
  title: string;
  summary: string;
  nextSteps: string[];
  confidence: number;
}

export interface Analysis {
  analyzedAt: string;
  executiveSummary: string;
  risks: Risk[];
  comparisonMatrix: ComparisonRow[];
  conflicts: Conflict[];
  recommendation: Recommendation;
  suggestedQuestions?: string[];
}

export interface AnalyzeResponse {
  sessionId: string;
  status: string;
  analysis: Analysis;
}

export interface Evidence {
  quote: string;
  sourceDocument: string;
  documentType: string;
}

export interface StructuredAIResponse {
  answer: string;
  evidence: Evidence[];
  risks: string;
  recommendation: string;
}

export interface ChatResponse {
  messageId: string;
  role: string;
  structuredResponse: StructuredAIResponse;
  processingTimeMs: number;
}

export interface PreSeededMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  structuredResponse?: StructuredAIResponse;
}

export interface DemoResponse {
  sessionId: string;
  documents: UploadedDocument[];
  analysis: Analysis;
  preSeededMessages: PreSeededMessage[];
}
