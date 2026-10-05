export default function Knowledge() {
  const articles = [
    {
      id: "KB001",
      title: "VPN Authentication Failure",
      category: "Network",
      subcategory: "VPN",
      owner: "Network Support",
      priority: "P2",
    },
    {
      id: "KB002",
      title: "Password Expired or Password Reset Required",
      category: "Account and Access",
      subcategory: "Password",
      owner: "Identity and Access Management",
      priority: "P2",
    },
    {
      id: "KB003",
      title: "Outlook Email Synchronization and Connectivity",
      category: "Collaboration",
      subcategory: "Outlook",
      owner: "Collaboration Support",
      priority: "P3",
    },
    {
      id: "KB004",
      title: "Corporate Wi-Fi Connectivity Problem",
      category: "Network",
      subcategory: "Wi-Fi",
      owner: "Network Support",
      priority: "P3",
    },
    {
      id: "KB005",
      title: "Slow Laptop or Poor System Performance",
      category: "Hardware and Performance",
      subcategory: "Laptop Performance",
      owner: "End User Computing",
      priority: "P3",
    },
    {
      id: "KB006",
      title: "Approved Software Installation Request",
      category: "Software and Applications",
      subcategory: "Software Installation",
      owner: "Endpoint Management",
      priority: "P3",
    },
    {
      id: "KB007",
      title: "Corporate Application Access Request",
      category: "Account and Access",
      subcategory: "Application Access",
      owner: "Identity and Access Management",
      priority: "P2",
    },
  ];

  return (
    <div>

      <div className="page-header">
        <h1>Knowledge Base</h1>

        <p>
          Approved enterprise knowledge used by the AI retrieval
          and self-service workflows.
        </p>
      </div>

      <div className="panel">

        <div className="panel-header">
          <div>
            <h2>Knowledge Articles</h2>
            <p className="panel-description">
              7 approved knowledge articles available for semantic search.
            </p>
          </div>

          <span className="kb-status">
            RAG Active
          </span>
        </div>

        <div className="knowledge-table">

          <div className="knowledge-header">
            <span>ID</span>
            <span>Article</span>
            <span>Category</span>
            <span>Owner</span>
            <span>Priority</span>
          </div>

          {articles.map((article) => (
            <div
              className="knowledge-row"
              key={article.id}
            >

              <strong>{article.id}</strong>

              <div>
                <strong>{article.title}</strong>

                <span className="article-subcategory">
                  {article.subcategory}
                </span>
              </div>

              <span>{article.category}</span>

              <span>{article.owner}</span>

              <span
                className={`priority-badge ${article.priority.toLowerCase()}`}
              >
                {article.priority}
              </span>

            </div>
          ))}

        </div>

      </div>

      <div className="knowledge-info-grid">

        <div className="panel">

          <h2>RAG Pipeline</h2>

          <div className="pipeline">

            <div className="pipeline-step">
              <strong>1</strong>
              <span>Knowledge Documents</span>
            </div>

            <div className="pipeline-arrow">→</div>

            <div className="pipeline-step">
              <strong>2</strong>
              <span>Chunking</span>
            </div>

            <div className="pipeline-arrow">→</div>

            <div className="pipeline-step">
              <strong>3</strong>
              <span>Embeddings</span>
            </div>

            <div className="pipeline-arrow">→</div>

            <div className="pipeline-step">
              <strong>4</strong>
              <span>FAISS Search</span>
            </div>

            <div className="pipeline-arrow">→</div>

            <div className="pipeline-step">
              <strong>5</strong>
              <span>Grounded Answer</span>
            </div>

          </div>

        </div>

        <div className="panel">

          <h2>AI Governance</h2>

          <div className="governance-item">
            <span className="governance-icon">✓</span>
            <div>
              <strong>Approved Sources</strong>
              <p>
                Responses are grounded in the approved knowledge base.
              </p>
            </div>
          </div>

          <div className="governance-item">
            <span className="governance-icon">✓</span>
            <div>
              <strong>Source Attribution</strong>
              <p>
                Retrieved knowledge articles are displayed with AI responses.
              </p>
            </div>
          </div>

          <div className="governance-item">
            <span className="governance-icon">✓</span>
            <div>
              <strong>Fallback</strong>
              <p>
                Requests without sufficient knowledge are escalated.
              </p>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}