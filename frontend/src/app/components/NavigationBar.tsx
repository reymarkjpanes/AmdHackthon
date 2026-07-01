import { useState } from "react";
import { Link } from "react-router";
import { Zap, Menu, X } from "lucide-react";

interface NavigationBarProps {
  showDemo?: boolean;
}

export function NavigationBar({ showDemo = true }: NavigationBarProps) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      <nav
        className="w-full flex items-center justify-between safe-top"
        style={{
          background: "rgba(8, 13, 26, 0.95)",
          height: "64px",
          paddingLeft: "clamp(16px, 4vw, 40px)",
          paddingRight: "clamp(16px, 4vw, 40px)",
          boxShadow: "0 1px 3px rgba(0,0,0,0.3)",
          backdropFilter: "blur(8px)",
          position: "sticky",
          top: 0,
          zIndex: 50,
        }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center">
            <span
              style={{
                fontFamily: "DM Sans, sans-serif",
                fontSize: "clamp(18px, 3vw, 22px)",
                color: "#F0F4FF",
                fontWeight: "bold",
                letterSpacing: "-0.02em",
              }}
            >
              Clausify
            </span>
            <span
              style={{
                fontFamily: "DM Sans, sans-serif",
                fontSize: "clamp(18px, 3vw, 22px)",
                color: "#3B7BF6",
                fontWeight: "bold",
                letterSpacing: "-0.02em",
              }}
            >
              AI
            </span>
          </Link>
          <div className="hidden sm:flex">
            <AMDBadge />
          </div>
        </div>

        {/* Desktop buttons */}
        {showDemo && (
          <div className="hidden sm:flex items-center gap-3">
            <Link to="/demo">
              <button
                className="px-4 py-2 h-9 rounded-lg border transition-all"
                style={{
                  background: "transparent",
                  borderColor: "#1E2D4A",
                  color: "#8B9CC8",
                  fontSize: "14px",
                  fontWeight: 500,
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = "#3B7BF6";
                  e.currentTarget.style.color = "#F0F4FF";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = "#1E2D4A";
                  e.currentTarget.style.color = "#8B9CC8";
                }}
              >
                View Demo
              </button>
            </Link>
            <Link to="/">
              <button
                className="px-4 py-2 h-9 rounded-lg transition-all"
                style={{
                  background: "#3B7BF6",
                  color: "#F0F4FF",
                  fontSize: "14px",
                  fontWeight: 500,
                  border: "none",
                  boxShadow: "0 0 20px rgba(59,123,246,0.3)",
                }}
                onMouseOver={(e) => { e.currentTarget.style.background = "#2D6AE0"; }}
                onMouseOut={(e) => { e.currentTarget.style.background = "#3B7BF6"; }}
              >
                Launch App
              </button>
            </Link>
          </div>
        )}

        {/* Mobile hamburger */}
        {showDemo && (
          <button
            className="sm:hidden flex items-center justify-center"
            onClick={() => setMenuOpen(!menuOpen)}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              color: "#F0F4FF",
              padding: "8px",
            }}
            aria-label="Toggle menu"
          >
            {menuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        )}
      </nav>

      {/* Mobile dropdown menu */}
      {showDemo && menuOpen && (
        <div
          className="sm:hidden animate-slideDown"
          style={{
            position: "fixed",
            top: "64px",
            left: 0,
            right: 0,
            background: "rgba(8, 13, 26, 0.98)",
            borderBottom: "1px solid #1E2D4A",
            padding: "16px",
            zIndex: 49,
            display: "flex",
            flexDirection: "column",
            gap: "10px",
          }}
        >
          <AMDBadge />
          <Link to="/demo" onClick={() => setMenuOpen(false)}>
            <button
              className="w-full px-4 py-3 rounded-lg border"
              style={{
                background: "transparent",
                borderColor: "#1E2D4A",
                color: "#8B9CC8",
                fontSize: "15px",
                fontWeight: 500,
                cursor: "pointer",
              }}
            >
              View Demo
            </button>
          </Link>
          <Link to="/" onClick={() => setMenuOpen(false)}>
            <button
              className="w-full px-4 py-3 rounded-lg"
              style={{
                background: "#3B7BF6",
                color: "#F0F4FF",
                fontSize: "15px",
                fontWeight: 500,
                border: "none",
                cursor: "pointer",
                boxShadow: "0 0 20px rgba(59,123,246,0.3)",
              }}
            >
              Launch App
            </button>
          </Link>
        </div>
      )}
    </>
  );
}

export function AMDBadge() {
  return (
    <div
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-full"
      style={{
        background: "rgba(237, 28, 36, 0.08)",
        border: "1px solid rgba(237, 28, 36, 0.20)",
        height: "26px",
      }}
    >
      <Zap size={12} style={{ color: "#ED1C24" }} />
      <span
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: "12px",
          color: "#ED1C24",
          fontWeight: 500,
          lineHeight: "16px",
          whiteSpace: "nowrap",
        }}
      >
        AMD MI300X
      </span>
    </div>
  );
}
