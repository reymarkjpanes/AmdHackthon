import { createBrowserRouter } from "react-router";
import { lazy, Suspense } from "react";
import { motion } from "framer-motion";

// Lazy-loaded page components for code-splitting
const Landing = lazy(() => import("./pages/Landing"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Chat = lazy(() => import("./pages/Chat"));
const Demo = lazy(() => import("./pages/Demo"));

// Professional loading fallback with Clausify branding
function PageLoader() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "var(--ink)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: "24px",
      }}
    >
      {/* Animated Clausify logo mark */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "16px" }}>
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          style={{
            width: "36px",
            height: "36px",
            borderRadius: "8px",
            background: "var(--volt)",
            transform: "rotate(45deg)",
            boxShadow: "0 0 20px rgba(59,123,246,0.3)",
          }}
        />
        <span
          style={{
            fontFamily: "'DM Sans', sans-serif",
            fontSize: "18px",
            fontWeight: 700,
            color: "var(--paper)",
            letterSpacing: "-0.02em",
          }}
        >
          Clausify AI
        </span>
      </div>

      {/* Pulsing dots */}
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <div className="animate-dot-1" style={{ width: "8px", height: "8px", borderRadius: "50%", background: "var(--volt)" }} />
        <div className="animate-dot-2" style={{ width: "8px", height: "8px", borderRadius: "50%", background: "var(--volt)" }} />
        <div className="animate-dot-3" style={{ width: "8px", height: "8px", borderRadius: "50%", background: "var(--volt)" }} />
      </div>

      {/* Shimmer bar */}
      <div style={{ width: "200px", height: "3px", background: "var(--rule)", borderRadius: "2px", overflow: "hidden" }}>
        <div className="shimmer-bar" style={{ height: "100%", borderRadius: "2px", width: "100%" }} />
      </div>
    </div>
  );
}

// Wrap lazy components with Suspense
function SuspenseWrapper({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<PageLoader />}>{children}</Suspense>;
}

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <SuspenseWrapper>
        <Landing />
      </SuspenseWrapper>
    ),
  },
  {
    path: "/dashboard",
    element: (
      <SuspenseWrapper>
        <Dashboard />
      </SuspenseWrapper>
    ),
  },
  {
    path: "/chat",
    element: (
      <SuspenseWrapper>
        <Chat />
      </SuspenseWrapper>
    ),
  },
  {
    path: "/demo",
    element: (
      <SuspenseWrapper>
        <Demo />
      </SuspenseWrapper>
    ),
  },
  {
    path: "*",
    element: (
      <SuspenseWrapper>
        <Landing />
      </SuspenseWrapper>
    ),
  },
]);
