import { createRoot } from "react-dom/client";
import App from "./app/App";
import "./styles/index.css";
import { AppProvider } from "./lib/store";
import { ErrorBoundary } from "./app/components/ErrorBoundary";

createRoot(document.getElementById("root")!).render(
  <ErrorBoundary>
    <AppProvider>
      <App />
    </AppProvider>
  </ErrorBoundary>
);
