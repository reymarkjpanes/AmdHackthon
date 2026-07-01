import { AlertCircle, AlertTriangle, Info, FileText } from "lucide-react";

interface RiskBadgeProps {
  variant: 'HIGH' | 'MEDIUM' | 'LOW';
}

export function RiskBadge({ variant }: RiskBadgeProps) {
  const styles = {
    HIGH: {
      background: 'rgba(239, 68, 68, 0.12)',
      border: '1px solid rgba(239, 68, 68, 0.25)',
      color: '#EF4444'
    },
    MEDIUM: {
      background: 'rgba(245, 158, 11, 0.12)',
      border: '1px solid rgba(245, 158, 11, 0.25)',
      color: '#F59E0B'
    },
    LOW: {
      background: 'rgba(16, 185, 129, 0.12)',
      border: '1px solid rgba(16, 185, 129, 0.25)',
      color: '#10B981'
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
      fontFamily: 'Inter, sans-serif',
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
      background: '#111E35',
      border: '1px solid #1E2D4A',
      height: '28px'
    }}>
      <FileText size={12} style={{ color: '#4A5878', flexShrink: 0 }} />
      <span style={{
        fontFamily: 'JetBrains Mono, monospace',
        fontSize: '11px',
        color: '#8B9CC8',
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
