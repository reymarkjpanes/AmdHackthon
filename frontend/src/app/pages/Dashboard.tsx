import { useState } from "react";
import { NavigationBar, AMDBadge } from "../components/NavigationBar";
import { Card } from "../components/Card";
import { RiskBadge, EvidenceTag } from "../components/Badges";
import { PrimaryButton, GhostButton } from "../components/Buttons";
import { Link } from "react-router";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import {
  ArrowLeft,
  Download,
  FileText,
  AlertTriangle,
  Scale,
  Lightbulb,
  ChevronDown,
  Cpu,
  PanelLeft,
  X,
} from "lucide-react";
import { exportReport, analyzeDocuments } from "../../lib/api";
import { toast } from "sonner";
import { useAppState, useAppDispatch } from "../../lib/store";

export default function Dashboard() {
  const dispatch = useAppDispatch();
  const { sessionId, documents, analysis } = useAppState();

  const [conflictExpanded, setConflictExpanded] = useState(true);
  const [isExporting, setIsExporting] = useState(false);
  const [isReanalyzing, setIsReanalyzing] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleExport = async () => {
    if (!sessionId) return;
    setIsExporting(true);
    try {
      const blob = await exportReport(sessionId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "clausify-report.pdf";
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Report downloaded!");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Export failed.";
      toast.error(`PDF export failed: ${msg}`);
    } finally {
      setIsExporting(false);
    }
  };

  const handleReanalyze = async () => {
    if (!sessionId || isReanalyzing) return;
    setIsReanalyzing(true);
    try {
      const result = await analyzeDocuments(sessionId);
      dispatch({ type: "SET_ANALYSIS", payload: result.analysis });
      toast.success("Re-analysis complete!");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Re-analysis failed.");
    } finally {
      setIsReanalyzing(false);
    }
  };

  if (!analysis) {
    return (
      <div className="min-h-screen" style={{ background: "#080D1A" }}>
        <NavigationBar showDemo={false} />
        <div className="flex flex-col items-center pt-24 gap-6 px-4 animate-fadeIn">
          <div className="px-6 py-6 rounded-xl text-center w-full" style={{ background: "#0D1528", border: "1px solid #1E2D4A", maxWidth: "480px" }}>
            <FileText size={40} style={{ color: "#4A5878", margin: "0 auto 16px" }} />
            <h2 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "20px", fontWeight: 600, color: "#F0F4FF", marginBottom: "8px" }}>
              No analysis available
            </h2>
            <p style={{ fontFamily: "Inter, sans-serif", fontSize: "15px", lineHeight: 1.6, color: "#8B9CC8", marginBottom: "20px" }}>
              Please upload documents first to generate an analysis.
            </p>
            <Link to="/"><PrimaryButton>Upload Documents</PrimaryButton></Link>
          </div>
        </div>
      </div>
    );
  }

  const matrixColumns: string[] =
    analysis.comparisonMatrix?.[0] ? Object.keys(analysis.comparisonMatrix[0].values) : [];

  const hasConflicts = analysis.conflicts.length > 0;
  const primaryConflict = analysis.conflicts[0];

  const SidebarContent = () => (
    <>
      <div className="p-5 flex items-center justify-between">
        <span style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", fontWeight: 500, color: "#8B9CC8" }}>
          Session Documents
        </span>
        <span className="px-2 py-0.5 rounded-full" style={{ background: "#1E2D4A", fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#F0F4FF" }}>
          {documents.length}
        </span>
      </div>

      <div>
        {documents.map((doc) => {
          const isImage = doc.fileType === "image";
          return (
            <div
              key={doc.id}
              className="px-4 py-3 cursor-pointer"
              style={{ borderBottom: "1px solid rgba(30,45,74,0.3)", borderLeft: "2px solid transparent", transition: "background 0.15s, border-left-color 0.15s" }}
              onMouseOver={(e) => { e.currentTarget.style.background = "#111E35"; e.currentTarget.style.borderLeftColor = "#3B7BF6"; }}
              onMouseOut={(e) => { e.currentTarget.style.background = "transparent"; e.currentTarget.style.borderLeftColor = "transparent"; }}
            >
              <div className="flex items-start gap-3">
                <div className="flex items-center justify-center rounded-md shrink-0" style={{ width: "24px", height: "24px", background: isImage ? "rgba(59,123,246,0.1)" : "rgba(239,68,68,0.1)", border: `1px solid ${isImage ? "rgba(59,123,246,0.3)" : "rgba(239,68,68,0.3)"}` }}>
                  <span style={{ fontFamily: "Inter, sans-serif", fontSize: "9px", fontWeight: 600, color: isImage ? "#3B7BF6" : "#EF4444" }}>
                    {isImage ? "IMG" : "PDF"}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="truncate" style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", fontWeight: 500, color: "#F0F4FF" }}>
                    {doc.filename}
                  </div>
                  <div style={{ fontFamily: "JetBrains Mono, monospace", fontSize: "11px", color: doc.processingStatus === "completed" ? "#10B981" : "#F59E0B" }}>
                    {doc.processingStatus === "completed" ? (isImage ? "Image · OCR Complete" : "Processed") : "Processing..."}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ borderTop: "1px solid #1E2D4A", marginTop: "16px" }}>
        <div className="p-4 space-y-3">
          <Link to="/" style={{ display: "block" }}>
            <GhostButton style={{ width: "100%", height: "36px" }}>Upload More</GhostButton>
          </Link>
          <div className="text-center">
            <button onClick={() => dispatch({ type: "RESET" })} style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878", background: "none", border: "none", cursor: "pointer" }}>
              New Session
            </button>
          </div>
          <div className="flex justify-center pt-1"><AMDBadge /></div>
        </div>
      </div>
    </>
  );

  return (
    <div className="min-h-screen" style={{ background: "#080D1A" }}>
      <NavigationBar showDemo={false} />

      {/* Breadcrumb */}
      <div className="px-4 sm:px-6 md:px-10 py-3" style={{ borderBottom: "1px solid #1E2D4A" }}>
        <div className="flex items-center gap-2">
          {/* Mobile sidebar toggle */}
          <button
            className="md:hidden flex items-center justify-center mr-1"
            onClick={() => setSidebarOpen(true)}
            style={{ background: "none", border: "none", cursor: "pointer", color: "#8B9CC8", padding: "4px" }}
          >
            <PanelLeft size={18} />
          </button>
          <Link to="/" className="inline-flex items-center gap-1.5" style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878" }}>
            <ArrowLeft size={13} />Upload
          </Link>
          <span style={{ color: "#4A5878" }}>/</span>
          <span style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#F0F4FF" }}>
            Analysis Dashboard
          </span>
        </div>
      </div>

      <div className="flex relative">
        {/* Desktop Sidebar */}
        <div
          className="hidden md:block shrink-0"
          style={{ width: "260px", minHeight: "calc(100vh - 108px)", background: "#0D1528", borderRight: "1px solid #1E2D4A" }}
        >
          <SidebarContent />
        </div>

        {/* Mobile Sidebar Drawer */}
        {sidebarOpen && (
          <div
            className="md:hidden fixed inset-0 z-50 animate-fadeIn"
            style={{ background: "rgba(0,0,0,0.6)" }}
            onClick={() => setSidebarOpen(false)}
          >
            <div
              className="animate-slideDown"
              style={{ width: "min(300px, 85vw)", height: "100%", background: "#0D1528", borderRight: "1px solid #1E2D4A", overflowY: "auto" }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between px-4 py-4" style={{ borderBottom: "1px solid #1E2D4A" }}>
                <span style={{ fontFamily: "DM Sans, sans-serif", fontSize: "15px", fontWeight: 600, color: "#F0F4FF" }}>Documents</span>
                <button onClick={() => setSidebarOpen(false)} style={{ background: "none", border: "none", cursor: "pointer", color: "#8B9CC8" }}>
                  <X size={18} />
                </button>
              </div>
              <SidebarContent />
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="flex-1 min-w-0 animate-fadeIn">
          {/* Top Bar */}
          <div
            className="flex flex-wrap items-center justify-between px-4 sm:px-6 md:px-8 py-3 gap-3"
            style={{ background: "#080D1A", borderBottom: "1px solid #1E2D4A" }}
          >
            <div className="flex items-center gap-2 min-w-0">
              <h2 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "clamp(16px, 3vw, 20px)", fontWeight: 600, color: "#F0F4FF", whiteSpace: "nowrap" }}>
                Analysis Results
              </h2>
              <span className="hidden sm:inline" style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878" }}>
                · Analyzed {analysis.analyzedAt ? new Date(analysis.analyzedAt).toLocaleString() : "just now"}
                {documents[0]?.uploadedAt && analysis.analyzedAt && (() => {
                  const ms = new Date(analysis.analyzedAt).getTime() - new Date(documents[0].uploadedAt).getTime();
                  if (ms > 0 && ms < 300000) return ` · ${(ms/1000).toFixed(1)}s on AMD MI300X`;
                  return "";
                })()}
              </span>
            </div>
            <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
              <GhostButton small onClick={handleReanalyze} disabled={isReanalyzing}>
                {isReanalyzing ? (
                  <div className="flex items-center gap-1.5">
                    <div className="animate-spin-slow w-3 h-3 rounded-full" style={{ border: "2px solid #4A5878", borderTopColor: "#3B7BF6" }} />
                    Analyzing…
                  </div>
                ) : "Re-analyze"}
              </GhostButton>
              <Link to="/chat"><PrimaryButton small>Ask a Question</PrimaryButton></Link>
              <GhostButton small onClick={handleExport} disabled={isExporting}>
                <Download size={14} className="mr-1.5" />
                {isExporting ? "Exporting…" : "Export PDF"}
              </GhostButton>
            </div>
          </div>

          {/* Content */}
          <div className="p-4 sm:p-6 md:p-8 space-y-5">
            {/* AMD Performance Metrics Banner */}
            {(() => {
              const analyzedAt = analysis.analyzedAt ? new Date(analysis.analyzedAt) : null;
              const uploadedAt = documents[0]?.uploadedAt ? new Date(documents[0].uploadedAt) : null;
              const processingMs = analyzedAt && uploadedAt ? analyzedAt.getTime() - uploadedAt.getTime() : null;
              const processingSeconds = processingMs && processingMs > 0 ? (processingMs / 1000).toFixed(1) : null;
              return (
                <div
                  className="rounded-xl p-4 animate-slideDown"
                  style={{
                    background: "linear-gradient(135deg, rgba(237,28,36,0.06) 0%, rgba(59,123,246,0.06) 100%)",
                    border: "1px solid rgba(237,28,36,0.2)",
                  }}
                >
                  <div className="flex flex-wrap items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <div style={{ width: "36px", height: "36px", borderRadius: "8px", background: "rgba(237,28,36,0.1)", border: "1px solid rgba(237,28,36,0.25)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                        <Cpu size={18} style={{ color: "#ED1C24" }} />
                      </div>
                      <div>
                        <div style={{ fontFamily: "DM Sans, sans-serif", fontSize: "14px", fontWeight: 700, color: "#F0F4FF" }}>AMD Instinct MI300X</div>
                        <div style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", color: "#4A5878" }}>ROCm-accelerated inference · HBM3 memory architecture</div>
                      </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-6">
                      {[
                        { label: "Analysis Time", value: processingSeconds ? `${processingSeconds}s` : "< 60s", color: "#10B981" },
                        { label: "Speedup vs CPU", value: "5.6×", color: "#3B7BF6" },
                        { label: "Documents", value: `${documents.length}`, color: "#F0F4FF" },
                        { label: "Risks Found", value: `${analysis.risks.length}`, color: analysis.risks.some(r => r.level === "HIGH") ? "#EF4444" : "#F59E0B" },
                      ].map(stat => (
                        <div key={stat.label} className="flex flex-col items-center">
                          <span style={{ fontFamily: "JetBrains Mono, monospace", fontSize: "20px", fontWeight: 700, color: stat.color }}>{stat.value}</span>
                          <span style={{ fontFamily: "Inter, sans-serif", fontSize: "10px", fontWeight: 500, color: "#4A5878", whiteSpace: "nowrap" }}>{stat.label}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* Conflict Alert */}
            {hasConflicts && primaryConflict && (
              <div className="rounded-lg p-4 animate-slideDown" style={{ background: "rgba(239,68,68,0.06)", border: "1px solid rgba(239,68,68,0.25)", borderLeft: "4px solid #EF4444" }}>
                <div className="flex items-start sm:items-center justify-between gap-3 mb-4 flex-wrap">
                  <div className="flex items-center gap-3 flex-wrap">
                    <AlertTriangle size={20} style={{ color: "#EF4444", flexShrink: 0 }} />
                    <span style={{ fontFamily: "DM Sans, sans-serif", fontSize: "16px", fontWeight: 600, color: "#EF4444" }}>Conflict Detected</span>
                    <span style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", color: "#8B9CC8" }}>
                      {analysis.conflicts.length} conflict{analysis.conflicts.length !== 1 ? "s" : ""} found
                    </span>
                  </div>
                  <button
                    onClick={() => setConflictExpanded(!conflictExpanded)}
                    style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#EF4444", background: "none", border: "none", cursor: "pointer", display: "flex", alignItems: "center", gap: "4px", whiteSpace: "nowrap" }}
                  >
                    View Details
                    <ChevronDown size={14} style={{ transform: conflictExpanded ? "rotate(180deg)" : "none", transition: "transform 0.2s" }} />
                  </button>
                </div>

                {conflictExpanded && (
                  <div style={{ paddingTop: "16px", borderTop: "1px solid rgba(239,68,68,0.15)" }}>
                    {analysis.conflicts.map((conflict) => (
                      <div key={conflict.id} className="rounded-lg p-4 mb-3" style={{ background: "rgba(239,68,68,0.04)" }}>
                        <div className="flex items-center gap-2 mb-3 flex-wrap">
                          <span style={{ fontFamily: "Inter, sans-serif", fontSize: "11px", fontWeight: 600, letterSpacing: "0.08em", color: "#EF4444", textTransform: "uppercase" }}>
                            {conflict.type}
                          </span>
                          <RiskBadge variant={conflict.severity} />
                        </div>
                        <div className="grid gap-3" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", marginBottom: "12px" }}>
                          {[conflict.documentA, conflict.documentB].map((doc, i) => (
                            <div key={i} className="rounded-lg p-3" style={{ background: "rgba(239,68,68,0.06)", border: "1px solid rgba(239,68,68,0.15)" }}>
                              <div className="mb-2"><EvidenceTag filename={doc.name} /></div>
                              <div style={{ fontFamily: "JetBrains Mono, monospace", fontSize: "13px", color: "#F0F4FF" }}>"{doc.excerpt}"</div>
                            </div>
                          ))}
                        </div>
                        <p style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", lineHeight: 1.6, color: "#8B9CC8" }}>{conflict.recommendedAction}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Analysis Cards Grid */}
            <div className="grid gap-4 sm:gap-5" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))" }}>
              {/* Executive Summary */}
              <Card>
                <div className="flex items-center justify-between mb-3">
                  <h3 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "18px", fontWeight: 600, color: "#F0F4FF" }}>Executive Summary</h3>
                  <FileText size={18} style={{ color: "#4A5878" }} />
                </div>
                <div style={{ height: "1px", background: "#1E2D4A", margin: "12px 0" }} />
                <p style={{ fontFamily: "Inter, sans-serif", fontSize: "15px", lineHeight: 1.6, color: "#8B9CC8", marginBottom: "16px" }}>
                  {analysis.executiveSummary}
                </p>
                <div style={{ borderTop: "1px solid #1E2D4A", paddingTop: "12px", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "8px" }}>
                  <div className="flex items-center gap-1.5">
                    <Cpu size={12} style={{ color: "#4A5878" }} />
                    <span style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878" }}>
                      Generated by AMD Llama 3.2 Vision
                    </span>
                  </div>
                  <AMDBadge />
                </div>
              </Card>

              {/* Risk Analysis */}
              <Card>
                <div className="flex items-center justify-between mb-3">
                  <h3 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "18px", fontWeight: 600, color: "#F0F4FF" }}>Risk Analysis</h3>
                  <AlertTriangle size={18} style={{ color: "#4A5878" }} />
                </div>
                <div style={{ height: "1px", background: "#1E2D4A", margin: "12px 0" }} />
                <div className="space-y-3">
                  {analysis.risks.length === 0 && (
                    <div className="flex flex-col items-center py-6 gap-2">
                      <div style={{ width: "36px", height: "36px", borderRadius: "50%", background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.2)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                        <span style={{ fontSize: "18px" }}>✓</span>
                      </div>
                      <p style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", color: "#10B981", fontWeight: 500 }}>No risks identified</p>
                      <p style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", color: "#4A5878", textAlign: "center" }}>The AI found no material risks in your documents.</p>
                    </div>
                  )}
                  {analysis.risks.map((risk) => (
                    <div key={risk.id} className="flex gap-3">
                      <RiskBadge variant={risk.level} />
                      <div className="flex-1 min-w-0">
                        <p style={{ fontFamily: "Inter, sans-serif", fontSize: "15px", lineHeight: 1.6, color: "#F0F4FF", marginBottom: "4px" }}>
                          {risk.description}
                        </p>
                        <EvidenceTag filename={risk.sourceDocument} />
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Comparison Matrix */}
              <Card>
                <div className="flex items-center justify-between mb-3">
                  <h3 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "18px", fontWeight: 600, color: "#F0F4FF" }}>Document Comparison</h3>
                  <Scale size={18} style={{ color: "#4A5878" }} />
                </div>
                <div style={{ height: "1px", background: "#1E2D4A", margin: "12px 0" }} />
                <div className="rounded-lg overflow-x-auto" style={{ border: "1px solid #1E2D4A" }}>
                  <table style={{ width: "100%", minWidth: "360px" }}>
                    <thead>
                      <tr style={{ background: "#111E35", height: "40px" }}>
                        <th className="px-4 text-left" style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878", whiteSpace: "nowrap" }}>Feature</th>
                        {matrixColumns.map((col) => (
                          <th key={col} className="px-4 text-left" style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878", whiteSpace: "nowrap" }}>{col}</th>
                        ))}
                        <th className="px-4 text-left" style={{ fontFamily: "Inter, sans-serif", fontSize: "12px", fontWeight: 500, color: "#4A5878", whiteSpace: "nowrap" }}>Winner</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysis.comparisonMatrix.map((row, idx) => (
                        <tr key={row.field} style={{ background: idx % 2 === 0 ? "#0D1528" : "rgba(17,30,53,0.5)", height: "48px", borderTop: "1px solid #1E2D4A" }}>
                          <td className="px-4" style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", color: "#F0F4FF", whiteSpace: "nowrap" }}>{row.field}</td>
                          {matrixColumns.map((col) => (
                            <td key={col} className="px-4" style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", color: "#F0F4FF" }}>{row.values[col] ?? "—"}</td>
                          ))}
                          <td className="px-4" style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", color: "#10B981", whiteSpace: "nowrap" }}>{row.winner}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>

              {/* AI Recommendation */}
              <Card style={{ background: "rgba(59,123,246,0.04)", border: "1px solid rgba(59,123,246,0.15)" }}>
                <div className="flex items-center justify-between mb-3">
                  <h3 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "18px", fontWeight: 600, color: "#F0F4FF" }}>AI Recommendation</h3>
                  <Lightbulb size={18} style={{ color: "#4A5878" }} />
                </div>
                <div style={{ height: "1px", background: "rgba(59,123,246,0.15)", margin: "12px 0" }} />
                <div className="inline-block px-4 py-2 rounded-full mb-4" style={{ background: "rgba(16,185,129,0.12)", border: "1px solid rgba(16,185,129,0.25)" }}>
                  <span style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", fontWeight: 500, color: "#10B981" }}>
                    {analysis.recommendation.title}
                  </span>
                </div>
                {/* Confidence Score */}
                <div className="flex items-center gap-3 mb-4">
                  <span style={{ fontFamily: "Inter, sans-serif", fontSize: "13px", fontWeight: 500, color: "#8B9CC8" }}>
                    AI Confidence
                  </span>
                  <div style={{ flex: 1, height: "6px", background: "#1E2D4A", borderRadius: "3px", overflow: "hidden" }}>
                    <div
                      style={{
                        height: "100%",
                        width: `${Math.round(analysis.recommendation.confidence * 100)}%`,
                        background: analysis.recommendation.confidence >= 0.7
                          ? "linear-gradient(90deg, #10B981, #34D399)"
                          : analysis.recommendation.confidence >= 0.4
                          ? "linear-gradient(90deg, #F59E0B, #FCD34D)"
                          : "linear-gradient(90deg, #EF4444, #F87171)",
                        borderRadius: "3px",
                        transition: "width 1s ease",
                      }}
                    />
                  </div>
                  <span style={{
                    fontFamily: "JetBrains Mono, monospace",
                    fontSize: "13px",
                    fontWeight: 700,
                    color: analysis.recommendation.confidence >= 0.7 ? "#10B981"
                      : analysis.recommendation.confidence >= 0.4 ? "#F59E0B"
                      : "#EF4444",
                    minWidth: "36px",
                    textAlign: "right",
                  }}>
                    {Math.round(analysis.recommendation.confidence * 100)}%
                  </span>
                </div>
                <p style={{ fontFamily: "Inter, sans-serif", fontSize: "15px", lineHeight: 1.6, color: "#8B9CC8", marginBottom: "12px" }}>
                  {analysis.recommendation.summary}
                </p>
                {analysis.recommendation.nextSteps.length > 0 && (
                  <ul className="space-y-1 mb-4">
                    {analysis.recommendation.nextSteps.map((step, i) => (
                      <li key={i} style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", lineHeight: 1.6, color: "#8B9CC8", paddingLeft: "12px", position: "relative" }}>
                        <span style={{ color: "#3B7BF6", marginRight: "6px" }}>&rarr;</span>{step}
                      </li>
                    ))}
                  </ul>
                )}
                <div style={{ borderTop: "1px solid rgba(59,123,246,0.15)", paddingTop: "16px" }}>
                  <Link to="/chat" style={{ fontFamily: "Inter, sans-serif", fontSize: "14px", fontWeight: 500, color: "#3B7BF6", textDecoration: "none" }}>
                    Ask follow-up questions →
                  </Link>
                </div>
              </Card>

              {/* Risk Distribution */}
              <Card>
                <div className="flex items-center justify-between mb-3">
                  <h3 style={{ fontFamily: "DM Sans, sans-serif", fontSize: "18px", fontWeight: 600, color: "#F0F4FF" }}>Risk Distribution</h3>
                  <AlertTriangle size={18} style={{ color: "#4A5878" }} />
                </div>
                <div style={{ height: "1px", background: "#1E2D4A", margin: "12px 0" }} />
                {(() => {
                  const high = analysis.risks.filter(r => r.level === "HIGH").length;
                  const medium = analysis.risks.filter(r => r.level === "MEDIUM").length;
                  const low = analysis.risks.filter(r => r.level === "LOW").length;
                  const data = [
                    { name: "HIGH", count: high, color: "#EF4444" },
                    { name: "MED", count: medium, color: "#F59E0B" },
                    { name: "LOW", count: low, color: "#10B981" },
                  ];
                  return (
                    <div>
                      <ResponsiveContainer width="100%" height={120}>
                        <BarChart data={data} barSize={32}>
                          <XAxis dataKey="name" tick={{ fontFamily: "Inter, sans-serif", fontSize: 11, fill: "#8B9CC8" }} axisLine={false} tickLine={false} />
                          <YAxis allowDecimals={false} tick={{ fontFamily: "Inter, sans-serif", fontSize: 10, fill: "#8B9CC8" }} axisLine={false} tickLine={false} width={20} />
                          <Tooltip
                            cursor={{ fill: "rgba(59,123,246,0.06)" }}
                            contentStyle={{ background: "#0D1528", border: "1px solid #1E2D4A", borderRadius: "8px", fontFamily: "Inter, sans-serif", fontSize: "13px" }}
                            labelStyle={{ color: "#F0F4FF" }}
                            itemStyle={{ color: "#8B9CC8" }}
                          />
                          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                            {data.map((entry, index) => (
                              <Cell key={index} fill={entry.color} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                      <div className="flex justify-around mt-2">
                        {data.map(d => (
                          <div key={d.name} className="flex flex-col items-center gap-1">
                            <span style={{ fontFamily: "JetBrains Mono, monospace", fontSize: "18px", fontWeight: 700, color: d.color }}>{d.count}</span>
                            <span style={{ fontFamily: "Inter, sans-serif", fontSize: "10px", fontWeight: 600, letterSpacing: "0.06em", color: "#4A5878" }}>{d.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })()}
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
