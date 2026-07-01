import { ButtonHTMLAttributes } from 'react';

interface PrimaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  small?: boolean;
}

export function PrimaryButton({ children, small = false, disabled, ...props }: PrimaryButtonProps) {
  return (
    <button
      className="rounded-lg transition-all"
      disabled={disabled}
      style={{
        background: disabled ? '#1E2D4A' : '#3B7BF6',
        color: disabled ? '#4A5878' : '#F0F4FF',
        fontSize: '14px',
        fontWeight: 500,
        lineHeight: '20px',
        padding: small ? '8px 16px' : '12px 24px',
        height: small ? '36px' : '44px',
        border: 'none',
        boxShadow: disabled ? 'none' : '0 0 20px rgba(59, 123, 246, 0.3)',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1,
        transition: 'background 0.15s, box-shadow 0.15s, opacity 0.15s',
      }}
      onMouseOver={(e) => {
        if (!disabled) e.currentTarget.style.background = '#2D6AE0';
      }}
      onMouseOut={(e) => {
        if (!disabled) e.currentTarget.style.background = '#3B7BF6';
      }}
      {...props}
    >
      {children}
    </button>
  );
}

interface GhostButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  small?: boolean;
}

export function GhostButton({ children, small = false, disabled, ...props }: GhostButtonProps) {
  return (
    <button
      className="rounded-lg border transition-all"
      disabled={disabled}
      style={{
        background: 'transparent',
        borderColor: disabled ? '#111E35' : '#1E2D4A',
        color: disabled ? '#4A5878' : '#8B9CC8',
        fontSize: '14px',
        fontWeight: 500,
        lineHeight: '20px',
        padding: small ? '8px 16px' : '12px 24px',
        height: small ? '36px' : '44px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        transition: 'border-color 0.15s, color 0.15s, opacity 0.15s',
      }}
      onMouseOver={(e) => {
        if (!disabled) {
          e.currentTarget.style.borderColor = '#3B7BF6';
          e.currentTarget.style.color = '#F0F4FF';
        }
      }}
      onMouseOut={(e) => {
        if (!disabled) {
          e.currentTarget.style.borderColor = '#1E2D4A';
          e.currentTarget.style.color = '#8B9CC8';
        }
      }}
      {...props}
    >
      {children}
    </button>
  );
}
