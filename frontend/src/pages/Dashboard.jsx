import { useEffect, useState } from "react";
import {
  Ticket,
  CheckCircle,
  AlertTriangle,
  Package,
  Zap,
  RefreshCw,
} from "lucide-react";

import api from "../services/api";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(false);

      const response = await api.get("/dashboard/stats");
      setStats(response.data);
    } catch (err) {
      console.error("Dashboard loading failed:", err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const statCards = [
    {
      title: "Total Tickets",
      value: stats?.total_tickets ?? 0,
      icon: Ticket,
      description: "Tickets created",
    },
    {
      title: "Open Tickets",
      value: stats?.open_tickets ?? 0,
      icon: AlertTriangle,
      description: "Awaiting resolution",
    },
    {
      title: "AI Resolved",
      value: stats?.resolved_tickets ?? 0,
      icon: CheckCircle,
      description: "Successfully resolved",
    },
    {
      title: "Software Requests",
      value: stats?.software_requests ?? 0,
      icon: Package,
      description: "Provisioning requests",
    },
    {
      title: "Automation Success",
      value: `${stats?.automation_success_rate ?? 0}%`,
      icon: Zap,
      description: `${stats?.successful_automations ?? 0} successful automations`,
    },
  ];

  return (
    <div>
      {/* Page Header */}
      <div className="page-header dashboard-header">
        <div>
          <h1>ITSM Command Center</h1>
          <p>
            AI-powered enterprise IT service management and intelligent
            automation.
          </p>
        </div>

        <button
          className="secondary-button refresh-button"
          onClick={loadDashboard}
          disabled={loading}
        >
          <RefreshCw size={15} className={loading ? "spin" : ""} />
          Refresh
        </button>
      </div>

      {/* Error State */}
      {error && (
        <div className="result-panel error-panel">
          <strong>Unable to load dashboard data.</strong>
          <p>
            Make sure the FastAPI backend is running and the dashboard
            statistics endpoint is available.
          </p>

          <button className="primary-button" onClick={loadDashboard}>
            Try Again
          </button>
        </div>
      )}

      {/* Statistics */}
      <div className="stats-grid">
        {statCards.map((stat) => {
          const Icon = stat.icon;

          return (
            <div className="stat-card" key={stat.title}>
              <div className="stat-top">
                <div>
                  <span className="stat-title">{stat.title}</span>

                  <div className="stat-value">
                    {loading ? "—" : stat.value}
                  </div>

                  <span className="stat-description">
                    {stat.description}
                  </span>
                </div>

                <div className="stat-icon">
                  <Icon size={20} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Dashboard Grid */}
      <div className="dashboard-grid">
        {/* Ticket Overview */}
        <div className="panel">
          <div className="panel-header">
            <div>
              <h2>Ticket Overview</h2>
              <p className="panel-description">
                Current IT service management workload.
              </p>
            </div>
          </div>

          <div className="incident-row">
            <div>
              <strong>Total Tickets</strong>
              <span>All tickets stored in MongoDB</span>
            </div>

            <span className="badge">
              {loading ? "—" : stats?.total_tickets ?? 0}
            </span>
          </div>

          <div className="incident-row">
            <div>
              <strong>Open Tickets</strong>
              <span>Tickets currently awaiting resolution</span>
            </div>

            <span className="badge warning">
              {loading ? "—" : stats?.open_tickets ?? 0}
            </span>
          </div>

          <div className="incident-row">
            <div>
              <strong>AI Resolved</strong>
              <span>Tickets resolved through automation</span>
            </div>

            <span className="badge success">
              {loading ? "—" : stats?.resolved_tickets ?? 0}
            </span>
          </div>

          <div className="incident-row">
            <div>
              <strong>Escalated</strong>
              <span>Requests requiring human support</span>
            </div>

            <span className="badge danger">
              {loading ? "—" : stats?.escalated_tickets ?? 0}
            </span>
          </div>
        </div>

        {/* Automation Overview */}
        <div className="panel">
          <div className="panel-header">
            <div>
              <h2>Automation Overview</h2>
              <p className="panel-description">
                Controlled AI-assisted remediation activity.
              </p>
            </div>
          </div>

          <div className="automation-summary">
            <div className="automation-summary-item">
              <span>Total Automations</span>
              <strong>
                {loading ? "—" : stats?.total_automations ?? 0}
              </strong>
            </div>

            <div className="automation-summary-item">
              <span>Successful</span>
              <strong>
                {loading ? "—" : stats?.successful_automations ?? 0}
              </strong>
            </div>

            <div className="automation-summary-item">
              <span>Success Rate</span>
              <strong>
                {loading
                  ? "—"
                  : `${stats?.automation_success_rate ?? 0}%`}
              </strong>
            </div>
          </div>

          <div className="automation-status">
            <div className="status-dot"></div>

            <div>
              <strong>Automation Engine</strong>
              <span>
                Controlled actions are executed through the approved action
                registry.
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Architecture / Workflow */}
      <div className="panel dashboard-workflow">
        <div className="panel-header">
          <div>
            <h2>Intelligent ITSM Workflow</h2>
            <p className="panel-description">
              How an employee request moves through the AI-enabled platform.
            </p>
          </div>
        </div>

        <div className="workflow-grid">
          <div className="workflow-card">
            <div className="workflow-number">01</div>
            <strong>Employee Request</strong>
            <span>
              Employee submits a question, incident, access request, or
              software request.
            </span>
          </div>

          <div className="workflow-arrow">→</div>

          <div className="workflow-card">
            <div className="workflow-number">02</div>
            <strong>AI Analysis</strong>
            <span>
              Intent, category, priority, assignment group, and confidence
              are determined.
            </span>
          </div>

          <div className="workflow-arrow">→</div>

          <div className="workflow-card">
            <div className="workflow-number">03</div>
            <strong>RAG / Automation</strong>
            <span>
              Approved knowledge is retrieved or a controlled automation
              workflow is selected.
            </span>
          </div>

          <div className="workflow-arrow">→</div>

          <div className="workflow-card">
            <div className="workflow-number">04</div>
            <strong>ITSM Action</strong>
            <span>
              MongoDB records the workflow and ServiceNow receives the
              incident or request.
            </span>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="panel system-status-panel">
        <div className="panel-header">
          <div>
            <h2>System Status</h2>
            <p className="panel-description">
              Current prototype service configuration.
            </p>
          </div>
        </div>

        <div className="system-status-grid">
          <div className="system-status-item">
            <span className="system-status-indicator"></span>
            <div>
              <strong>FastAPI Backend</strong>
              <span>Connected</span>
            </div>
          </div>

          <div className="system-status-item">
            <span className="system-status-indicator"></span>
            <div>
              <strong>MongoDB Atlas</strong>
              <span>Connected</span>
            </div>
          </div>

          <div className="system-status-item">
            <span className="system-status-indicator"></span>
            <div>
              <strong>RAG Knowledge Base</strong>
              <span>FAISS / Active</span>
            </div>
          </div>

          <div className="system-status-item">
            <span className="system-status-indicator"></span>
            <div>
              <strong>ServiceNow</strong>
              <span>Mock API / Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}