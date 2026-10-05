import { useState } from "react";
import api from "../services/api";

export default function Assistant() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const askAssistant = async () => {

    if (!message.trim()) return;

    setLoading(true);

    try {

      const result = await api.post("/chat", {
        message,
      });

      setResponse(result.data);

    } catch (error) {

      setResponse({
        answer: "Unable to connect to the ITSM backend.",
        sources: [],
      });

    } finally {
      setLoading(false);
    }
  };

  return (
    <div>

      <div className="page-header">
        <h1>Employee Self-Service</h1>
        <p>
          Ask the AI assistant about IT issues or request support.
        </p>
      </div>

      <div className="panel">

        <div className="chat-area">

          <div className="assistant-message">
            <strong>AI ITSM Assistant</strong>
            <p>
              Hello! I can help with VPN, passwords, Outlook,
              Wi-Fi, laptop performance and software requests.
            </p>
          </div>

          {response && (
            <div className="assistant-message">

              <strong>AI Response</strong>

              <p>{response.answer}</p>

              {response.confidence !== undefined && (
                <small>
                  Confidence:{" "}
                  {(response.confidence * 100).toFixed(1)}%
                </small>
              )}

              {response.sources?.length > 0 && (
                <div className="source-list">

                  <strong>Knowledge Sources</strong>

                  {response.sources.map((source) => (
                    <div
                      className="source-item"
                      key={source.article_id}
                    >
                      {source.article_id} — {source.title}
                    </div>
                  ))}

                </div>
              )}

            </div>
          )}

        </div>

        <div className="quick-actions">

          <button
            onClick={() =>
              setMessage("My VPN authentication keeps failing.")
            }
          >
            VPN Issue
          </button>

          <button
            onClick={() =>
              setMessage("My password has expired.")
            }
          >
            Password
          </button>

          <button
            onClick={() =>
              setMessage("My Outlook emails are not syncing.")
            }
          >
            Outlook
          </button>

          <button
            onClick={() =>
              setMessage("I need Visual Studio Code installed.")
            }
          >
            Software
          </button>

        </div>

        <div className="chat-input">

          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe your IT issue..."
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askAssistant();
              }
            }}
          />

          <button onClick={askAssistant}>
            {loading ? "Analyzing..." : "Ask AI"}
          </button>

        </div>

      </div>

    </div>
  );
}