import { AlertCircle, AlertTriangle, Info, FileText } from "lucide-react";

interface RiskBadgeProps {
  variant: 'HIGH' | 'MEDIUM' | 'LOW';
}

export function RiskBadge({ variant }: RiskBadgeProps) {
  const styles = {
    HIGH: {
      background: 'rgba(237, 28, 36, 0.12)',
      border: '1px solid rgba(237, 28, 36, 0.25)',
      color: 'var(--amd-signal)'
    },
    MEDIUM: {
      background: 'rgba(245, 166, 35, 0.12)',
      border: '1px solid rgba(245, 166, 35, 0.25)',
      color: 'var(--caution)'
    },
    LOW: {
      background: 'rgba(0, 196, 140, 0.12)',
      border: '1px solid rgba(0, 196, 140, 0.25)',
      color: 'var(--cleared)'
    }
  };

  const icons = {
    HIGH: <AlertCircle size={12} style={{ flexShrink: 0 }} />,
    MEDIUM: <AlertTriangle size={12} style={{ flexShrink: 0 }} />,
    LOW: <Info size={12} style={{ flexShrink: 0 }} />,
  };

  const style = styles[variant];

  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded" style={{
      background: style.background,
      border: style.border,
      color: style.color,
      fontFamily: "'Inter', sans-serif",
      fontSize: '11px',
      fontWeight: 600,
      lineHeight: '16px',
      letterSpacing: '0.08em',
      textTransform: 'uppercase'
    }}>
      {icons[variant]}
      {variant}
    </span>
  );
}

interface EvidenceTagProps {
  filename: string;
}

export function EvidenceTag({ filename }: EvidenceTagProps) {
  return (
    <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md" style={{
      background: 'var(--graphite)',
      border: '1px solid var(--rule)',
      height: '28px'
    }}>
      <FileText size={12} style={{ color: 'var(--ghost)', flexShrink: 0 }} />
      <span style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: '11px',
        color: 'var(--ash)',
        lineHeight: '16px',
        maxWidth: '200px',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
        display: 'inline-block',
      }}>
        {filename}
      </span>
    </div>
  );
}

interface EvidenceBoxProps {
  quote: string;
  className?: string;
  style?: React.CSSProperties;
}

export function EvidenceBox({ quote, className = '', style = {} }: EvidenceBoxProps) {
  return (
    <div
      className={className}
      style={{
        background: 'var(--parchment)',
        color: 'var(--lead)',
        fontFamily: "'JetBrains Mono', monospace",
        fontWeight: 400,
        fontSize: '12px',
        lineHeight: '18px',
        borderRadius: '4px',
        padding: '12px',
        ...style
      }}
    >
      &ldquo;{quote}&rdquo;
    </div>
  );
}
