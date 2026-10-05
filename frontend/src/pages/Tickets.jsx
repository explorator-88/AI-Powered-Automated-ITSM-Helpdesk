import { useState } from "react";
import api from "../services/api";

export default function Tickets() {

  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const createTicket = async () => {

    if (!message.trim()) return;

    setLoading(true);

    try {

      const response = await api.post("/tickets/intake", {
        message,
      });

      setResult(response.data);

    } catch (error) {

      alert("Ticket creation failed.");

    } finally {

      setLoading(false);

    }
  };

  return (
    <div>

      <div className="page-header">
        <h1>Intelligent Ticket Intake</h1>
        <p>
          AI automatically analyzes and routes employee incidents.
        </p>
      </div>

      <div className="panel">

        <textarea
          rows="5"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Example: I cannot connect to VPN since this morning. Authentication keeps failing."
          style={{
            width: "100%",
            padding: "14px",
            border: "1px solid #d1d5db",
            borderRadius: "8px",
            resize: "vertical",
          }}
        />

        <button
          onClick={createTicket}
          className="primary-button"
        >
          {loading ? "Analyzing..." : "Analyze & Create Ticket"}
        </button>

      </div>

      {result && (

        <div className="panel result-panel">

          <h2>AI Ticket Analysis</h2>

          <div className="analysis-grid">

            <div>
              <label>Intent</label>
              <strong>{result.analysis.intent}</strong>
            </div>

            <div>
              <label>Category</label>
              <strong>{result.analysis.category}</strong>
            </div>

            <div>
              <label>Subcategory</label>
              <strong>{result.analysis.subcategory}</strong>
            </div>

            <div>
              <label>Priority</label>
              <strong>{result.analysis.priority}</strong>
            </div>

            <div>
              <label>Impact</label>
              <strong>{result.analysis.impact}</strong>
            </div>

            <div>
              <label>Urgency</label>
              <strong>{result.analysis.urgency}</strong>
            </div>

            <div>
              <label>Assignment Group</label>
              <strong>{result.analysis.assignment_group}</strong>
            </div>

            <div>
              <label>Confidence</label>
              <strong>
                {(result.analysis.confidence * 100).toFixed(0)}%
              </strong>
            </div>

          </div>

          {result.servicenow && (
            <div className="success-box">
              ServiceNow Incident Created:{" "}
              <strong>{result.servicenow.number}</strong>
            </div>
          )}

          <h3>Suggested Resolution</h3>

          <p>{result.suggested_resolution}</p>

        </div>

      )}

    </div>
  );
}