import { useEffect, useState } from "react";
import { Activity, Stethoscope } from "lucide-react";
import { getHealth } from "./api/client";
import { AiSafetyEvaluation } from "./pages/AiSafetyEvaluation";
import type { HealthResponse } from "./types/audit";

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState("");

  useEffect(() => {
    let ignore = false;

    getHealth()
      .then((response) => {
        if (!ignore) {
          setHealth(response);
        }
      })
      .catch((error) => {
        if (!ignore) {
          setHealthError(error instanceof Error ? error.message : "FastAPI is not reachable.");
        }
      });

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">AS</div>
          <div>
            <strong>AfriSafeBench</strong>
            <span>AI safety evaluation tool</span>
          </div>
        </div>
        <nav>
          <button className="nav-button nav-button--active">
            <Stethoscope size={18} />
            AI Safety Evaluation
          </button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h1>AI Safety Evaluation</h1>
            <p>African healthcare AI deployment risk assessment and governance recommendations.</p>
          </div>
          <div className={healthError ? "api-state api-state--error" : "api-state"}>
            <Activity size={16} />
            <span>{healthError ? "API offline" : health ? "API online" : "Checking API"}</span>
          </div>
        </header>

        {healthError ? <div className="error-banner">{healthError}</div> : null}
        {health ? (
          <div className="index-strip">
            <div>
              <span>AfriSafeBench Frameworks</span>
              <strong>{health.afrisafe_frameworks_index_available ? "Available" : "Missing"}</strong>
            </div>
          </div>
        ) : null}

        <AiSafetyEvaluation />
      </main>
    </div>
  );
}
