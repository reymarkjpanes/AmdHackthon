import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  style?: React.CSSProperties;
  hoverable?: boolean;
}

export function Card({ children, className = '', style = {}, hoverable = true }: CardProps) {
  // Store original border to restore on mouse out
  const originalBorder = (style.border as string | undefined) ?? '1px solid #1E2D4A';

  return (
    <div
      className={`rounded-xl p-6 ${className}`}
      style={{
        background: '#0D1528',
        border: originalBorder,
        transition: hoverable ? 'border-color 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease' : undefined,
        ...style,
      }}
      onMouseOver={(e) => {
        if (hoverable) {
          e.currentTarget.style.borderColor = 'rgba(59, 123, 246, 0.4)';
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 8px 32px rgba(59,123,246,0.08)';
        }
      }}
      onMouseOut={(e) => {
        if (hoverable) {
          // Extract color from the original border string
          const match = originalBorder.match(/1px solid (.+)/);
          e.currentTarget.style.borderColor = match ? match[1] : '#1E2D4A';
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = 'none';
        }
      }}
    >
      {children}
    </div>
  );
}
