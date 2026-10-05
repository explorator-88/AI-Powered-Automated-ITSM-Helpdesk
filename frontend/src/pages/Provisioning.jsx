import { useState } from "react";
import api from "../services/api";

const softwareCatalogue = [
  {
    id: "SW001",
    name: "Visual Studio Code",
    category: "Development Tools",
    description: "Source-code editor for software development.",
  },
  {
    id: "SW002",
    name: "Google Chrome",
    category: "Browser",
    description: "Approved enterprise web browser.",
  },
  {
    id: "SW003",
    name: "Python",
    category: "Development Tools",
    description: "Python development environment.",
  },
  {
    id: "SW004",
    name: "Postman",
    category: "Development Tools",
    description: "API development and testing tool.",
  },
  {
    id: "SW005",
    name: "7-Zip",
    category: "Utilities",
    description: "File compression and archive utility.",
  },
  {
    id: "SW006",
    name: "Git",
    category: "Development Tools",
    description: "Distributed version-control system.",
  },
];

export default function Provisioning() {
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("employee");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const requestSoftware = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await api.post("/provisioning/request", {
        message,
        username,
      });

      setResult(response.data);
    } catch (error) {
      console.error(error);

      setResult({
        status: "error",
        message: "Unable to connect to the provisioning service.",
      });
    } finally {
      setLoading(false);
    }
  };

  const selectSoftware = (softwareName) => {
    setMessage(`I need ${softwareName} installed.`);
  };

  return (
    <div>
      <div className="page-header">
        <h1>Software Provisioning</h1>
        <p>
          Request approved software through AI-driven catalogue selection,
          ServiceNow and automated provisioning.
        </p>
      </div>

      {/* Software Catalogue */}
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Approved Software Catalogue</h2>
            <p className="panel-description">
              Software available for automated enterprise provisioning.
            </p>
          </div>

          <span className="kb-status">Catalogue Active</span>
        </div>

        <div className="software-grid">
          {softwareCatalogue.map((software) => (
            <div className="software-card" key={software.id}>
              <div className="software-icon">
                {software.name.substring(0, 2).toUpperCase()}
              </div>

              <div className="software-info">
                <h3>{software.name}</h3>

                <span className="software-category">
                  {software.category}
                </span>

                <p>{software.description}</p>

                <button
                  className="secondary-button"
                  onClick={() => selectSoftware(software.name)}
                >
                  Request
                </button>
              </div>

              <span className="approved-badge">Approved</span>
            </div>
          ))}
        </div>
      </div>

      {/* Request Form */}
      <div className="panel provisioning-request">
        <div className="panel-header">
          <div>
            <h2>Request Software</h2>
            <p className="panel-description">
              Describe the software you need. The AI workflow identifies the
              catalogue item and creates the ServiceNow request.
            </p>
          </div>
        </div>

        <div className="provisioning-form">
          <div>
            <label>Employee</label>

            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Employee username"
            />
          </div>

          <div>
            <label>Software Request</label>

            <textarea
              rows="4"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Example: I need Visual Studio Code installed."
            />
          </div>
        </div>

        <button
          className="primary-button"
          onClick={requestSoftware}
          disabled={loading}
        >
          {loading ? "Processing Request..." : "Submit Software Request"}
        </button>

        <div className="provisioning-examples">
          <span>Try:</span>

          <button onClick={() => selectSoftware("Visual Studio Code")}>
            Visual Studio Code
          </button>

          <button onClick={() => selectSoftware("Postman")}>
            Postman
          </button>

          <button onClick={() => selectSoftware("Python")}>
            Python
          </button>
        </div>
      </div>

      {/* Result */}
      {result && (
        <div className="panel provisioning-result">
          <div className="panel-header">
            <div>
              <h2>Provisioning Result</h2>
            </div>

            <span
              className={
                result.status === "completed"
                  ? "result-status success"
                  : "result-status failure"
              }
            >
              {result.status}
            </span>
          </div>

          <p className="result-message">{result.message}</p>

          {result.software && (
            <div className="provisioning-result-grid">
              <div className="result-card">
                <label>Software</label>
                <strong>{result.software.name}</strong>
              </div>

              <div className="result-card">
                <label>Software ID</label>
                <strong>{result.software.software_id}</strong>
              </div>

              <div className="result-card">
                <label>Provisioning</label>
                <strong>
                  {result.provisioning?.status || "Pending"}
                </strong>
              </div>

              <div className="result-card">
                <label>ServiceNow Request</label>
                <strong>
                  {result.servicenow?.number || "Not created"}
                </strong>
              </div>
            </div>
          )}

          {result.provisioning && (
            <div className="provisioning-success-box">
              <strong>✓ Provisioning Workflow Completed</strong>

              <p>
                {result.provisioning.message}
              </p>

              <div className="workflow-reference">
                <span>
                  ServiceNow:{" "}
                  <strong>
                    {result.servicenow?.number || "N/A"}
                  </strong>
                </span>

                <span>
                  Audit ID:{" "}
                  <strong>
                    {result.audit_id || "N/A"}
                  </strong>
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}