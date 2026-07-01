import { createBrowserRouter } from "react-router";
import { lazy, Suspense } from "react";

// Lazy-loaded page components for code-splitting
const Landing = lazy(() => import("./pages/Landing"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Chat = lazy(() => import("./pages/Chat"));
const Demo = lazy(() => import("./pages/Demo"));

// Simple loading fallback matching the app's dark theme
function PageLoader() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#080D1A",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div className="flex items-center gap-3">
        <div
          className="animate-spin-slow"
          style={{
            width: "24px",
            height: "24px",
            borderRadius: "50%",
            border: "3px solid #1E2D4A",
            borderTopColor: "#3B7BF6",
          }}
        />
        <span
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: "14px",
            color: "#8B9CC8",
          }}
        >
          Loading…
        </span>
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
]);
