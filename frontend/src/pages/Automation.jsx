import { useState } from "react";
import api from "../services/api";

export default function Automation() {
  const [message, setMessage] = useState("");
  const [ticketId, setTicketId] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runAutomation = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await api.post("/automation/self-heal", {
        message,
        ticket_id: ticketId || null,
      });

      setResult(response.data);
    } catch (error) {
      console.error(error);

      setResult({
        status: "error",
        message:
          "Unable to connect to the automation service.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>

      <div className="page-header">
        <h1>Self-Healing Automation</h1>

        <p>
          AI-driven diagnosis, controlled remediation and ServiceNow
          incident updates.
        </p>
      </div>

      {/* Automation workflow */}
      <div className="panel">

        <div className="panel-header">
          <div>
            <h2>Automation Workflow</h2>
            <p className="panel-description">
              Controlled automation prevents the AI from executing
              arbitrary system actions.
            </p>
          </div>

          <span className="kb-status">
            Automation Active
          </span>
        </div>

        <div className="automation-flow">

          <div className="automation-step">
            <div className="step-number">1</div>
            <strong>Identify</strong>
            <span>Understand employee issue</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="automation-step">
            <div className="step-number">2</div>
            <strong>Diagnose</strong>
            <span>Analyze request</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="automation-step">
            <div className="step-number">3</div>
            <strong>Knowledge Search</strong>
            <span>Retrieve approved KB</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="automation-step">
            <div className="step-number">4</div>
            <strong>Execute</strong>
            <span>Approved action</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="automation-step">
            <div className="step-number">5</div>
            <strong>Validate</strong>
            <span>Verify result</span>
          </div>

          <div className="flow-arrow">→</div>

          <div className="automation-step">
            <div className="step-number">6</div>
            <strong>Update ITSM</strong>
            <span>ServiceNow + audit</span>
          </div>

        </div>

      </div>

      {/* Test automation */}
      <div className="panel automation-test-panel">

        <div className="panel-header">
          <div>
            <h2>Run Self-Healing Automation</h2>

            <p className="panel-description">
              Try an approved automatable issue.
            </p>
          </div>
        </div>

        <div className="automation-input-grid">

          <div>
            <label>Employee Issue</label>

            <textarea
              rows="4"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Example: My password has expired."
            />
          </div>

          <div>
            <label>ServiceNow Incident</label>

            <input
              value={ticketId}
              onChange={(e) => setTicketId(e.target.value)}
              placeholder="Example: INC1002"
            />

            <div className="automation-examples">

              <button
                onClick={() => {
                  setMessage("My password has expired.");
                  setTicketId("INC1002");
                }}
              >
                Password Reset
              </button>

              <button
                onClick={() => {
                  setMessage(
                    "My account is locked."
                  );
                  setTicketId("INC1003");
                }}
              >
                Account Unlock
              </button>

              <button
                onClick={() => {
                  setMessage(
                    "My Outlook emails are not syncing."
                  );
                  setTicketId("INC1004");
                }}
              >
                Outlook Restart
              </button>

            </div>

          </div>

        </div>

        <button
          className="primary-button"
          onClick={runAutomation}
          disabled={loading}
        >
          {loading
            ? "Running Automation..."
            : "Run Self-Healing Agent"}
        </button>

      </div>

      {/* Result */}
      {result && (
        <div className="panel automation-result">

          <div className="panel-header">

            <div>
              <h2>Automation Result</h2>
            </div>

            <span
              className={
                result.status === "resolved"
                  ? "result-status success"
                  : "result-status failure"
              }
            >
              {result.status}
            </span>

          </div>

          <p className="result-message">
            {result.message}
          </p>

          <div className="automation-result-grid">

            <div className="result-card">
              <label>Action</label>

              <strong>
                {result.automation?.action || "None"}
              </strong>
            </div>

            <div className="result-card">
              <label>Execution</label>

              <strong>
                {result.automation?.execution?.status ||
                  "Not executed"}
              </strong>
            </div>

            <div className="result-card">
              <label>Validation</label>

              <strong>
                {result.automation?.validation?.success
                  ? "Successful"
                  : "Not validated"}
              </strong>
            </div>

            <div className="result-card">
              <label>ServiceNow</label>

              <strong>
                {result.servicenow?.number ||
                  "Not updated"}
              </strong>
            </div>

          </div>

          {result.knowledge?.sources?.length > 0 && (
            <div className="automation-sources">

              <h3>Knowledge Used</h3>

              {result.knowledge.sources.map((source) => (
                <div
                  className="source-item"
                  key={source.article_id}
                >
                  {source.article_id} — {source.title}
                </div>
              ))}

            </div>
          )}

          {result.audit && (
            <div className="audit-box">

              <strong>Audit Trail Recorded</strong>

              <p>
                Automation ID: {result.audit.automation_id}
              </p>

              <p>
                Audit ID: {result.audit.audit_id}
              </p>

            </div>
          )}

        </div>
      )}

    </div>
  );
}